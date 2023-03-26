import os

from getgauge.python import step
from test_suite.fixtures.hooks import Hooks

from naga.test.framework.utils.core import *
from naga.test.framework.utils.data_store import data


@step("Create HTML files out of all spec file under given folder")
def create_html_files_out_of_all_spec_file_under_given_folder():
    get_root = os.getcwd().split('\\neon\\test')[0]
    spec_path = get_root + data.scenario.spec_path
    html_path = get_root + "\\features\\"
    if os.path.exists(html_path):
        FileUtils.remove_directory_tree(html_path)
    SpecHTMLUtils.convert_specs_html(spec_path, html_path)
    assert os.path.exists(html_path), "Features not created"


@step("Set spec folder path to <path>")
def set_spec_folder_path_to(path):
    data.scenario.spec_path = path
