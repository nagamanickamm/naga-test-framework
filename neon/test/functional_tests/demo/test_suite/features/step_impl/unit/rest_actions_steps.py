import os

from getgauge.python import step
from test_suite.fixtures.hooks import Hooks

from naga.test.framework.actions.api.rest_actions import (ContentType, RestActions)
from naga.test.framework.utils.core import *


@step("Download Image <inputfile>")
def get_image(inputfile):
    url = 'http://localhost:5000/image/' + inputfile
    path = os.environ["Current_Working_Dir"] + '\\test_suite\\resources\\images\\download\\output.jpg'
    RestActions.add_headers(ContentType.IMAGE).get(url, path)


@step("Compare image <inputfile> with <outputfile> and expect <result>")
def compare_image_with(inputfile, outputfile, expected_result):
    input_path = os.environ["Current_Working_Dir"] + '\\test_suite\\resources\\images\\'
    download_path = os.environ["Current_Working_Dir"] + '\\test_suite\\resources\\images\\download\\'
    actual_result = CommonUtils.image_compare(input_path + inputfile, download_path + outputfile)
    expected_result = CommonUtils.to_bool(expected_result)
    CommonUtils.assert_equals(expected_result, actual_result)


@step("Upload Image file <file>")
def upload_image_file(file):
    path = os.environ["Current_Working_Dir"] + '\\test_suite\\resources\\images\\'
    file = {'file': open(path + file, 'rb')}

    os.makedirs(path + "uploaded", exist_ok=True)
    body = {"path": path + "uploaded\\"}
    RestActions.add_headers(None).data(body).post('http://localhost:5000/uploader', files=file)


@step("Upload should be successful")
def upload_should_be_successful():
    RestActions.checkStatus(200)
    uploaded_file = os.environ["Current_Working_Dir"] + '\\test_suite\\resources\\images\\uploaded\\input.jpg'
    input_file = os.environ["Current_Working_Dir"] + '\\test_suite\\resources\\images\\input.jpg'
    actual_result = CommonUtils.image_compare(uploaded_file, input_file)
    os.remove(uploaded_file)
    CommonUtils.assert_equals(True, actual_result)
