import time

import threading
from gattfuzz.lib.Logger import Logger
from scapy import utils
from scapy.layers.bluetooth import BluetoothHCISocket

logger = Logger(loggername='BTLog').get_logger()


class BTLog():

    # 默认使用hci0
    def __init__(self, mac, hci=0 ):
        self.hci = hci
        self.pks = None
        self._thread = None
        self._running = False
        self._mac = mac

    def catch_log(self):
        self._running = True
        bt = BluetoothHCISocket(self.hci)
        self.pks = bt.sniff()

    def start_sniffing(self):
        if self._thread is None or not self._thread.is_alive():
            self._thread = threading.Thread(target=self.catch_log)
            self._thread.start()
            logger.info("Bluetooth sniffing started.")
        else:
            logger.error("Bluetooth sniffing is already running.")

    def stop_sniffing(self):
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(3)
            self.save_pcap()
            logger.info("Bluetooth sniffing stopped.")
        else:
            logger.error("Bluetooth sniffing is not running.")

    def save_pcap(self):
        pcap_name = time.time()
        utils.wrpcap(r"./gattfuzz/data/"+ self._mac + str(int(pcap_name)) +".pcap", self.pks)
        logger.info("数据包已保存到"+"./gattfuzz/data/"+ self._mac + str(int(pcap_name)) +".pcap")

