import logging
import os
import ssl
import threading
from contextlib import contextmanager

import greenlet
import websocket


class WebsocketActions:
    ws: websocket
    message = ''
    websocket.enableTrace(False)
    user = {}
    message_list = []
    id = 0
    receiver_thread = None
    external_func = None
    url = None

    def __get_user(id):
        if id is None:
            try:
                return greenlet.getcurrent().minimal_ident + 1
            except Exception:
                return 0
        else:
            return id

    @contextmanager
    def get_instance(uid=None):
        try:
            user_id = WebsocketActions.__get_user(uid)
            websocket_actions: WebsocketActions
            websocket_actions = WebsocketActions.user[user_id] \
                              = WebsocketActions.user.get(user_id, WebsocketActions())
            websocket_actions.id = user_id
            yield websocket_actions
        except TimeoutError as error:
            raise TimeoutError(str(error))
        except Exception as error:
            assert False, error

    def connect(webSocketUrl):
        with WebsocketActions.get_instance() as socket_action:
            socket_action.url = webSocketUrl
            if os.getenv('subProtocol', None) is not None:
                socket_action.ws = websocket.create_connection(webSocketUrl,
                                                               subprotocols=[os.environ['subProtocol']],
                                                               sslopt={"cert_reqs": ssl.CERT_NONE})
            else:
                socket_action.ws = websocket.create_connection(webSocketUrl)
            socket_action.receiver_thread = threading.Thread(target=WebsocketActions.receive, args=(socket_action.id,))
            socket_action.receiver_thread.start()

    def send(message):
        with WebsocketActions.get_instance() as socket_action:
            if not socket_action.ws.connected:
                socket_action.connect(socket_action.url)
            socket_action.message = message
            socket_action.ws.send(message)

    # ---------------------------- Receive from websocket---------------------------------------
    def receive(id):
        with WebsocketActions.get_instance(id) as socket_action:
            while socket_action.ws.connected:
                try:
                    message = socket_action.ws.recv()
                    if socket_action.external_func is not None:
                        socket_action.external_func(message)
                    else:
                        socket_action.message_list.append(message)
                except Exception as e:
                    logging.ERROR(e)

    def register_consumer(external_func):
        with WebsocketActions.get_instance() as socket_action:
            socket_action.external_func = external_func

    def read():
        with WebsocketActions.get_instance() as socket_action:
            if len(socket_action.message_list) > 0:
                return socket_action.message_list.pop(0)
            else:
                return None

    # ---------------------------- Close websocket---------------------------------------
    def close():
        with WebsocketActions.get_instance() as socket_action:
            if WebsocketActions.is_open():
                socket_action.ws.close()

    def is_open():
        is_open = False
        with WebsocketActions.get_instance() as socket_action:
            try:
                is_open = socket_action.ws.connected
            except:
                is_open = False
        return is_open
