import unittest
import pcapy
import sys
from impacket.ImpactDecoder import *


class TestCapture(unittest.TestCase):
    def test_list_interfaces(self):
        ifs = pcapy.findalldevs()
        print(ifs)

        dev = 'eth0'

        if 0 == len(ifs):
            print("You don't have enough permissions to open any interface on this system.")
            sys.exit(1)

        # Only one interface available, use it.
        elif 1 == len(ifs):
            print('Only one interface present, defaulting to it.')
            dev=ifs[0]

        pc = pcapy.open_live(dev, 65535, True, 100)
        print(pc)

        pc.setfilter('tcp')
        pc.setfilter("ip && tcp && dst net %s && dst port 80" % '204.194.111.66')

        print("ip && tcp && dst net %s && dst port 80" % '204.194.111.66')

        # pc.loop(-1, self.recv_pkts) # capture packets

    def recv_pkts(self, hdr, data):
        print(data)
        packet = EthDecoder().decode(data)
        ip = packet.child()
        tcp = ip.child()
        adata = tcp.get_data_as_string()
        print(adata)
