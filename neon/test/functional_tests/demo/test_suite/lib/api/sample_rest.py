import os

from naga.test.framework.actions.api.rest_actions import (ContentType, RestActions)
from naga.test.framework.utils.json_utils import JsonUtils

baseURL = lambda: os.environ["rest_protocol"].strip() + "://" + os.getenv("apiBaseURL").strip()


class Content:
    header = ContentType.JSON

    class Url:
        get_url = lambda: baseURL() + "/api/todos/1"
        post_url = lambda: baseURL() + "/api/todos"

    class Files:
        folder = os.getcwd() if os.getenv("demo_path") is None else os.getenv("demo_path")
        post_json = folder + "/test_suite/resources/json_files/post.json"


class SampleRestAPI:

    def get_request():
        RestActions.add_headers(ContentType.JSON).get(Content.Url.get_url())
        json_data = RestActions.response.json()
        return json_data

    def post_request():
        json = JsonUtils.readJSONFile(Content.Files.post_json)
        RestActions.add_headers(ContentType.JSON).body(json).post(Content.Url.post_url())
        json_data = RestActions.response.json()
        return json_data
