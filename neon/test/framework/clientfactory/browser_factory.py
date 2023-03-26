import os

from playwright.sync_api import Page, sync_playwright
from screeninfo import get_monitors
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.service import Service
from selenium.webdriver.ie.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager

from naga.test.framework.utils.data_store import data
from naga.test.framework.utils.report_utils import ReportUtils


class BrowserFactory:
    _driver: WebDriver = None
    _page: Page = None
    _context = None
    _browser = None
    _playWright = None
    tabs = dict({})

    def __init__(self, headless, video) -> None:
        self.headless = headless
        self.video = video

    def open_selenium_browser(self, browserName):
        if browserName == "chrome":
            chrome_options = ChromeOptions()
            if self.headless == "yes":
                chrome_options.add_argument("--headless")
            _driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

        elif browserName == "firefox":
            firefox_options = FirefoxOptions()
            if self.headless == "yes":
                firefox_options.headless = True
                _driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_options=firefox_options)
            else:
                _driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        elif browserName == "ie":
            _driver = webdriver.Ie(service=Service(IEDriverManager().install()))

        else:
            ReportUtils.log("Browser type not found - " + browserName)
            raise Exception("Browser type not found - " + browserName)
        ReportUtils.log("Selenium browser opened")

        self._driver = _driver
        self._driver.maximize_window()
        self._driver.delete_all_cookies()
        self.tabs.update({"default": self._driver.current_window_handle})

    def quit_selenium_browser(self):
        self._driver.quit()

    def start_play_wright_engine(self):
        self._playWright = sync_playwright().start()
        return self._playWright

    def open_play_wright_browser(self, browserName):
        self._playWright = self.start_play_wright_engine()
        ReportUtils.log("Entering open_playwright_browser")
        if browserName == "chrome":
            browser = self._playWright.chromium.launch(headless=False, slow_mo=50)
            if self.headless == "yes":
                browser = self._playWright.chromium.launch(headless=True, slow_mo=50)
            if self.video == "yes":
                context = browser.new_context()
                page = browser.new_page(record_video_dir="./reports/video")
            else:
                context = browser.new_context()
                page = browser.new_page()

        elif browserName == "firefox":
            self._playWright.firefox.launch(headless=False, slow_mo=50)
            if self.headless == "yes":
                self._playWright.firefox.launch(headless=True, slow_mo=50)
            page = self._playWright.new_page()

        elif browserName == "webkit":
            self._playWright.webkit.launch(headless=False, slow_mo=50)
            if self.headless == "yes":
                self._playWright.webkit.launch(headless=True, slow_mo=50)
            page = self._playWright.new_page()
        else:
            ReportUtils.log("Browser type not found - " + browserName)
            raise Exception("Browser type not found - " + browserName)

        def check(response):
            if (response.status >= 400):
                assert False, "network error----Response Status--- " + str(response.status) + "-----url--- " + response.url

        page.on("response", check)
        self._page = page
        self._context = context
        self._browser = browser
        self.tabs.update({"default": page})
        self._page.set_viewport_size({"width": get_monitors()[0].width, "height": get_monitors()[0].height})

    def quit_play_wright_browser(self):
        ReportUtils.log("Entering into play wright close")
        self._browser.close()
        self._context.close()
        self.stop_play_wright_engine()
        ReportUtils.log("closed playwright browser successfully")

    def stop_play_wright_engine(self):
        self._playWright.stop()
