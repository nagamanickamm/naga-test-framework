from getgauge.python import step
from test_suite.fixtures.hooks import Hooks

from naga.test.framework.utils.core import *
from naga.test.framework.utils.data_store import data


@step("Got the result <matched>")
def i_get_the_result(matched):
    matched = CommonUtils.to_bool(matched)
    CommonUtils.assert_equals(matched, data.scenario.found_match, "Match not expected")


@step("Search all <list> items matching in <text>")
def i_search_all_items_matching_in(list_item, text):
    list_item = list_item.split(',')
    data.scenario.found_match = ListUtils.is_all_present(text, list_item)


@step("Got the list <matched>")
def i_get_the_list(matched):
    matched = CommonUtils.to_bool(matched)
    CommonUtils.assert_equals(matched, len(data.scenario.found_list) > 0, "Match not expected")


@step("Search any <list> items matching in <text>")
def i_search_any_items_matching_in(list_item, text):
    list_item = list_item.split(',')
    data.scenario.found_match = ListUtils.is_any_present(text, list_item)


@step("Search all <list> items matching the <text>")
def i_search_all_items_matching(list_item: str, text):
    list_item = list_item.split(',')
    data.scenario.found_list = ListUtils.contains_partial_text(list_item, text)
