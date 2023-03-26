from getgauge.python import step

from naga.test.framework.utils.core import *
from naga.test.framework.utils.data_store import data


@step("Create password for Customer ID <3088> and balance <0>")
def create_password_for_customer_id_and_balance(cust_id, balance):
    data.scenario.password = cust_id + str(len(cust_id))
    data.scenario.balance = balance


@step("Encrypted value is <kD4mFZSMmh8snLKy321SAw==>")
def encrypted_value_is(expected_value):
    encrypted_value = Encryption.encrypt_with_password(data.scenario.balance, data.scenario.password)
    CommonUtils.assert_equals(expected_value, encrypted_value)
