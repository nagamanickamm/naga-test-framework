from naga.test.framework.interface.iweb import IWeb
from naga.test.framework.locators.locator import Locator
from naga.test.framework.utils.data_store import data
from naga.test.framework.utils.report_utils import ReportUtils


class Content:
    txtUsername = (Locator.id, "user-name")
    txtPassword = (Locator.id, "password")
    btnLogin = (Locator.id, "login-button")
    title = (Locator.xpath, "//span[@class='title']")


class LoginPage:
    iWeb: IWeb

    def __init__(self):
        self.iWeb = data.scenario.iWeb

    def login(self, username, password):
        self.iWeb.find(Content.txtUsername).type(username)
        self.iWeb.find(Content.txtPassword).type(password)
        ReportUtils.log("Entered username and password")
        self.iWeb.find(Content.btnLogin).click()
        ReportUtils.log("Clicked on login button")
