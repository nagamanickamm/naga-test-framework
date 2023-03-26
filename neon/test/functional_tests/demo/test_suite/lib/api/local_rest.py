import os
from email import header

from naga.test.framework.actions.api.rest_actions import (ContentType, RestActions)

baseURL = lambda: os.environ["rest_protocol"].strip() + "://" + os.getenv("apiBaseURL").strip()


class Content:
    header = ContentType.JSON

    class Url:
        get_url = lambda: baseURL() + "/server"


class LocalRestAPI:

    def get_request():
        RestActions.add_headers(Content.header).get(Content.Url.get_url())
        text = RestActions.response.text
        assert text != None, "No response from server"
