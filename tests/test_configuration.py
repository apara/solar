import unittest
from configuration import Configuration, ConfigurationFileNotFound


class TestConfiguration(unittest.TestCase):
    def test_configuration(self):
        configuration = Configuration('tests/test_configuration.txt')
        self.assertEqual('A', configuration['propertyA'])
        self.assertEqual('B', configuration['propertyB'])
        self.assertEqual('204.194.111.66', configuration.collector_ip_address)

        try:
            configuration['invalidProperty']
            self.assertTrue(False)
        except KeyError:
            pass

    def test_invalid_configuration_name(self):
        try:
            configuration = Configuration('foo')
            self.assertTrue(False)
        except ConfigurationFileNotFound:
            pass

