import os

from getgauge.python import step

from naga.test.framework.actions.api.rest_actions import (ContentType, RestActions)
from naga.test.framework.utils.data_store import data
from naga.test.framework.utils.json_utils import JsonUtils


class Reqres_Content:

    class Url:
        reqres_url = os.environ['apiBaseURL'] + "api/users"

    class Files:
        registration_json_path = os.environ['Current_Working_Dir'] + '\\test_suite\\resources\\json_files\\reqres_post.json'
        registration_schema_path = os.environ['Current_Working_Dir'] + '\\test_suite\\resources\\json_schema\\reqres_post.json'


class Reqres_API:

    def register_employee(name, job):
        json_data = JsonUtils.readJSONFile(Reqres_Content.Files.registration_json_path)
        json_data['name'] = name
        json_data['job'] = job
        RestActions.add_headers(ContentType.JSON).body(json_data).post(Reqres_Content.Url.reqres_url)
        data.scenario.input_json = json_data

    def verify_registration():
        schema_file_path = Reqres_Content.Files.registration_schema_path
        RestActions.checkStatus(201)
        schema = JsonUtils.readJSONFile(schema_file_path)
        JsonUtils.validate_schema(RestActions.response.json(), schema)
