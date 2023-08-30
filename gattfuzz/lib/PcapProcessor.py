from re import sub
from struct import unpack

from gattfuzz.lib.Logger import Logger
from scapy.all import *

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
    
    # def pcap_pro

    # 适用于解析手机抓到的hci log
    def att_data(self):
        handles = []
        hwdata = {}
        packets =  rdpcap(self.pcap_path)
        for packet in packets: 
            # print(packet)
            try:
                if "ATT header" in packet:
                    # print("发现 ATT header")
                    opcode = packet["ATT header"].opcode
                    if opcode == 0x52:
                        # hand = hex(packet["ATT header"]["Write Request"].gatt_handle)
                        hand = packet["ATT header"]["Write Request"].gatt_handle
                        data = packet["ATT header"]["Write Request"].data
                        # print("data type:", str(data))
                        if hand not in hwdata.keys():
                            handles.append(hand)
                            hwdata[hand] = [data]           #{handle:value}
                        else:
                            if data not in hwdata[hand]:                 #去重
                                hwdata[hand].append(data)
            except Exception as e:
                Logger.info(e)
                continue

        # print(handles)
        # print(hwdata)
        return handles, hwdata              

    # 适用于解析空中包
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
                self.write_handler_list.append(handler)
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


# if __name__ == '__main__':
#     pcap_path = './dump.pcap'
#     pcap_processor = PcapProcessor(pcap_path)
#     # hand, val = pcap_processor.process_pcap()
#     hand, val = pcap_processor.att_data()
#     print(hand)
#     print(val)
