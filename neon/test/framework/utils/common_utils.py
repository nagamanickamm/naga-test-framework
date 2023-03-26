import base64
import csv
import gzip
import math
import random
import socket
import string
from random import choice

from naga.test.framework.utils.report_utils import ReportUtils


class CommonUtils:

    def compress(request):
        return gzip.compress(bytes(request))

    def decompress(request):
        return gzip.decompress(request)

    def base64_encode(message):
        return base64.b64encode(message)

    def base64_decode(message):
        return base64.b64decode(message)

    def decode(message):
        return message.decode("utf-8")

    def image_compare(image_location_1, image_location_2):
        im1 = base64.b64encode(open(image_location_1, "rb").read())
        im2 = base64.b64encode(open(image_location_2, "rb").read())
        return im1 == im2

    def generate_random_alphabets(prefix='', range_value=5):
        """Generate a random string in lower case"""
        letters = string.ascii_lowercase
        random_name = ''.join(random.choice(letters) for i in range(range_value))
        new_name = prefix + random_name
        return new_name

    def generate_random_number(digit):
        """Generate a random number for the given digit ex: 10 digit random number"""
        max = math.pow(10, int(digit))
        min = max / 10
        number = random.randint(min, max)
        return number

    def generate_random_float_number(min, max, round_off):
        """Generates a random float and  rounds it"""
        number = random.uniform(min, max)
        number = round(number, round_off)
        return number

    def random_int(min, max, exclude=[]):
        return random.choice([i for i in range(min, max) if i not in exclude])

    def assert_equals(expected, actual, message=None):
        if message == None:
            message = f'''
            ---- Expected: {expected} 
            ---- Actual: {actual}
            '''
        else:
            message = f'''
            ---- Expected: {expected} 
            ---- Actual: {actual}
            ---- Msg: {message}
            '''
        assert expected == actual, message

    def assertion(condition: bool, fail_reason: str, expected: str, actual: str):
        message = f'''
            ---- Expected: {expected} 
            ---- Actual: {actual}
            ---- Msg: {fail_reason}
            '''
        assert condition, message

    def to_bool(value):
        """convert string to boolean value"""
        if str(value).lower() in ("true", "1", 1):
            return True
        elif str(value).lower() in ("false", "0", 0):
            return False
        else:
            assert False, "Invalid Boolean format : " + str(value)

    def translate_word_to_python(input_value):
        if type(input_value) is str:
            input_value = input_value.lower()
            input = {'empty': '', 'null': None, 'space': ' '}
            if input_value in input:
                return input[input_value]
        return input_value

    def translate_dict_words_to_python(dict_obj):
        """Translate dictionary words to python"""
        for key in dict_obj:
            dict_obj[key] = CommonUtils.translate_word_to_python(dict_obj[key])
        return dict_obj

    def translate_tuple_words_to_python(tuple_obj):
        """Translate tuple words to python"""
        list_obj = []
        for obj in tuple_obj:
            list_obj.append(CommonUtils.translate_word_to_python(obj))
        return tuple(list_obj)

    def set_root(rootName='src'):
        import pathlib
        import sys
        path = str(pathlib.Path().resolve())
        root = path.split(rootName)[0]
        sys.path.insert(0, root)

    def get_current_ip_address():
        """Returns current / local IP address

        Returns:
            Str: IP Addr
        """
        ip_address = socket.gethostbyname(socket.gethostname())
        ReportUtils.log(ip_address)
        return ip_address

    def get_host_name():
        """Returns current / local Hostname

        Returns:
            Str: IP Hostname
        """
        host_name = socket.gethostname().strip()
        ReportUtils.log("Hostname---" + host_name)
        return host_name