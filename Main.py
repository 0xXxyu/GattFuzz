from Value_LCS import Value_LCS
from Pkt_pro import Pkt_pro
from BLE_write import BLE_control

val = Value_LCS()


'''
7.21 一个问题（已解决）
基于pcap的变异覆盖率
'''
def Pcap_fuzz(pcap_path,tar_mac):

    #提取数据包 static            
    pkt = Pkt_pro(pcap_path)

    pcap_handles = []
    han_val_dic = {}
    pcap_handles, han_val_dic = pkt.pr_pcap()          # 返回handle列表和{handle：[value]}字典
    print("pcap handles:", pcap_handles)                # pcap中的handles
    print("all_value:", han_val_dic)
                                      

    # connect device and print chars
    ble = BLE_control()                 
    ble.tar_con(tar_mac)
    bulepy_handles = ble.print_char()                      # 建立连接打印read，并打开所有notification
    print("handles:", bulepy_handles)

    # 存在部分handle不通信的情况，pcap中没有数据，补充这部分
    for handle in bulepy_handles:
        if handle not in pcap_handles:
            han_val_dic[handle] = []

    after_Muta_dic = val.pro_dict(han_val_dic)              # 进行规则标记、变异，返回变异后字典

    ble.tar_con(tar_mac)
    ble.write_to_csv(after_Muta_dic)                        # write过程写入csv并写到目标设备handle


def no_pcap_fuzz(tar_mac):

    # just write
    ble = BLE_control()
    ble.tar_con(tar_mac)
    handles = ble.print_char()
    print(handles)

    # 随机变异十次
    n = 0
    while n<10:
        val.var_no_pcap(tar_mac, handles)
        n=+1

pcap_path = '/home/xiaoyu/data/BleFuzz/BLEFuzz/open_lock_2.pcap'
tar_mac = 'ec:a9:2a:78:18:48'
Pcap_fuzz(pcap_path, tar_mac)
