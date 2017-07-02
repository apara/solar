import unittest
import json
from pprint import pprint


class TestJSON(unittest.TestCase):
    def skip_test_parse(self):
        with open('tests/test_json.txt') as data_file:
            data_stuff = data_file.read()
            data = json.loads(data_stuff)

        pprint(data)
        result = data["result"]
        pprint(result)
        print("There are {} devices".format(len(data["devices"])))

        for device in data["devices"]:
            print("Serial: {}".format(device['SERIAL']))



