import unittest
import pcapy
from impacket.ImpactDecoder import *


class TestCapture(unittest.TestCase):
    def test_list_interfaces(self):
        pc = pcapy.open_live('eth0', 65535, True, 1000)
        # pc.setfilter('tcp')
        pc.setfilter("ip && tcp && dst net %s && dst port 80" % '204.194.111.66')
        # pc.loop(-1, self.recv_pkts)  # capture packets

    def recv_pkts(self, hdr, data):
        packet = EthDecoder().decode(data)
        ip = packet.child()
        tcp = ip.child()
        adata = tcp.get_data_as_string()
        print("DATA: %s" % adata)
