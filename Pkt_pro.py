import binascii
from re import sub
from scapy.all import *

'''
提取pcap中request_command handle和value到字典
'''


class Pkt_pro():

    def __init__(self):
        self.handWvalue = {}
        self.wri_handle = []
    

    def pcap(self):
        pcap_path = './4.pcap'
        pkts = rdpcap(pcap_path)
        for pkt in pkts: 
            try:                               #需要添加mac判断
                raw = pkt.raw_packet_cache                  # <class 'bytes'>
                #return raw 
                att = raw[27:len(raw)-3]   
                self.sub_pak(att)
            except:
                continue  

        print(self.wri_handle)
        print(self.handWvalue)
        return self.wri_handle, self.handWvalue

    def sub_pak(self, att):
        
        opcode = att[:1]
        #print(opcode.hex())
        #print(type(opcode))
        
        if opcode.hex() == '52':     #write command 0x52
            handl = att[1:3]
            print(len(handl))
            print("handle:", type(handl))
            value = att[3:]
            #handl = handl.hex()
            #value = value.hex()
           
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

pkt = Pkt_pro()
pkt.pcap()
