import os
import pathlib

from flask import Flask
from functional_tests.demo.test_suite.lib.pages.home_page import HomePage
from functional_tests.demo.test_suite.lib.pages.login_page import LoginPage

from naga.test.framework.actions.web.playwright_actions import \
    PlayWrightActions
from naga.test.framework.utils.data_store import data

root = str(pathlib.Path().resolve().parents[0].parents[0].parents[0].parents[0])

os.environ["apiBaseUrl"] = "https://jsonplaceholder.typicode.com/"
os.environ["testType"] = "server"
os.environ["demo_path"] = root + "/functional_tests/demo"

from functional_tests.demo.test_suite.lib.api.sample_rest import SampleRestAPI

app = Flask(__name__)


@app.route("/server")
def index():
    return "Hellow, this Server works"


@app.route("/demo")
def demo():
    return SampleRestAPI.get_request()


@app.route("/web")
def web():
    data.suite.enable_video = "no"
    iWeb = PlayWrightActions()
    iWeb.open_browser("chrome")
    iWeb.navigate_to_url("https://www.saucedemo.com/")
    data.scenario.iWeb = iWeb
    LoginPage().login("standard_user", "secret_sauce")
    HomePage().homePage_Loaded()
    iWeb.quit_browser()
    return "Sauce page opened"