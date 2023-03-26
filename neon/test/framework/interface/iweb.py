from abc import abstractmethod


class IWeb:

    @abstractmethod
    def close_selenium_current_browser(self):
        NotImplementedError
        return self

    @abstractmethod
    def navigate_to_url(self, url):
        NotImplementedError
        return self

    @abstractmethod
    def click(self):
        NotImplementedError
        return self

    @abstractmethod
    def clear(self):
        NotImplementedError
        return self

    @abstractmethod
    def type(self, testData):
        NotImplementedError
        return self

    @abstractmethod
    def find(self, locator):
        NotImplementedError
        return self

    @abstractmethod
    def find(self, locator, timeout):
        NotImplementedError
        return self

    @abstractmethod
    def get_text(self):
        NotImplementedError
        return self

    @abstractmethod
    def wait_for(self, locator, timeToWaitInMilliSec) -> bool:
        NotImplementedError
        return self

    @abstractmethod
    def wait_time(self, seconds):
        NotImplementedError
        return self

    @abstractmethod
    def verify_title(self, textToVerify):
        NotImplementedError
        return self

    @abstractmethod
    def get_current_window_id(self):
        NotImplementedError
        return self

    @abstractmethod
    def get_all_window_id(self):
        NotImplementedError

    @abstractmethod
    def switch_to_window(self, window_id):
        NotImplementedError
        return self

    @abstractmethod
    def take_screenshot(self, path):
        NotImplementedError

    @abstractmethod
    def get_current_url(self):
        NotImplementedError
        return self

    @abstractmethod
    def clear_with_keyboard_and_type_data(self, element, data):
        NotImplementedError
        return self

    @abstractmethod
    def select_from_drop_down(self, dropdown_type, value):
        NotImplementedError
        return self

    @abstractmethod
    def refresh_page(self):
        NotImplementedError
        return self

    @abstractmethod
    def click_and_switch_to_new_window(self):
        NotImplementedError
        return self

    @abstractmethod
    def route(self, url, json_file_python_format):
        NotImplementedError
        return self

    @abstractmethod
    def click_and_wait_for_new_window(self, pageName):
        NotImplementedError
        return self

    @abstractmethod
    def enter_with_keyboard(self):
        NotImplementedError
        return self

    @abstractmethod
    def close_tab(self):
        NotImplementedError
        return self

    @abstractmethod
    def get_input_value(self, locator):
        NotImplementedError
        return self

    @abstractmethod
    def is_alert_present(self, timeout):
        NotImplementedError
        return self

    @abstractmethod
    def alert_accept(self):
        NotImplementedError
        return self

    @abstractmethod
    def alert_dismiss(self):
        NotImplementedError
        return self

    @abstractmethod
    def js_click(self):
        NotImplementedError
        return self

    @abstractmethod
    def keyboard_action(self, action_type):
        NotImplementedError
        return self

    @abstractmethod
    def evaluate(self, expression, arg=None):
        NotImplementedError