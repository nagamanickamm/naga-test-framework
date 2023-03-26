# from functools import wraps
import logging
import os
import time
import traceback
from contextlib import contextmanager


class LocustFactory:
    user_data = {}

    def __init__(self, context):
        self.context = context
        self.user = context.user
        self.id = str(id(context.user))
        self.name = 'None'
        self.req_type = 'None'
        self.time_lapsed = 0
        self.start_time = 0
        self.response_message = 'None'
        self.base_url = 'None'
        self.message = ''
        self.task_id = 00
        LocustFactory.user_data[self.id] = LocustFactory.user_data.get(self.id, {})

    # ********************* Start Task *****************************************

    @contextmanager
    def start_task(self, task_name, task_type='Unknown', rate=None, sync_limit=0):
        stop_run = True
        task_failed = False
        exception = ''
        self.locust_user_data = LocustFactory.user_data[self.id]
        self.locust_user_data['message'] = ""
        try:
            self.__queue(rate)
            self.__sync(sync_limit)
            self.start_time = time.time()
            yield self.locust_user_data
            stop_run = False
        except Exception as error:
            stop_run = False
            task_failed = True
            logging.error(f"Id: {self.locust_user_data.get('egm',self.id)}, Message : {traceback.format_exc()}")
            logging.error(f"Message : {str(error)}")
            exception = str(error)[:160] + ' ...............    Check Perf_logs/* Logs for more details...'
        finally:
            LocustFactory.__remove_task(self.name)
            # ----------------- If not On Stop event ------------------
            if not stop_run:
                self.__fire_event(exception, task_name, task_type, self.locust_user_data['message'])
                self.locust_user_data['task_type'] = task_type
                self.__on_failure(task_failed, exception)

    # ********************* Fire Event *****************************************
    def __on_failure(self, task_failed, exception):
        if task_failed:
            timeout = self.locust_user_data.get(f"{self.name}_timeout", 1)
            time.sleep(timeout)
            self.locust_user_data[f"{self.name}_timeout"] = timeout * 2
            func = self.locust_user_data.get('on_failure', None)
            if func is not None:
                func()
            else:
                raise Exception(exception)
        else:
            self.locust_user_data[f"{self.name}_timeout"] = 1

    def __fire_event(self, exception, task_name, task_type, response_message):
        if os.environ["testType"] == "perf":
            end_time = time.time()
            self.time_lapsed = end_time - self.start_time
            message = response_message if response_message != None else ''
            type = str(task_type).strip().upper()

            # Toggle Task ID and ordering
            if type == 'LOCUST':
                self.task_id = '999'
            if os.getenv('enable_locust_task_id', '0') == '1':
                self.name = self.task_id + ' - ' + self.name

            #--------- Fire Event on Locust---------------------------------------
            self.user.environment.events.request.fire(
                request_type=type,
                name=task_name,
                response_time=self.time_lapsed * 1000,
                response="test",
                response_length=len(message.encode('utf-16')) if message is str else len(message),
                exception=exception,
                context=self.user.context(),
            )

    # ********************* Queuing and Syncing *****************************************

    def __queue(self, rate=None):
        # Add Task
        LocustFactory.__add_task(self.name)

        # Get Task ID
        task_list = self.locust_user_data.get('task_list', {})
        if task_list.get(self.name, None) is None:
            self.locust_user_data['task_id'] = "{0:02d}".format(int(self.locust_user_data.get('task_id', 00)) + 1)
            task_list[self.name] = self.locust_user_data['task_id']
        self.locust_user_data['task_list'] = task_list
        self.task_id = task_list[self.name]

        queue_timeout = float(os.getenv('queue_timeout', 0.2))

        # If rate enabled then queue
        if rate is not None:
            for i in range(LocustFactory.__get_task_count(self.name) * 2):
                if LocustFactory.__get_task_count(self.name) > rate:
                    time.sleep(queue_timeout)
                else:
                    break

    def __sync(self, sync_limit=0):
        if sync_limit > 1:
            name = self.name + "_sync"
            LocustFactory.__add_task(name)
            sync_timeout = float(os.getenv('sync_timeout', 0.2))
            for i in range(sync_limit):
                if LocustFactory.__get_task_count(name) + 1 / LocustFactory.get_user_count() + 1 != 1:
                    time.sleep(sync_timeout)
                else:
                    break

    # ********************* Manage User and Task *****************************************
    def __add_task(name):
        LocustFactory.user_data[name] = LocustFactory.user_data.get(name, 0) + 1

    def __remove_task(name):
        LocustFactory.user_data[name] -= 1

    def __get_task_count(name):
        return LocustFactory.user_data.get(name, 1)

    def add_user():
        LocustFactory.user_data['user_count'] = LocustFactory.user_data.get('user_count', 0) + 1

    def remove_user():
        LocustFactory.user_data['user_count'] -= 1

    def get_user_count():
        return LocustFactory.user_data.get('user_count', 0)

    def reset():
        LocustFactory.user_data['user_count'] = 0
        search = "_sync"
        keys = [key for key, val in LocustFactory.user_data.items() if search in key]
        for key in keys:
            del LocustFactory.user_data[key]
