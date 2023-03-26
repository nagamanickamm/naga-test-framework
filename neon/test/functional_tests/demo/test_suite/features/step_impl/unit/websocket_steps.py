import os

from getgauge.python import step

from naga.test.framework.actions.api.websocket_actions import WebsocketActions
from naga.test.framework.utils.common_utils import CommonUtils


@step("Connect to websocket <host> <port>")
def connect_to_websocket(host, port):
    # del os.environ['subProtocol']
    WebsocketActions.connect(f"ws://{host}:{port}")


@step("Send message <msg>")
def send_message(msg):
    WebsocketActions.send(msg)


@step("Receive message <expected_msg>")
def receive_message(expected_msg):
    msg = WebsocketActions.read()
    CommonUtils.assert_equals(expected_msg, msg)
