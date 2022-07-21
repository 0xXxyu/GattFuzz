from Value_LCS import Value_LCS
from Pkt_pro import Pkt_pro
from BLE_write import BLE_write

val = Value_LCS()

def Pcap_var(pcap_path,tar_mac):

    #提取数据包 static            
    pkt = Pkt_pro(pcap_path)
   

    # connect device and print chars
    ble = BLE_write()
    ble.tar_con(tar_mac)
    handles = ble.print_char()
    print("handles:", handles)

    all_handles = []
    all_values = {}
    all_handle, all_values = pkt.pr_pcap()          # 返回handle列表和{handle：[value]}字典
    print("all_value:", all_values)

    val.pro_dict(all_values)
    # ble = BLE_write()
    # ble.tar_con(tar_mac)            
    # handles = ble.print_char()                      # 建立连接打印read，并打开所有notification

# #横向比较——变异——输入
# n = 0
# while n<10:
#     val.pro_dict(all_values)
#     n=+1


def Just_write(tar_mac):

    # just write
    ble = BLE_write()
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
Pcap_var(pcap_path, tar_mac)
