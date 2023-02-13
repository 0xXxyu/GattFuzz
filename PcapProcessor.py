import binascii
from re import sub
from struct import unpack
from scapy.all import *
from Logger import Logger
import matplotlib
matplotlib.use('Agg')
logger = Logger(loggername='Pkt_pro').get_logger()
'''
提取pcap中request_command handle和value到字典

{'handle':['value1','value2']}
'''


class PcapProcessor():

    def __init__(self, pcap_path):
        self.handWvalue = {}
        self.write_handler_list = []
        self.pcap_path = pcap_path
    

    def process_pcap(self):
        packets =  rdpcap(self.pcap_path)
        for packet in packets: 
            try:                                            # 需要添加mac判断
                raw = packet.raw_packet_cache                  # <class 'bytes'>               
                # print("raw:", raw.hex())
                attr_prot = raw[27 : len(raw) - 3]   
                self.parse_attr_protocol(attr_prot)
            except Exception as e:
                logger.warning(e)
                continue  
        # print(self.write_handler_list)
        # print(self.handWvalue)
        return self.write_handler_list, self.handWvalue

    def parse_attr_protocol(self, attr_prot):
        
        # opcode = attr_prot[:1]
        
        # logger.info(opcode)

        # opcode(1) + handler(2) + value(>=1)
        if len(attr_prot) <= 4:
            # logger.error('[-] error attr_prot')
            return


        opcode = unpack('<b', attr_prot[0:1])[0]


        # print("opcode:", opcode.hex())
        if opcode == 0x52:     #write command 0x52
            handler = unpack('<h', attr_prot[1:3])[0]
            # logger.info(handler)

            value = attr_prot[3:]
            value_hex = value.hex()
            
            if handler not in self.handWvalue.keys():
                self.write_handler_list.append(value_hex)
                # val = []
                # val.append(value_hex)
                self.handWvalue[handler] = [value_hex]           #{handle:value}
            else:
                if value_hex not in self.handWvalue[handler]:                 #去重
                    self.handWvalue[handler].append(value_hex)

        #elif opcode.hex() == '12':
            #print("write request")
        #else:
            #print("other")

        #return self.wri_handle, self.handWvalue


if __name__ == '__main__':
    pcap_path = './sum.pcap'
    pcap_processor = PcapProcessor(pcap_path)
    hand, val = pcap_processor.process_pcap()
    print(hand)
    print(val)