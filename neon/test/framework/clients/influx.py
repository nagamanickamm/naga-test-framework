from contextlib import contextmanager

import greenlet
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxClient:

    influx_conn: InfluxDBClient
    user = {}
    user_id = None
    connected = False

    def __init__(self) -> None:
        pass

    def __get_user():
        try:
            return greenlet.getcurrent().minimal_ident + 1
        except Exception:
            return 0

    @contextmanager
    def get_instance(user_id=None):
        try:
            user_id = user_id or InfluxClient.__get_user()
            influx_client: InfluxClient
            influx_client = InfluxClient.user[user_id] \
                          = InfluxClient.user.get(user_id, InfluxClient())
            influx_client.user_id = user_id
            yield influx_client
        except Exception as error:
            assert False, error

    def get_user_id():
        with InfluxClient.get_instance() as influx_client:
            return influx_client.user_id

    def connect(url, token):
        with InfluxClient.get_instance() as influx_client:
            influx_client.influx_conn = InfluxDBClient(url=url, token=token)
            influx_client.connected = True

    def write(bucket, org, data, user_id=None):
        with InfluxClient.get_instance(user_id) as influx_client:
            if influx_client.connected:
                write_api = influx_client.influx_conn.write_api(write_options=SYNCHRONOUS)
                write_api.write(bucket, org, data)
                write_api.close()

    def disconnect():
        with InfluxClient.get_instance() as influx_client:
            if influx_client.connected:
                influx_client.influx_conn.close()
                influx_client.connected = False