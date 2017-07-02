import sys
import time
from httplib import HTTPConnection, OK
from configuration import Configuration
from line import LinesFactory, DbLineManager
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
        # Init
        #
        run = 0
        last_data = ''

        # Run while we can
        #
        while True:
            # Increment run
            run += 1

            # Read data
            #
            data = self.__read_data()

            # If we got something, insert it
            #
            if (data is not None) and (data != last_data):
                last_data = data
                self.__insert_results(data)
                action = 'Processed'
            else:
                action = 'Skipped'

            self.logger.info("Run: %s, Length: %s, Action: %s", run, len(data), action)

            # Sleep for a bit
            #
            time.sleep(self.__config.pull_frequency_seconds)

    def __read_data(self):
        # Initialize connection
        #
        connection = None

        # Read the data from connection
        #
        try:
            # Create connection
            #
            connection = HTTPConnection(self.__config.devices_host)

            # Execute the request
            #
            connection.request('GET', self.__config.devices_url)

            # Get the status
            #
            response = connection.getresponse()

            # If the response is good, then proceed
            #
            return response.read() if response.status == OK else None

        finally:
            if connection is not None:
                connection.close()

    def __insert_results(self, data):
        # Create lines for results
        #
        results = self.__lines_factory.build(data)

        # Insert into database
        #
        for l in results:
            self.__dbLineManager.insert(l)


def main():
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
