import json
import logging
import shutil
import time
from contextlib import contextmanager

import greenlet
import requests
import urllib3

from naga.test.framework.utils.data_store import data
from naga.test.framework.utils.json_utils import JsonUtils

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ContentType:
    JSON = {"Content-Type": "application/json"}
    XML = {"Content-Type": "application/xml"}
    TXT_HTML = {"Content-Type": "text/html"}
    IMAGE = {"Content-Type": "image/jpeg"}


class RestActions:
    headers = None
    body = None
    data = None
    response = None
    download_file = None
    statusCode: int = None
    user = {}

    def __get_user():
        try:
            return greenlet.getcurrent().minimal_ident + 1
        except Exception:
            return 0

    @contextmanager
    def get_instance():
        try:
            rest_actions: RestActions
            rest_actions = RestActions.user[RestActions.__get_user()] \
                         = RestActions.user.get(RestActions.__get_user(), RestActions())
            yield rest_actions
        except Exception as error:
            assert False, error

    def get_response():
        response = None
        with RestActions.get_instance() as rest_action:
            response = rest_action.response
        return response

    def checkStatus(code):
        with RestActions.get_instance() as rest_action:
            rest_action.statusCode = rest_action.response.status_code
            code = int(code) if type(code) != int else code
            error = f'''Status code 
                        Expected: {code} \n
                        Actual : {rest_action.statusCode}\n
                        --  {rest_action.response.reason} \n
                        --  {rest_action.response.text}\n
                        ---  {rest_action.response.request.url}\n
                        ---  {rest_action.response.request.body}'''
            assert rest_action.statusCode == code, error

    def add_headers(header_dict=None):
        with RestActions.get_instance() as rest_action:
            if header_dict == None:
                rest_action.headers = None
                return rest_action.Methods
            else:
                rest_action.headers = JsonUtils.parse_json(header_dict)
            return rest_action.Methods

    class Methods:

        def body(value):
            with RestActions.get_instance() as rest_action:
                rest_action.body = value
                rest_action.data = None
                return rest_action.Methods

        def data(value):
            with RestActions.get_instance() as rest_action:
                rest_action.body = None
                rest_action.data = value
                return rest_action.Methods

        def get(url, save_file=None, **kwargs):
            """Get Request

            Args:
                url (_type_): _description_
                save_file (_type_, optional): . Defaults to None
                get(
                url: str | bytes,
                params: _Params | None = ...,
                *,
                data: _Data | None = ...,
                headers: _HeadersMapping | None = ...,
                cookies: RequestsCookieJar | _TextMapping | None = ...,
                files: _Files | None = ...,
                auth: _Auth | None = ...,
                timeout: _Timeout | None = ...,
                allow_redirects: bool = ...,
                proxies: _TextMapping | None = ...,
                hooks: _HooksInput | None = ...,
                stream: bool | None = ...,
                verify: _Verify | None = ...,
                cert: _Cert | None = ...,
                json: Incomplete | None = ...
                ) -> Response
            """
            with RestActions.get_instance() as rest_action:
                if save_file != None:
                    rest_action.response = requests.get(url, headers=rest_action.headers, verify=False, stream=True, **kwargs)
                    with open(save_file, 'wb') as out_file:
                        shutil.copyfileobj(rest_action.response.raw, out_file)
                else:
                    rest_action.response = requests.get(url, headers=rest_action.headers, verify=False, **kwargs)

                RestActions.response = rest_action.response

        def post(url, **kwargs):
            """Send a Post request

            Args:
                url (_type_): Api End point
                **Kwargs - post(
                    url: str | bytes,
                    data: _Data | None = ...,
                    json: Incomplete | None = ...,
                    *,
                    params: _Params | None = ...,
                    headers: _HeadersMapping | None = ...,
                    cookies: RequestsCookieJar | _TextMapping | None = ...,
                    files: _Files | None = ...,
                    auth: _Auth | None = ...,
                    timeout: _Timeout | None = ...,
                    allow_redirects: bool = ...,
                    proxies: _TextMapping | None = ...,
                    hooks: _HooksInput | None = ...,
                    stream: bool | None = ...,
                    verify: _Verify | None = ...,
                    cert: _Cert | None = ...
                ) -> Response
            """
            with RestActions.get_instance() as rest_action:
                if type(rest_action.body) in [dict, json]:
                    rest_action.response = requests.post(url, headers=rest_action.headers, json=rest_action.body, verify=False, **kwargs)
                else:
                    rest_action.response = requests.post(url,
                                                         data=rest_action.data,
                                                         json=rest_action.body,
                                                         headers=rest_action.headers,
                                                         verify=False,
                                                         **kwargs)
                RestActions.response = rest_action.response
                data.scenario.input_json = rest_action.body

        def put(url, **kwargs):
            """Put request

            Args:
                url (_type_): Api End point,
                put(
                url: str | bytes,
                data: _Data | None = ...,
                *,
                params: _Params | None = ...,
                headers: _HeadersMapping | None = ...,
                cookies: RequestsCookieJar | _TextMapping | None = ...,
                files: _Files | None = ...,
                auth: _Auth | None = ...,
                timeout: _Timeout | None = ...,
                allow_redirects: bool = ...,
                proxies: _TextMapping | None = ...,
                hooks: _HooksInput | None = ...,
                stream: bool | None = ...,
                verify: _Verify | None = ...,
                cert: _Cert | None = ...,
                json: Incomplete | None = ...
                ) -> Response
            """
            with RestActions.get_instance() as rest_action:
                if type(rest_action.body) in [dict, json]:
                    rest_action.response = requests.put(url, headers=rest_action.headers, json=rest_action.body, verify=False, **kwargs)
                else:
                    rest_action.response = requests.put(url,
                                                        data=rest_action.data,
                                                        json=rest_action.body,
                                                        headers=rest_action.headers,
                                                        verify=False,
                                                        **kwargs)
                RestActions.response = rest_action.response
                data.scenario.input_json = rest_action.body

        def patch(url, **kwargs):
            """_Patch Request

            Args:
                url (_type_): Api End point
                patch(
                url: str | bytes,
                data: _Data | None = ...,
                *,
                params: _Params | None = ...,
                headers: _HeadersMapping | None = ...,
                cookies: RequestsCookieJar | _TextMapping | None = ...,
                files: _Files | None = ...,
                auth: _Auth | None = ...,
                timeout: _Timeout | None = ...,
                allow_redirects: bool = ...,
                proxies: _TextMapping | None = ...,
                hooks: _HooksInput | None = ...,
                stream: bool | None = ...,
                verify: _Verify | None = ...,
                cert: _Cert | None = ...,
                json: Incomplete | None = ...
            ) -> Response
            """
            with RestActions.get_instance() as rest_action:
                rest_action.response = requests.patch(url, json=rest_action.body, headers=rest_action.headers, verify=False, **kwargs)
                RestActions.response = rest_action.response

        def delete(url, **kwargs):
            """Delete Request

            Args:
                url (_type_): Api End point
                delete(
                url: str | bytes,
                *,
                params: _Params | None = ...,
                data: _Data | None = ...,
                headers: _HeadersMapping | None = ...,
                cookies: RequestsCookieJar | _TextMapping | None = ...,
                files: _Files | None = ...,
                auth: _Auth | None = ...,
                timeout: _Timeout | None = ...,
                allow_redirects: bool = ...,
                proxies: _TextMapping | None = ...,
                hooks: _HooksInput | None = ...,
                stream: bool | None = ...,
                verify: _Verify | None = ...,
                cert: _Cert | None = ...,
                json: Incomplete | None = ...
            ) -> Response
            """
            with RestActions.get_instance() as rest_action:
                rest_action.response = requests.delete(url, headers=rest_action.headers, verify=False, **kwargs)
                RestActions.response = rest_action.response
