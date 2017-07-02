import sys
import pcapy
from configuration import Configuration
from impacket.ImpactDecoder import *
from line import LinesFactory, Line, DbLineManager
from utils import LogMixin


class DataCapture(LogMixin):
    def __init__(self, config_file_names):
        # Create configuration
        #
        self.__config = Configuration(config_file_names)

        # Create parser for lines
        #
        self.__lines_factory = LinesFactory()

        # Create database manager
        #
        self.__dbLineManager = DbLineManager(self.__config)

    def run(self):
        
        return 0

    def __insert_results(self, data):
        # Create lines for results
        #
        results = self.__lines_factory.build(data)

        # Insert into database
        #
        for l in results:
            self.__dbLineManager.insert(l)


def main():

    ifs = pcapy.findalldevs()
    print(ifs)

    import logging
    logging.basicConfig(
        # filename='output.txt',
        format='%(asctime)s|%(levelname)s|%(message)s|',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )
    
    return DataCapture(['./solar.conf', 'conf/solar.conf', '/etc/solar.conf']).run()


if __name__ == "__main__":
    sys.exit(main())
