import os
import pathlib
import sys

root = str(pathlib.Path().resolve().parents[0].parents[0].parents[0].parents[0])
sys.path.insert(0, root)

from getgauge.python import (after_scenario, after_step, before_scenario, before_suite)

from naga.test.framework.actions.api.websocket_actions import WebsocketActions
from naga.test.framework.actions.web.playwright_actions import \
    PlayWrightActions
from naga.test.framework.actions.web.selenium_actions import SeleniumActions
from naga.test.framework.utils.core import *
from naga.test.framework.utils.data_store import data

webTool = os.getenv("webtool")
execute = os.getenv("execute")
data.suite.enable_video = os.getenv("videorecord")
browserName = os.getenv("browserName")
headless = os.getenv("headless")
webBaseURL = os.getenv("webBaseURL")
os.environ["GH_TOKEN"] = os.getenv("ghToken")
os.environ["current_working_dir"] = os.getcwd()


class Hooks:

    @before_suite
    def before_suite(context):
        SpecHTMLUtils.convert_specs_html(os.getcwd() + '/test_suite/features/specs/', os.getcwd() + '/docs/')
        data.suite.default_page_timeout = os.getenv("pagetimeout")
        data.suite.default_element_timeout = os.getenv("elementtimeout")
        data.suite.webTool = os.getenv("webtool")

    @before_scenario
    def before_scenario(context):
        if execute == "web":
            global iWeb
            iWeb = SeleniumActions() if data.suite.webTool.strip() in "selenium" else PlayWrightActions()
            iWeb.open_browser(browserName)
            data.scenario.iWeb = iWeb
            iWeb.navigate_to_url(webBaseURL)

    @after_scenario
    def close_driver(context):
        if execute == "web":
            iWeb.quit_browser()

        if WebsocketActions.is_open():
            WebsocketActions.close()
        ReportUtils.log("Feature Name is - " + str(context._ExecutionContext__specification.name))
        ReportUtils.log("Scenario Name is - " + str(context._ExecutionContext__scenario.name))
        ReportUtils.log("Tag Name is - " + str(context._ExecutionContext__scenario.tags))
        ReportUtils.log("Failing status is - " + str(context._ExecutionContext__scenario.is_failing))

    @after_step
    def after_step(context):
        path = "\html-report\\test_suite\\features\specs"
        ReportUtils.log("Step Name is - " + str(context._ExecutionContext__step.text))
        ReportUtils.log("Failing status is - " + str(context._ExecutionContext__step._Step__is_failing))
        if execute == "web":
            if context._ExecutionContext__step._Step__is_failing:
                ReportUtils.log("<img src='" + iWeb.take_screenshot(path) + "' width='750' height='500'>")