from configparser import ConfigParser


class ConfigurationFileNotFound(Exception):
    def __init__(self, file_names):
        super(ConfigurationFileNotFound, self).__init__()
        self.__file_names = file_names

    def __str__(self):
        return repr(self.__file_names)


class Configuration:

    def __init__(self, file_names):
        # Read the configuration
        #
        self.__config = self.__read_configuration__(file_names)

    @staticmethod
    def __read_configuration__(file_names):
        # Create config object
        #
        config = ConfigParser()
        config.read(file_names)

        # if we were not able to read any configuration files, then raise exception
        #
        if len(config.sections()) == 0:
            raise ConfigurationFileNotFound("Could not find configuration file in the following paths: %s" % file_names)

        # Return the read configuration
        #
        return config["defaults"]

    # Return address of the collector that we should be watching, 204.194.111.66 for example for
    # collector.sunpowermonitor.com
    #
    @property
    def collector_ip_address(self):
        return self['collector_ip_address']

    # Return the network interface that we are going to monitor
    #
    @property
    def network_interface(self):
        return self['network_interface']


    def __getitem__(self, property_name):
        # Get the value
        #
        value = self.__config[property_name]

        # Return the value of the property
        #
        return value





