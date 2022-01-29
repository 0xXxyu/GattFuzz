import binascii
from scapy.all import *



# her: c1:aa:10:54:e4:58
# cen: 7d:8e:68:5c:79:a2


class pkt_pro():

    def __init__(self):
        pass


    def pcap(self):
        pcap_path = './1.pcap'
        pkts = rdpcap(pcap_path)
        for pkt in pkts:                                #需要添加mac判断
            raw = pkt.raw_packet_cache
            #sub_pak(raw)
            #return raw 
            att = raw[27:len(raw)-3]
            print(att.hex())    

    def sub_pak(self, att):
        if att[:1] == b'52':     #write command 0x52
            handl = att[1:2]
            value = att[3:]
            self.handWvalue[handl] = value           #{handle:value}

            self.wri_handle.append(handl)
        elif att[:1] == b'12':
            print("write request")
        else:
            print("other")
        print(self.wri_handle)
        print(self.handWvalue)

        return self.wri_handle, self.handWvalue






