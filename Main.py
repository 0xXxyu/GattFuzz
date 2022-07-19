from Value_LCS import Value_LCS
from Pkt_pro import Pkt_pro
from BLE_write import BLE_write

val = Value_LCS()

# #提取数据包 static
# pcap_path = './s2.pcap'                  
# pkt = Pkt_pro(pcap_path)
# all_handles = []# tar_mac = 'b4:60:ed:99:1f:16'    #B4:60:ED:99:1F:16
# ble = BLE_write()
# ble.tar_con(tar_mac)
# handles = ble.print_char()c
# print(handles)


# 随机变异
# n = 0
# while n<10:
#     val.var_no_pcap(tar_mac, handles)
#     n=+1

# all_values = {}
# all_handle, all_values = pkt.pr_pcap()          # 返回handle列表和{handle：[value]}字典
# print(all_values)


# tar_mac = ' b4:60:ed:99:1f:34'
# ble = BLE_write()
# ble.tar_con(tar_mac)            
# handles = ble.print_char()                      # 建立连接打印read，并打开所有notification

# #横向比较——变异——输入
# n = 0
# while n<10:
#     val.pro_dict(all_values)
#     n=+1


# just write
#tar_mac = '6c:ce:44:f5:8f:53'   #SE
#tar_mac = 'b4:60:ed:99:1f:34'    #B4:60:ED:99:1F:16
tar_mac = '9C:56:36:56:B6:E4'
ble = BLE_write()
ble.tar_con(tar_mac)
handles = ble.print_char()
print(handles)


#随机变异
n = 0
while n<10:
    val.var_no_pcap(tar_mac, handles)
    n=+1
