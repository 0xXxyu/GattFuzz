import argparse
import os
import time

from scapy.all import *

from gattfuzz.lib.BLEControl import BLEControl
from gattfuzz.lib.BTLog import BTLog
from gattfuzz.lib.PcapProcessor import PcapProcessor
from gattfuzz.lib.StringMutator import StringMutator
from gattfuzz.lib.ValueLCS import ValueLCS

stringMutator = StringMutator()

from gattfuzz.lib.Logger import Logger

logger = Logger(loggername='Main').get_logger()


val = ValueLCS()

'''
2023.2.8 补充 空payload
7.21 一个问题（已解决）
基于pcap的变异覆盖率

7.21 一个问题
多次连接才能连上
'''

def fuzz_with_pcap(ble, btlog, pcap_path):
    
    latest_dic = {}
    #提取数据包 static          
    logger.info("--开始处理pcap文件--")
    pcap_processor = PcapProcessor(pcap_path)

    pcap_handles = []
    han_val_dic = {}

    pcap_handles, han_val_dic = pcap_processor.process_pcap()          # 返回handle列表和{handle：[value]}字典
    logger.info("--处理pcap文件结束--")
    # print("pcap handles:", pcap_handles)                # pcap中的handles
    # print("all_value:", han_val_dic)
                                      
    # connect device and logger.info chars
    # logger.info("#"*30+ "设备扫描"+ '#'*30)

    btlog.start_sniffing()       # 开始抓包
              
    ble.tar_con()
    bulepy_handles = ble.print_char()                      # 建立连接打印read，并打开所有notification
    logger.info("bluepy handles:{}".format(str(bulepy_handles)))

    # 存在部分handle不通信的情况，pcap中没有数据，补充这部分
    for handle in bulepy_handles:
        # logger.info("handle:{}".format(str(handle))
        if handle not in pcap_handles:
            latest_dic[handle] = []
        else:
            latest_dic[handle] = han_val_dic[handle]
    # print("latest pcap dic:", latest_dic)
    
    logger.info("--开始变异--")
    after_Muta_dic = val.pro_dict(latest_dic)              # 进行规则标记、变异，返回变异后字典
    # logger.info(after_Muta_dic)
    # ble.tar_con(tar_mac)
    # # TODO +判断连接状态
    ble.write_to_csv(after_Muta_dic)                        # write过程写入csv并写到目标设备handle
    btlog.stop_sniffing()


def fuzz_without_pcap(ble):

    # btlog.start_sniffing()       # 开始抓包
    ble.tar_con()
    handles = ble.print_char()
    print("handles:", handles)

    # 随机变异100次
    n = 0
    after_dic = {}
    
    while n<100:
        logger.info("--开始随机变异--")
        after_dic = val.var_no_pcap(handles)   # 一次变异
        logger.info("--随机变异结束--")
        # print("after_dic:", after_dic)
        n += 1

        time.sleep(10.0)
        print(ble._conn)
        logger.info("--开始变异结果写入--")
        # ble.tar_con(tar_mac)
        ble.write_to_csv(after_dic)
        logger.info("--一次Fuzz结束--")
        
    # btlog.stop_sniffing()

def main():
    print("""
   ###     #     ####### #######   #######
  #   #    #        #       #     #
 #        ###       #       #     #        #    #  #####   #####
 #  ###   #  #      #       #     #####    #    #     #       #
 #    #  ######     #       #     #        #    #    #       #
  #   #  #    #     #       #     #        #   ##   #       #
   #### ##    ##    #       #     #         ### #  #####   #####

    """)
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='input pcap file',required=False)
    parser.add_argument('-m', '--mac', help='mac address of target', required=True)
    parser.add_argument('-p', '--path', help='input bad strings txt path', required=False)
    parser.add_argument('-x', '--hcix', help='input hci', default='hci0', required=False)
    args = parser.parse_args()

    pcap_path = args.file
    target_mac = args.mac
    bad_strings = args.path
    hcix = args.hcix

    # 初始化hci适配器
    if hcix in os.popen("sudo hciconfig -a").read():
        n = re.findall(r'\d+', hcix)
        btLog = BTLog(int(n[0]))                            # btlog初始化
        logger.info("使用" + hcix)
        ble = BLEControl(target_mac.lower(), n)
    elif hcix not in os.popen("sudo hciconfig -a"):
        logger.error("请确定使用'sudo hciconfig -a'查看本地支持的蓝牙适配器，并以hcix的格式输入。") 
        sys.exit(0)  
    else:
        logger.error("请确定使用'sudo hciconfig -a'查看本地支持的蓝牙适配器，并以hcix的格式输入。")

    # update bad payload
    if bad_strings and os.path.exists(str(bad_strings)) and bad_strings.endswitch('.txt'):
        stringMutator.input_list(bad_strings)
        logger.info("列表加载成功")
    else:
        pass

    if pcap_path and os.path.exists(pcap_path) and bad_strings.endswitch('.pcap'):
        fuzz_with_pcap(ble, btLog, pcap_path)
    else:
        # fuzz_without_pcap(ble, btLog)
        fuzz_without_pcap(ble)