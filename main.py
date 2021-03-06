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

        # Create a data buffer
        #
        self.__buffer = ''

        # Create database manager
        #
        self.__dbLineManager = DbLineManager(self.__config)

    def run(self):
        # Open live capture onto the network interface in promiscious mode
        #
        pc = pcapy.open_live(self.__config.network_interface, 65535, True, 1000)

        # Configure the filter
        #
        pc.setfilter("tcp && ip && dst net %s && dst port 80" % '204.194.111.66')

        # Begin packet capture loop
        #
        pc.loop(-1, self.__receive_packets)  # capture packets

        return 0

    def __receive_packets(self, hdr, data):
        # Decode the data
        #
        packet = EthDecoder().decode(data)
        ip = packet.child()
        tcp = ip.child()
        data = tcp.get_data_as_string()

        # print("DATA (%i): [%s]" % (len(data), data))

        # If this is a blank line, then we got the entire request
        #
        if len(data) == 0:
            # if there is anything in the buffer, then process it, otherwise nothing to see here
            #
            if len(self.__buffer) > 0:
                self.logger.info("PROCESSING (%i): [%s]" % (len(self.__buffer), self.__buffer))

                # Create lines for results
                #
                results = self.__lines_factory.build(self.__buffer)

                # Clear out the buffer
                #
                self.__buffer = ''

                # Insert into database
                #
                for l in results:
                    self.__dbLineManager.insert(l)
            else:
                pass
        else:
            # Otherwise, append this data to the buffer
            #
            self.__buffer += data


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
