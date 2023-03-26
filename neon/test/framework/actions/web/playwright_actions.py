import os
import time
from uuid import uuid1

from getgauge.python import Messages
from multipledispatch import dispatch
from playwright.sync_api import BrowserContext, Page, Route

from naga.test.framework.clientfactory.browser_factory import BrowserFactory
from naga.test.framework.interface.iweb import IWeb
from naga.test.framework.locators.locator import Locator
from naga.test.framework.utils.report_utils import ReportUtils


class PlayWrightActions(IWeb, BrowserFactory):
    _element: Page

    def __init__(self, headless, video):
        super().__init__(headless, video)
        
    def refactor(self, locator):
        match locator[0]:
            case Locator.id:
                return "[id=" + locator[1] + "]"
            case Locator.name:
                return "[name=" + locator[1] + "]"
            case Locator.class_name:
                return "[class=" + locator[1] + "]"
            case _:
                return locator[1]

    def open_browser(self, browserName):
        self.open_play_wright_browser(browserName)

    def quit_browser(self):
        self.quit_play_wright_browser()

    def wait_for(self, locator, timeToWait) -> bool:
        isElementPresent = False
        try:
            if self._page.wait_for_selector(self.refactor(locator), timeout=int(timeToWait)):
                isElementPresent = True
        except Exception as e:
            ReportUtils.log("Element not present---"+str(e.__traceback__))
        return isElementPresent

    def get_current_window_id(self):
        return self._page.context.pages[0]

    def get_all_window_id(self):
        return self._page.context.pages

    def switch_to_window(self, pageName):
        self._page = self.tabs.get(pageName)
        title = self._page.title()
        ReportUtils.log(title)

    def get_current_url(self):
        return self._page.url

    def refresh_page(self):
        self._page.reload()

    def get_text(self):
        return self._element.text_content()

    def navigate_to_url(self, url):
        ReportUtils.log("Navigate to url method")
        self._page.goto(url)
        ReportUtils.log("done url method")

    def click(self):
        self._element.click()
        return self

    def type(self, testData):
        self._element.fill(testData)
        return self
    
    def evaluate(self, expression, arg=None):
        return self._page.evaluate(expression, arg)

    @dispatch(tuple)
    def find(self, locator):
        self._element = self._page.locator(self.refactor(locator))
        return self

    @dispatch(tuple, str)
    def find(self, locator, timeout):
        if not self.wait_for(locator, int(timeout)):
            assert False, "Element not found:"+self.refactor(locator)
        self._element = self._page.locator(self.refactor(locator))
        return self

    def wait_time(self, seconds):
        time.sleep(seconds)

    def verify_title(self, textToVerify):
        assert self._page.url.__contains__(textToVerify)

    def take_screenshot(self, path):
        image = self._page.screenshot()
        file_name = os.path.join(
            os.getenv("gauge_reports_dir") + path,
            "screenshot-{0}.png".format(uuid1().int),
        )
        file = open(file_name, "wb")
        file.write(image)
        return os.path.basename(file_name)

    def click_and_wait_for_new_window(self, pageName):
        with self._page.context.expect_page() as newPage:
            self._element.click()
            time.sleep(2)
            new_page = newPage.value
            self.tabs.update({pageName: new_page})
            self._page = new_page

    def route(self, url, json_file_python_format):
        def handle_route(route: Route) -> None:
            route.fulfill(content_type="application/json",
                          body=json_file_python_format)
        self._page.route(url, handle_route)

    def close_tab(self, pageName):
        self._page = self.tabs.pop(pageName)
        self._page.close()
        self.switch_to_window("default")
        Messages.write_message("Switched to parent window")

    def select_from_drop_down(self, dropdown_option, dropdown_value):
        if dropdown_option.strip().casefold() == "text":
            self._element.select_option(label=dropdown_value)
        elif dropdown_option.strip().casefold() == "value":
            self._element.select_option(value=dropdown_value)
        elif dropdown_option.strip().casefold() == "index":
            self._element.select_option(index=int(dropdown_value))

    def get_input_value(self, locator):
        value = self._page.input_value(self.refactor(locator))
        return value

    def keyboard_action(self, action_type):
        if action_type.strip().casefold() == "tab":
            self._page.keyboard.down("Tab")
        else:
            self._page.keyboard.down("Enter")
        ReportUtils.log("Switched to parent window")
