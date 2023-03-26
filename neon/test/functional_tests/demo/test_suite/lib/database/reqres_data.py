from getgauge.python import step

from naga.test.framework.utils.data_store import data
from naga.test.framework.utils.db_utils import DBUtils
from naga.test.framework.utils.json_utils import JsonUtils


class Reqres_Data:

    def validate_registration_details():
        query_json = DBUtils.query_to_json('SELECT * from [reqres]')
        db_json_array = JsonUtils.parse_json(query_json)
        JsonUtils.compare_two_json_values(data.scenario.input_json, db_json_array[0])
