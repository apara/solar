import sys
import time
from httplib import HTTPConnection, OK
from configuration import Configuration
from line import LinesFactory, DbLineManager, Line130
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
            if data is not None:
                total_inserts = self.__insert_results(data)
                action = 'Processed ({} rows)'.format(total_inserts)
            else:
                action = 'Skipped, unable to read data'

            # Log info processing message
            #
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

        # Total insert counter
        #
        total_inserts = 0

        # Insert into database
        #
        for l in results:
            if self.__dbLineManager.insert(l):
                total_inserts += 1

        # Return total inserts
        #
        return total_inserts

    @property
    def db_line_manager(self):
        return self.__dbLineManager


def main():
    import logging
    logging.basicConfig(
        # filename='output.txt',
        format='%(asctime)s|%(levelname)s|%(message)s|',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )
    
    return DataCapture(['./solar.conf', 'conf/solar.conf', '/etc/solar.conf']).run()


def oldmain():
    import json
    dc = DataCapture(['./solar.conf', 'conf/solar.conf', '/etc/solar.conf'])

    data_130 = '{"ISDETAIL":"1","SERIAL":"414051706011633","TYPE":"SOLARBRIDGE","STATE":"working","STATEDESCR":"Working","MODEL":"AC_Module_Type_C","DESCR":"Inverter 414051706011633","DEVICE_TYPE":"Inverter","SWVER":"951007408","PORT":"","MOD_SN":"","NMPLT_SKU":"","DATATIME":"2017,07,02,03,05,14","ltea_3phsum_kwh":"58.7856","p_3phsum_kw":"0","vln_3phavg_v":"249.2725","i_3phsum_a":"0","p_mpptsum_kw":"0","v_mppt1_v":"55.5546","i_mppt1_a":"-0.0333","t_htsnk_degc":"26.75","freq_hz":"60.0096","CURTIME":"2017,07,02,03,12,10"}'
    data_json_130 = json.loads(data_130)

    line = Line130(device=data_json_130)

    dc.db_line_manager.insert(line)


if __name__ == "__main__":
    sys.exit(main())
