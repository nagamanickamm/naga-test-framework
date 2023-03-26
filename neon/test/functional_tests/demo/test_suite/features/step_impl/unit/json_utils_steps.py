import os

from getgauge.python import step
from test_suite.fixtures.hooks import Hooks

from naga.test.framework.utils.core import *
from naga.test.framework.utils.data_store import data


@step("Setup two JSON objects")
def setup_two_json_objects():
    data.scenario.json1 = {
        'name': 'man',
        'time': '2022-10-03T16:17:59.926Z',
        'dob': '2021-02-01',
        'float': 20.50000000,
        'int': 555,
        'bool': False,
        'extra': 'test'
    }
    data.scenario.json2 = {'name': 'man', 'time': '2022-10-03', 'dob': '2021-02-01T10:60:55', 'float': 20.5, 'int': 555, 'bool': False}


@step("Compare two JSON objects")
def compare_two_json_objects():
    JsonUtils.compare_two_json_values(data.scenario.json1, data.scenario.json2)


@step("Provided a inline table data <table>")
def provided_a_inline_table_data(table):
    data.scenario.table = table


@step("Read table as Json array")
def read_table_as_json_array():
    json_array = JsonUtils.convert_table_to_json_array(data.scenario.table)
    CommonUtils.assert_equals('data11', json_array[0]['Header1'], 'Data not present in json')
    CommonUtils.assert_equals('data22', json_array[1]['Header2'], 'Data not present in json')


@step("Provided 2 Json array of different json order")
def provided_2_json_array_of_different_json_order():
    data.scenario.json_array1 = [{"name": "elon", "age": 50}, {"name": "musk", "age": 20}]
    data.scenario.json_array2 = [{"name": "musk", "age": 20}, {"name": "elon", "age": 50}]


@step("Compare given Json arrays")
def compare_given_json_arrays():
    JsonUtils.compare_json_array(data.scenario.json_array1, data.scenario.json_array2)


@step("Provided json model and input from csv <scenario> with <csv_json>")
def provided_json_model_and_input_from_csv_with(scenario, csv_json):
    csv_file = os.getcwd() + csv_json
    data.scenario.input_json = FileUtils.get_scenario_in_csv('scenario', scenario, csv_file)


@step("Insert values into json model")
def insert_values_into_json_model():
    json_body = {'name': None, 'job': None, 'extra': 'empty', 'number': 0, 'Empty': '', 'flag': False}
    json_body = JsonUtils.insert_json_values(json_body, data.scenario.input_json)

    expected_body = {'name': 'morpheus', 'job': 'leader', 'extra': 'empty', 'number': 0.01, 'Empty': None, 'flag': True}
    CommonUtils.assert_equals(expected_body, json_body, "Json insertion failed")


@step("Given Response Json")
def given_response_json_and_mapping_json():
    data.scenario.response = {'PropertyID': '0'}


@step("Map response json and validate output")
def map_response_json_and_validate_output():
    response = JsonUtils.field_mapping(data.scenario.response, data.scenario.mapping_json)
    CommonUtils.assert_equals({'VenueID': '0'}, response)


@step("Set mapping the columns from response to database columns")
def map_the_columns_from_response_to_database_columns():
    data.scenario.mapping_json = {'PropertyID': 'VenueID'}


@step("Find dictionary key by value <search>")
def find_dictionary_key_by_value(search):
    dict_item = {'one': 1, 'two': 2, 'two_2': 2}
    data.scenario.return_key = JsonUtils.get_key_by_value(dict_item, int(search))


@step("Correct Key is <returned>")
def correct_key_is(returned):
    CommonUtils.assert_equals(returned, data.scenario.return_key)


@step("Convert dictionary to class")
def create_dictionary():
    dict_obj = {'name': 'mark', 'address': 'ol1 2xp', 'preference': True, 'id': 10}
    data.scenario.grab_dict = (JsonUtils.convert_dict_to_class(dict_obj))


@step("Dictionary should be converted to class with correct data types")
def validate_class():
    class_obj = data.scenario.grab_dict
    CommonUtils.assert_equals('mark', class_obj.name)
    CommonUtils.assert_equals('ol1 2xp', class_obj.address)
    CommonUtils.assert_equals(True, class_obj.preference)
    CommonUtils.assert_equals(10, class_obj.id)
