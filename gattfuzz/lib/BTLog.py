import time

import scapy
from gattfuzz.lib.Logger import Logger
from scapy import utils
from scapy.layers.bluetooth import BluetoothHCISocket

logger = Logger(loggername='BTLog').get_logger()


class BTLog():

    # 默认使用hci0
    def __init__(self, hci=0):
        self.hci = hci
        self.pks = None

    def catch_log(self):
        bt = BluetoothHCISocket(self.hci)
        self.pks = bt.sniff()


    def save_pcap(self):
        pcap_name = time.time()
        utils.wrpcap("../data/"+ str(pcap_name) +".pcap", self.pks)
        logger.info("数据包已保存到"+"../data/"+ str(pcap_name) +".pcap")
