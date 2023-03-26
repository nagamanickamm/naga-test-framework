import xmltodict
import json
from xml.dom import minidom


class XMLUtils:

    xml_root: minidom.Document
    current_node: minidom.Element

    def get_xml_string():
        """Convert XML document to pretty xml string
        Returns:
            str: pretty xml
        """
        return XMLUtils.xml_root.toprettyxml(indent="\t")

    def create_root_xml():
        """create root xml node
        """
        XMLUtils.xml_root = minidom.Document()

    def create_node(parent: minidom.Element, tag_name: str, attributes: dict = None, text: str = None, namespace: tuple | list = None):
        """create new node and append to given parent node

        Args:
            parent (minidom.Element): parent node
            tag_name (str): new node name
            attributes (dict, optional): xml attributes for new node. Defaults to None.
            text (str, optional): xml text for new node . Defaults to None.
            namespace (tuple, optional): namespace if any. Defaults to None.

        Returns:
            minidom.Document: new node
        """
        dom = minidom.Document()
        node = dom.createElement(tag_name)
        parent.appendChild(node)
        if attributes is not None:
            for key, value in attributes.items():
                node.setAttribute(key, value)
        if text is not None:
            text_node = dom.createTextNode(text)
            node.appendChild(text_node)
        if namespace is not None:
            if type(namespace) == list:
                for ns in namespace:
                    node.setAttributeNS(*ns)
            else:
                node.setAttributeNS(*namespace)
        XMLUtils.current_node = node
        return node

    def parse_xml(xml_string: str):
        """Parse XML 

        Args:
            result (str): XML string

        Returns:
            JSON/Dict: Parsed XML in JSON format
        """
        parseXml = xmltodict.parse(xml_string)
        parseXml = json.dumps(parseXml)
        parseXml = json.loads(parseXml)
        return parseXml
