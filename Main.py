from Value_LCS import Value_LCS
from Pkt_pro import Pkt_pro
from BLE_write import BLE_control
from scapy.all import *
import argparse

from log import Logger
logger = Logger(loggername='Main').get_logger()

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='input pcap file',required=False)
parser.add_argument('-m', '--mac', help='mac address of target', required=True)

val = Value_LCS()


'''
7.21 一个问题（已解决）
基于pcap的变异覆盖率

7.21 一个问题
多次连接才能连上
'''
def Pcap_fuzz(pcap_path,tar_mac):
    
    latest_dic={}
    #提取数据包 static          
    logger.info("#"*30+"开始处理pcap文件"+'#'*30)
    pkt = Pkt_pro(pcap_path)

    pcap_handles = []
    han_val_dic = {}

    pcap_handles, han_val_dic = pkt.pr_pcap()          # 返回handle列表和{handle：[value]}字典
    logger.info("#"*30+"处理pcap文件结束"+'#'*30)
    print("pcap handles:", pcap_handles)                # pcap中的handles
    #logger.info("all_value:", han_val_dic)
                                      

    # connect device and logger.info chars
    logger.info("#"*30+ "设备扫描"+ '#'*30)
    ble = BLE_control()                 
    ble.tar_con(tar_mac)
    bulepy_handles = ble.logging.info_char()                      # 建立连接打印read，并打开所有notification
    logger.info("bluepy handles:", bulepy_handles)

    # 存在部分handle不通信的情况，pcap中没有数据，补充这部分
    for handle in bulepy_handles:
        logger.info("handle:", handle)
        if handle not in pcap_handles:
            latest_dic[handle] = []
        else:
            latest_dic[handle] = han_val_dic[handle]
    logger.info("latest pcap dic:", latest_dic)
    
    logger.info("#"*30+ "fuzz 输入"+ '#'*30)
    after_Muta_dic = val.pro_dict( latest_dic)              # 进行规则标记、变异，返回变异后字典
    # logger.info(after_Muta_dic)
    ble.tar_con(tar_mac)
    ble.write_to_csv(after_Muta_dic)                        # write过程写入csv并写到目标设备handle


def no_pcap_fuzz(tar_mac):

    # just write
    ble = BLE_control()
    ble.tar_con(tar_mac)
    handles = ble.logging.info_char()
    logger.info(handles)

    # 随机变异十次
    n = 0
    while n<10:
        val.var_no_pcap(tar_mac, handles)
        n=+1

#pcap_path = 'E:\IoT_Test\德施曼智能门锁\\5.pcapng'
#pcap_path = 'E:\IoT_Test\小米手环\\4_mingwen3.pcapng'
pcap_path = 'sum.pcapng'
tar_mac = 'ec:a9:2a:78:18:48'
logger.warning('start pcap fuzz')
Pcap_fuzz(pcap_path, tar_mac)

# def main():
#     args = parser.parse_args()
#     pcap_path = args.file
#     target_mac = args.mac
#     try:
#         if not pcap_path:
#             no_pcap_fuzz(target_mac)
#         else:
#             Pcap_fuzz(pcap_path, target_mac)
#     except Exception as e:
#         print('[-] fuzz error : {}'.format(e))

# if __name__ == '__main__':
#     main()