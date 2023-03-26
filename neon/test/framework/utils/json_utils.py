import copy
import json

import jsonschema
from deepdiff import DeepDiff
from jsonschema import validate

from naga.test.framework.utils.common_utils import CommonUtils
from naga.test.framework.utils.regex_utils import RegEx
from naga.test.framework.utils.report_utils import ReportUtils


class JsonUtils:

    def readJSONFile(fileName):
        data = open(fileName)
        jsonData = json.load(data)
        return jsonData

    def format_json(json_data):
        return json.dumps(json_data)

    def parse_json(json_data):
        """Converts String to JSON

        Args:
            json_data (str): Json like string

        Returns:
            json: Json object
        """
        if type(json_data) in [dict, list]:
            json_data = json.dumps(json_data)
        parsed_json = json.loads(json_data)
        return parsed_json

    def validate_schema(json_data, json_schema):
        """Validate the Json contract

        Args:
            json_data (json): json_data to validate
            json_schema (json): json_schema to match
        """
        try:
            validate(instance=json_data, schema=json_schema)
        except jsonschema.exceptions.ValidationError as err:
            assert False, f"JSON schema is not matching : \n {err}"

    def check_schema(json_data, json_schema):
        """Validate the Json contract

        Args:
            json_data (json): json_data to validate
            json_schema (json): json_schema to match
        """
        match = True
        try:
            validate(instance=json_data, schema=json_schema)
        except jsonschema.exceptions.ValidationError as err:
            match = False

        return match

    def get_keys(json_data):
        """Get all keys from json

        Args:
            response (dict): json data

        Returns:
            list: list of key names ex: ['name','id']
        """
        return list(json_data.keys())

    def get_values(response):
        """Returns list of values from current dictionary

        Args:
            response (json): json data

        Returns:
            list: value list
        """
        return list(response.values())

    def normalize_json_values(json_data):
        """Normalize json values

        Args:
            json_data (_type_): example : {'one': [{'one': 'empty'}]}  /(or)/ {'one': 'empty'}
        """
        for key in json_data:
            if type(json_data[key]) == list:
                for item in json_data[key]:
                    JsonUtils.normalize_json_values(item)
            else:
                json_data[key] = CommonUtils.translate_word_to_python(json_data[key])

        return json_data

    def compare_json_array(expected_json, actual_json, ignore_order=True):
        """Perform deep compare between expected and actual json in a json array, where user can ignore the order of the json optionally

        Args:
            expected_json (list): expected json array list
            actual_json (list): actual json array list
            ignore_order (bool, optional): ignore order of json in the list, Defaults to True.
        """
        diff = DeepDiff(expected_json, actual_json, ignore_order=ignore_order)
        if diff != {}:
            assert False, "Expected and Actual array did not match {diff}"

    def compare_two_json_values(expected_json, actual_json):
        """Used to Validate JSON response values with JSON query response/DB output
        Note: This method skips the column name if not found in one of the two JSONs, also this function does not accept JSON array
        Parameters
        ----------
        expected_json : json object
            Should be an input json response from API/CSV
        actual_json : json object
            Should be an output json response from DB"""

        #Prepare JSON objects
        expected_json = JsonUtils.keys_lowercase(expected_json)
        actual_json = JsonUtils.keys_lowercase(actual_json)
        actual_json_keys = JsonUtils.get_keys(actual_json)
        expected_json_keys = JsonUtils.get_keys(expected_json)
        if len(set(expected_json_keys).difference(actual_json_keys)) > 0:
            ReportUtils.log(str(set(expected_json_keys).difference(actual_json_keys)), ReportUtils.level_info)

        #Compare excepted vs actual JSON object
        for column_name in expected_json:
            if column_name in actual_json_keys:
                if type(expected_json[column_name]) == str or type(actual_json[column_name]) == str:
                    expected = str(expected_json[column_name]).lower()
                    actual = str(actual_json[column_name]).lower()
                    # Normalize text
                    if RegEx.is_float(expected) or RegEx.is_float(actual):
                        result = float(expected) == float(actual)
                    elif RegEx.is_date(expected) or RegEx.is_date(actual):
                        result = expected[:10] == actual[:10]
                    else:
                        result = expected == actual
                else:
                    result = expected_json[column_name] == actual_json[column_name]

                CommonUtils.assertion(result, 'Values not matching for ' + column_name, expected_json[column_name], actual_json[column_name])

    def find_element(dict_json: dict, find):
        """Search for given element in nested json/dictionary

            Args:
                dicts (dict): nested dictionary object
                find (str): search text

            Returns:
                dict, bool: dictionary and find result
            """
        found = False
        for key, value in dict_json.items():
            if find in key:
                return value, True
            else:
                if type(value) == dict:
                    return_dict, found = JsonUtils.find_element(value, find)
                    if found:
                        return return_dict, found
        return None, found

    def convert_table_to_json_array(table_object):
        """Convert Gauge table object to Json Array
           table_object: table 
           return: Json Array
        """
        header = list(table_object._Table__headers)
        table_rows = list(table_object)
        json_array = []
        for each_row in table_rows:
            json_row = {}
            for index, each_cell in enumerate(each_row):
                json_row[f'{header[index]}'] = each_cell
            json_array.append(json_row)
        return json_array

    def insert_json_values(json_body, input_json):
        """This is used to update all values from input_json into given json body
        Parameters
        ----------
        json_body : json object
            Should be an json body
        input_json : json object
            Should be an input from csv in json format
        
        Returns updated json_body"""

        #Prepare JSON objects
        db_json_key_lists = JsonUtils.get_keys(input_json)
        # Compare two jsons and update if column name matches
        for column_name in json_body:
            if column_name in db_json_key_lists:
                if input_json[column_name].lower() in ['none', 'null']:
                    json_body[column_name] = CommonUtils.translate_word_to_python(input_json[column_name])
                elif (type(json_body[column_name]) in [float, int]) and (RegEx.is_float(input_json[column_name])):
                    json_body[column_name] = float(input_json[column_name])
                elif type(json_body[column_name]) is int:
                    json_body[column_name] = int(input_json[column_name])
                elif type(json_body[column_name]) is bool:
                    json_body[column_name] = CommonUtils.to_bool(input_json[column_name])
                else:
                    json_body[column_name] = CommonUtils.translate_word_to_python(input_json[column_name])
        return json_body

    def field_mapping(input_json: json, mapping_json: dict):
        """Map response column names to Database columns

        Args:
            input_json (json): Response JSON
            mapping_json (dict): Mapping Json 

        Returns:
            _type_: updated response json
        """
        for old, new in mapping_json.items():
            input_json[new] = input_json.pop(old)
        return input_json

    def split_json(input_json: dict, column_names: list):
        """Split given JSON into two, second JSON will be based on List of column names

        Args:
            input_json (dict): input json to split
            column_names (list): column names to extract from input json and form new json

        Returns:
            tuples: input_json, new_json
        """
        new_json: dict = {}
        main_json = copy.copy(input_json)
        for key, value in input_json.items():
            if key in column_names:
                new_json[key] = main_json.pop(key)

        return main_json, new_json

    def find_first_dictionary(input_json_array: list, search_column: str, search_value):
        """Query JSON array based on Key and Value and find matching json record within given array

        Args:
            input_json_array (dict): example: [{'name':'peter', 'id':2},{'name':'jord', 'id':2}]
            search_column (str): key to match, ex: search_column='id'
            search_value (any): value to match, ex: search_value = 2 

        Returns:
            dict: returns matched json record, ex: {'name':'jord', 'id':2}, if not matched returns None
        """
        return next((d for d in input_json_array if d[search_column] == search_value), None)

    def find_all_dictionary(input_json_array: list, search_column: str, search_value):
        """Query JSON array based on Key and Value and return all matching json records within given array

        Args:
            input_json_array (dict): example: [{'name':'peter', 'id':2},{'name':'jord', 'id':2}]
            search_column (str): key to match, ex: search_column='id'
            search_value (any): value to match, ex: search_value = 2 

        Returns:
            dict: returns matched json record, ex: {'name':'jord', 'id':2}
        """
        return (d for d in input_json_array if d[search_column] == search_value)

    def save_json(json_string, path):
        """Save JSON string to file

        Args:
            json_string (dict): JSON String
            path (Str): Path to output file
        """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(json_string, f, ensure_ascii=False, indent=4)

    def convert_dict_to_class(dict_obj):
        """Converts a JSON / Dictionary to Class object

        Args:
            dict_obj (dict): object to convert

        Returns:
            class: converted class instance
        """
        class_obj = type('class', (object,), dict_obj)
        return class_obj

    def remove_keys(list_to_remove, json_data):
        """Remove given keys from JSON

        Args:
            list_to_remove (list): list of keys to remove
            json_data (dict): from given json

        Returns:
            json/dict: json_data
        """
        for rem in list_to_remove:
            json_data.pop(rem)
        return json_data

    def keys_lowercase(json_data):
        """Convert all keys in the dictionary to lower case

        Args:
            json_data (): Json object

        Returns:
            dict: output json
        """
        new_dict = dict((k.lower(), v) for k, v in json_data.items())
        return new_dict

    def get_key_by_value(dictionary, search_value):
        """Search key by value in dictionary

        Args:
            dictionary (dict): dictionary item
            search_value (any): search text

        Returns:
            _type_: str , returns key text
        """
        for key, value in dictionary.items():
            if value == search_value:
                return key