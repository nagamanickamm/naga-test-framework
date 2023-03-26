import os

from getgauge.python import step
from test_suite.fixtures.hooks import Hooks

from naga.test.framework.utils.core import *
from naga.test.framework.utils.data_store import data


@step("Read <scenario> with <path>")
def read_with(scenario, path):
    file_path = os.environ["current_working_dir"] + path
    data.scenario.read_scenario = FileUtils.get_scenario_in_csv('scenario', scenario, file_path)


@step("Validate configuration file")
def validate_configuration_file():
    CommonUtils.assertion(data.scenario.user == "neon", "user value not matching", "neon", data.scenario.user)


@step("Read config file <path>")
def read_config_file(path):
    file_path = os.environ["current_working_dir"] + path
    data.scenario.user = FileUtils.search_config_file(file_path, "bitbucket.org", "User")


@step("Each <scenario> row should be a dictionary")
def validate_scenario_data(scenario):
    if scenario == 'scenario1':
        CommonUtils.assert_equals({'employee_name': 'fred', 'department': 'engineering'}, data.scenario.read_scenario)
    elif scenario == 'scenario2':
        CommonUtils.assert_equals({'employee_name': 'barry', 'department': 'mechanic'}, data.scenario.read_scenario)


@step("Validate output of tuple")
def validate_output_of_tuple():
    output = ('', None, ' ')
    output_type = (data.scenario.get_tuple) == output
    CommonUtils.assertion(output_type, "incorrect tuple", output, str(data.scenario.get_tuple))


@step("Returned the working directory path")
def returned_the_working_directory_path():
    CommonUtils.assertion(os.path.exists(data.scenario.cwd), "Path did not exist", "Valid path to features", data.scenario.cwd)
