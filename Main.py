from Value_LCS import Value_LCS
from Pkt_pro import Pkt_pro
from BLE_write import BLE_write


#提取数据包
pcap_path = './1.pcap'                  
pkt = Pkt_pro(pcap_path)
all_handles = []
all_values = {}
all_handle, all_values = pkt.pr_pcap()          # 


tar_mac = ''
ble = BLE_write()
ble.tar_con(tar_mac)
ble.print_char()


# 横向比较——变异——输入
val = Value_LCS()
val.pro_dict(all_values)



