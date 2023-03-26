import os
import time
from uuid import uuid1

from getgauge.python import Messages
from multipledispatch import dispatch
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from naga.test.framework.clientfactory.browser_factory import BrowserFactory
from naga.test.framework.interface.iweb import IWeb
from naga.test.framework.locators.locator import Locator
from naga.test.framework.utils.report_utils import ReportUtils


class SeleniumActions(IWeb, BrowserFactory):
    _element: WebElement = None

    def __init__(self, headless, video):
        super().__init__(headless, video)

    def open_browser(self, browserName):
        BrowserFactory.open_selenium_browser(self, browserName)

    def quit_browser(self):
        BrowserFactory.quit_selenium_browser(self)

    def wait_for(self, locator, timeToWait) -> bool:
        isElementPresent = False
        waitTime = int(timeToWait) / 1000
        try:
            self._element = WebDriverWait(self._driver, int(waitTime)).until(EC.presence_of_element_located(locator))
            if self._element.is_displayed():
                isElementPresent = True
        except Exception as e:
            ReportUtils.log("Element not present---" + str(e.__cause__))
        return isElementPresent

    def navigate_to_url(self, url):
        self._driver.get(url)
        ReportUtils.log(self._driver.current_url)

    @dispatch(tuple)
    def find(self, locator):
        locatorID = locator[0]
        locatorValue = locator[1]
        ReportUtils.log(locator)
        self._element = self._driver.find_element(locatorID, locatorValue)
        if self._element == None:
            assert False, "element not found"
        return self

    @dispatch(tuple, int)
    def find(self, locator, timeout):
        locatorID = locator[0]
        locatorValue = locator[1]
        if not self.wait_for(locator, timeout):
            assert False, "Element not found:" + locatorValue
        self._element = self._driver.find_element(locatorID, locatorValue)
        return self

    def click(self):
        self._element.click()
        ReportUtils.log("clicked successfully")
        return self

    def type(self, testData):
        self._element.clear()
        self._element.send_keys(testData)
        ReportUtils.log("Test type")
        return self

    def wait_time(self, seconds):
        time.sleep(3)
        return self

    def verify_title(self, textToVerify):
        url = self._driver.title
        ReportUtils.log(url)
        assert url.strip(" ").__contains__(textToVerify), "Failed to verify title"

    def take_screenshot(self, path):
        image = self._driver.get_screenshot_as_png()
        file_name = os.path.join(
            os.getenv("gauge_reports_dir") + path,
            "screenshot-{0}.png".format(uuid1().int),
        )
        file = open(file_name, "wb")
        file.write(image)
        return os.path.basename(file_name)

    def get_current_window_id(self):
        current_window = self._driver.current_window_handle
        return current_window

    def switch_to_window(self, windowName):
        windowId = self.tabs.get(windowName)
        self._driver.switch_to.window(windowId)
        return self

    def get_all_window_id(self):
        handles = self._driver.window_handles
        ReportUtils.log("get_current_window_id" + str(len(handles)))
        return handles

    def get_current_url(self):
        url = self._driver.current_url
        ReportUtils.log("url---" + url)
        return url

    def clear_with_keyboard_and_type_data(self, element: WebElement, data):
        delete = Keys.CONTROL + "a" + Keys.DELETE
        action = ActionChains(self._driver)
        action_to_send = action.send_keys(delete)
        self.wait_time(2)
        element.send_keys(action_to_send + data)
        return self

    def select_from_drop_down_by_visible_text(self, value):
        try:
            select = Select(self._element)
            select.select_by_visible_text(value)
        except Exception as e:
            ReportUtils.log("Error in select from drop down method---" + str(e.__cause__))
            raise Exception("Error in select from drop down method---" + str(e.__cause__))
        return self

    def select_from_drop_down_by_value(self, value):
        try:
            select = Select(self._element)
            select.select_by_value(value)
        except Exception as e:
            ReportUtils.log("Error in select from drop down method---" + str(e.__cause__))
            raise Exception("Error in select from drop down method---" + str(e.__cause__))
        return self

    def select_from_drop_down_by_index(self, value):
        try:
            select = Select(self._element)
            select.select_by_index(value)
        except Exception as e:
            ReportUtils.log("Error in select from drop down method---" + str(e.__cause__))
            raise Exception("Error in select from drop down method---", +str(e.__cause__))
        return self

    def refresh_page(self):
        self._driver.refresh()
        return self

    def get_text(self):
        extract_text = self._element.text
        return extract_text

    def enter_with_keyboard(self):
        self._element.send_keys(Keys.ENTER)
        return self

    def click_and_wait_for_new_window(self, pageName):
        parentWindowId = self.tabs.get("default")
        self._element.click()
        for handle in self.get_all_window_id():
            if handle not in self.tabs.values():
                self.tabs.update({pageName: handle})
                break
        self.switch_to_window(pageName)

    def close_tab(self, windowName):
        self._driver.close()
        self.switch_to_window("default")
        ReportUtils.log("Switched to parent window")

    def close_selenium_current_browser(self):
        self._driver.close()

    def select_from_drop_down(self, dropdown_option, dropdown_value):
        select = Select(self._element)
        if dropdown_option.strip().casefold() == "text":
            select.select_by_visible_text(dropdown_value)
        elif dropdown_option.strip().casefold() == "value":
            select.select_by_value(dropdown_value)
        elif dropdown_option.strip().casefold() == "index":
            select.select_by_index(dropdown_value)
        else:
            select.first_selected_option()

    def is_alert_present(self, timeout):
        is_alert_present = False
        waitTime = int(timeout) / 1000
        try:
            alert = WebDriverWait(self._driver, waitTime).until(EC.alert_is_present())
            if alert:
                is_alert_present = True
        except Exception as e:
            Messages.write_message("Exception occured during waiting for alert--" + str(e.__traceback__))
        return is_alert_present

    def evaluate(self, expression, arg=None):
        return self._driver.execute_script(expression, arg)

    def alert_accept(self):
        alert = self._driver.switch_to.alert
        alert.accept()

    def alert_dismiss(self):
        alert = self._driver.switch_to.alert
        alert.dismiss()

    def js_click(self):
        self._driver.execute_script("arguments[0].click();", self._element)
