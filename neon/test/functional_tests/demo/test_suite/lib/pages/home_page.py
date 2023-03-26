from naga.test.framework.interface.iweb import IWeb
from naga.test.framework.locators.locator import Locator
from naga.test.framework.utils.data_store import data
from naga.test.framework.utils.report_utils import ReportUtils


class Content:
    title = (Locator.xpath, "//span[@class='title']")


class HomePage:

    iWeb: IWeb

    def __init__(self):
        self.iWeb = data.scenario.iWeb

    def homePage_Loaded(self):
        if not self.iWeb.wait_for(Content.title, data.suite.default_page_timeout):
            assert False, "Login not successful"
