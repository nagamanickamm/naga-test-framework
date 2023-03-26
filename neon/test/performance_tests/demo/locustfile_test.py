import os
import pathlib

root = str(pathlib.Path().resolve().parents[0])

os.environ["apiBaseURL"] = ""
os.environ["testType"] = "perf"

from locust import SequentialTaskSet, User, constant, task

from naga.test.framework.clientfactory.locust_factory import LocustFactory


class TestLocust(SequentialTaskSet):

    @task
    def get_demo(self):
        with LocustFactory.start_task("Demo - Get Request") as lf:
            print('task1')

    @task
    def post_demo(self):
        with LocustFactory.start_task("Demo - Post Request") as lf:
            print('task2')


class Execution(User):
    tasks = {TestLocust}

    def on_start(self):
        wait_time = constant(1)
        LocustFactory.set_user(self)
        os.environ["apiBaseURL"] = self.host.replace("https://", "").replace('http://', '').replace("wss://", "").replace("ws://",
                                                                                                                          "").replace("/", '')
