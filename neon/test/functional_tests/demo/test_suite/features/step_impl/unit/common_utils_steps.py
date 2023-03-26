import re

from getgauge.python import step
from test_suite.fixtures.hooks import Hooks

from naga.test.framework.utils.common_utils import CommonUtils
from naga.test.framework.utils.data_store import data
from naga.test.framework.utils.file_utils import FileUtils


@step("Validate random letter")
def validate_random_letter():
    data.scenario.random_letter = CommonUtils.generate_random_alphabets(prefix='', range_value=5)
    return_type = type(data.scenario.random_letter)
    CommonUtils.assertion(return_type == str, "Return type is not a string", str(data.scenario.random_letter), return_type)


@step("Validate letter case")
def validate_letter_case():
    return_case = str.lower(data.scenario.random_letter)
    CommonUtils.assertion(return_case, "String is not lower case", str.lower(data.scenario.random_letter), return_case)


@step("Generate random number")
def generate_random_number():
    data.scenario.random_number = CommonUtils.generate_random_number(digit=10)


@step("Validate random number")
def validate_random_number():
    return_type = type(data.scenario.random_number)
    CommonUtils.assertion(return_type == int, "Return type is not integer", "int", return_type)
    return_range = range(data.scenario.random_number)
    CommonUtils.assertion(return_range, "Number is not within range", 10, return_range)


@step("Generate random float number")
def generate_random_float_number():
    data.scenario.random_float = CommonUtils.generate_random_float_number(0, 9, 2)


@step("Validate random float number")
def validate_random_float_number():
    return_type = type(data.scenario.random_float)
    text = str(data.scenario.random_float)
    match1 = re.match(r'^\d\.\d{1}$', text)
    match2 = re.match(r'^\d\.\d{2}$', text)
    CommonUtils.assertion(match1 or match2, "Return value not in expected format", "d.dd", data.scenario.random_float)
    CommonUtils.assertion(return_type == float, "Return type is not a float", "float", return_type)


@step("Convert str <input> to bool value")
def generate_bool_value(input):
    data.scenario.bool_casing = (CommonUtils.to_bool(input))


@step("Validate bool value <output>")
def validate_bool_casing(output):
    result = str(output) == str(data.scenario.bool_casing)
    CommonUtils.assertion(result, "incorrect value", output, data.scenario.bool_casing)
    output_type = type(data.scenario.bool_casing) == bool
    CommonUtils.assertion(output_type, "incorrect type", bool, type(data.scenario.bool_casing))


@step("Convert int <input> to bool value")
def generate_bool_value(input):
    data.scenario.bool_casing = (CommonUtils.to_bool(int(input)))


@step("Feed dictionary for translation")
def get_input_of_dict():
    input = {'empty': 'empty', 'null': 'null', 'space': 'space'}
    data.scenario.get_dict = CommonUtils.translate_dict_words_to_python(input)


@step("Validate output of dictionary")
def validate_of_dictionary():
    output = {'empty': '', 'null': None, 'space': ' '}
    output_type = (data.scenario.get_dict) == output
    CommonUtils.assertion(output_type, "incorrect dictionary", output, str(data.scenario.get_dict))


@step("Feed tuple for translation")
def get_of_tuple():
    input = ('empty', 'null', 'space')
    data.scenario.get_tuple = (CommonUtils.translate_tuple_words_to_python(input))


@step("Get current working directory")
def get_current_working_directory():
    data.scenario.cwd = FileUtils.get_path_current_file('feature', __file__)
