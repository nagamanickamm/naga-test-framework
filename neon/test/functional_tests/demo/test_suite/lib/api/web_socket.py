import os
import pathlib
import sys

from naga.test.framework.utils.report_utils import ReportUtils

root = str(pathlib.Path().resolve().parents[0])
sys.path.insert(0, root)

from naga.test.framework.actions.api.websocket_actions import WebsocketActions

baseURL = lambda: os.environ["ws_protocol"].strip() + "://" + os.getenv("webSocketUrl").strip()


class Content:

    class Files:
        folder = os.getcwd() if os.getenv("demo_path") is None else os.getenv("demo_path")


class WebSocket_Demo:

    def connect_to_socket():
        WebsocketActions.connect(baseURL())
        ReportUtils.log("Connected")

    def send_message(message):
        ReportUtils.log("Sending ," + message)
        WebsocketActions.send(message)

    def receive_websocket_response(timeout):
        ReportUtils.log("Receiving...")
        result = WebsocketActions.receive(timeout)
        ReportUtils.log("Received '%s'" % result)

    def close():
        WebsocketActions.close()
