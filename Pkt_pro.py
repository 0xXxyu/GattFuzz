import binascii
from re import sub
from scapy.all import *
from log import Logger
logger = Logger(loggername='Pkt_pro').get_logger()
'''
提取pcap中request_command handle和value到字典

{'handle':['value1','value2']}
'''


class PcapProcessor():

    def __init__(self, pcap_path):
        self.handWvalue = {}
        self.write_handle = []
        self.pcap_path = pcap_path
    

    def process_pcap(self):
        packets =  rdpcap(self.pcap_path)
        for packet in packets: 
            try:                                            # 需要添加mac判断
                raw = packet.raw_packet_cache                  # <class 'bytes'>
                
                #print("raw:", raw.hex())
                attr_prot = raw[27 : len(raw) - 3]   
                self.process_attr_protocol(attr_prot)
            except:
                continue  
        # print(self.wri_handle)
        # print(self.handWvalue)
        return self.write_handle, self.handWvalue

    def process_attr_protocol(self, att):
        
        opcode = att[:1]

        # print("opcode:", opcode.hex())
        if opcode.hex() == '52':     #write command 0x52

            handl0 = att[2:3]+att[1:2]           # 小端转大端，<class 'bytes'>
            value0 = att[3:]
            hand = handl0.hex()
            handl = int(hand, 16)

            value = value0.hex()
            
            if handl not in self.handWvalue.keys():
                self.wri_handle.append(handl)
                val = []
                val.append(value)
                
                self.handWvalue[handl] = val           #{handle:value}
            else:
                if value not in self.handWvalue[handl]:                 #去重
                    self.handWvalue[handl].append(value)

        #elif opcode.hex() == '12':
            #print("write request")
        #else:
            #print("other")

        #return self.wri_handle, self.handWvalue


if __name__ == '__main__':
    pcap_path = './sum.pcap'
    packets =  rdpcap(pcap_path)
    logger.info(len(packets))
    for packet_item in packets:
        logger.info(packet_item)
        raw = packet_item.raw_packet_cache
        att = raw[27 : len(raw) - 3]
        logger.info(att)
        break