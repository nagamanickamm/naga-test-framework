from getgauge.python import step
from test_suite.fixtures.hooks import Hooks

from naga.test.framework.utils.core import *
from naga.test.framework.utils.data_store import data


@step("Given Ventress details")
def given_ventress_details():
    data.spec.ns = {'vt': "http://www.w3.org/2001/XMLSchema-instance", "asajj": "http://IntelligentGaming/Asajj/v1.0"}

    data.spec.ventress_attr = {
        "vt:destination": "Ventress://10.255.200.7",
        "vt:type": "Request",
        "vt:label": "Meters.Occurrence",
        "vt:createdTime": "2022-10-10T12:05:26.185Z",
        "vt:source": "Ventress://8.4000",
        "vt:sentTime": "2022-10-10T12:05:26.185Z",
        "vt:messageId": "216",
        "vt:priority": "Normal"
    }

    data.spec.header_attr = {
        "vt:contentType": "Ventress",
        "vt:timeToBeReceived": "300",
        "vt:encoding": "XmlGzip",
        "vt:persist": "false",
        "vt:trace": "false",
        "vt:timeToReachQueue": "300",
        "vt:journal": "false",
        "vt:deadLetter": "false",
    }

    data.spec.encoded_text = "H4sIAAAAAAAAAJVUXW+CMBR991eQvittFUaIYBbNNpN9mIy97K3DGyWDgm0189"


@step("Create a ventress XML")
def create_a_ventress_xml():
    XMLUtils.create_root_xml()
    vent_node = XMLUtils.create_node(XMLUtils.xml_root, 'vt:Ventress', data.spec.ventress_attr, None, ('vt', "xmlns:vt", data.spec.ns['vt']))
    header_node = XMLUtils.create_node(vent_node, 'vt:Header', data.spec.header_attr)
    content_node = XMLUtils.create_node(header_node, 'vt:Content')
    compressed_node1 = XMLUtils.create_node(content_node, 'asajj:Compressed', None, data.spec.encoded_text,
                                            ("asajj", "xmlns:asajj", data.spec.ns['asajj']))
    compressed_node2 = XMLUtils.create_node(content_node, 'asajj:Compressed', None,
                                            str(data.spec.encoded_text) + "1", ("asajj", "xmlns:asajj", data.spec.ns['asajj']))


@step("Parse ventress XML string")
def parse_ventress_xml_string():
    data.scenario.parsed_xml = XMLUtils.parse_xml(XMLUtils.get_xml_string())


@step("Found the element <text_to_find>")
def found_the_element(text_to_find):
    json_out, found = JsonUtils.find_element(data.scenario.parsed_xml, text_to_find)
    CommonUtils.assert_equals(True, found, "Element not found: " + text_to_find)
    CommonUtils.assertion(type(json_out) in [dict, list], "Element is not dict/list : " + text_to_find, "dict/list", type(json_out))


@step("Not Found the element <text_to_find>")
def not_found_the_element(text_to_find):
    json_out, found = JsonUtils.find_element(data.scenario.parsed_xml, text_to_find)
    CommonUtils.assert_equals(False, found, "Element found: " + text_to_find)
    CommonUtils.assertion(json_out is None, "Element is not None : " + text_to_find, "None", type(json_out))
