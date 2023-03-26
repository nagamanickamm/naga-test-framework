import os
import pathlib

from naga.test.framework.actions.api.rest_actions import RestActions

root = str(pathlib.Path().resolve().parents[0])

os.environ["rest_protocol"] = 'https'
os.environ["slots_path"] = root + "/slots"
os.environ["current_working_dir"] = os.getcwd() + '/neon/test/functional_tests/demo'
os.environ["apiBaseURL"] = ""
os.environ["testType"] = "perf"
log_settings = 'both' if os.getenv('log') is None else os.getenv('log')

from locust import SequentialTaskSet, User, constant, task

from naga.test.framework.clientfactory.locust_factory import LocustFactory
from naga.test.functional_tests.demo.test_suite.lib.api.sample_rest import \
    SampleRestAPI


class TestLocust(SequentialTaskSet):

    @task
    @LocustFactory.handle_exception
    def get_demo(self):
        LocustFactory.set_task_name("Demo - Get Request")
        SampleRestAPI.get_request()

    @task
    @LocustFactory.handle_exception
    def post_demo(self):
        LocustFactory.set_task_name("Demo - Post Request")
        SampleRestAPI.post_request()


class Execution(User):
    tasks = {TestLocust}

    def on_start(self):
        wait_time = constant(1)
        LocustFactory.set_user(self)
        os.environ["apiBaseURL"] = self.host.replace("https://", "").replace('http://', '').replace("wss://", "").replace("ws://",
                                                                                                                          "").replace("/", '')
