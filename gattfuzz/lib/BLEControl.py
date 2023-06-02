from cgitb import enable
import csv
import threading
from bluepy import btle
from bluepy.btle import Peripheral,UUID,DefaultDelegate,Scanner
from bluepy.btle import BTLEException
import _thread
import time
from gattfuzz.lib.Logger import Logger
logger = Logger(loggername='Gatt_Write').get_logger()

'''
connect to target device

#TODO 监听所有notification接口，所有indications属性

'''

class ReceiveDelegate(DefaultDelegate):
    def __init__(self):
        super().__init__()
    
    def handleNotification(self, cHandle, data):
        logger.error("Recevied handle: {}  nofity  ----> {} ".format(str(cHandle), str(data)))



class BLEControl():
 
    # connect to target mac
    def tar_con(self, tar_mac):
        logger.info("Begin sacn")
        n = 1
        scanner = Scanner()
        devices = scanner.scan(timeout=10)
        logger.info("发现 %d 个设备", len(devices))          
        for dev in devices:    
            if dev.addr==tar_mac:
                logger.info("Find target device::"+ tar_mac)
                # logger.info("\n")
                logger.info("              ————————————广播信息————————————                    ")
                logger.info("|                                                      |")
                for (adtype, desc, value) in dev.getScanData():
                    logger.info("    %s = %s" % (desc, value))
                logger.info("|                                                      |")
                logger.info("              ————————————广播信息————————————                    ")
                for i in range(0,10):
                    # logger.info("i = %d ", i)
                    try: 
                        logger.info("...龟速连接中，第 " + str(i+1) +" 次尝试...")
                        self._conn = Peripheral(dev.addr, dev.addrType)
                        break
                    except:
                        if i<10:
                            continue
                        else:
                            logger.info('\n')
                            logger.error("The device connection failed, check the device status or previous pyload and try again.")
                            # sys.exit()
                if self._conn:
                    self._mac = tar_mac
                    self._conn.setDelegate(ReceiveDelegate())
                    self._conn.setMTU(500)
                    # self.print_char()
                
                else: 
                    if n < len(devices):
                        n = n+1
                        continue
                    else:
                        logger.error("The target device was not found, please confirm the device status or previous pyload and try again.")
                        break      
        
        # find_flag = False
        # logger.info("Begin sacn")
        # n = 1
        # for _ in range(15):  
        #     scanner = Scanner()
        #     devices = scanner.scan(timeout=10)
        #     # logger.info("发现 %d 个设备", len(devices))          
        #     for dev in devices:    
        #         if dev.addr==tar_mac:
        #             find_flag = True
        #             logger.info("Find target device::"+ tar_mac)
        #             # logger.info("\n")
        #             logger.info("              ————————————广播信息————————————                    ")
        #             logger.info("|                                                      |")
        #             for (adtype, desc, value) in dev.getScanData():
        #                 logger.info("    %s = %s" % (desc, value))
        #             logger.info("|                                                      |")
        #             logger.info("              ————————————广播信息————————————                    ")
        #             for i in range(0,5):
        #                 # logger.info("i = %d ", i)
        #                 try: 
        #                     logger.info("...龟速连接中，第 " + str(i+1) +" 次尝试...")
        #                     self._conn = Peripheral(dev.addr, dev.addrType)
        #                     break
        #                 except:
        #                     if i<4:
        #                         continue
        #                     else:
        #                         logger.info('\n')
        #                         logger.error("The device connection failed, check the device status or previous pyload and try again.")
        #                         # sys.exit()
        #             if self._conn:
        #                 self._mac = tar_mac
        #                 self._conn.setDelegate(ReceiveDelegate())
        #                 self._conn.setMTU(500)
        #                 # self.print_char()
                    
        #             break
        #         # else: 
        #         #     if n < len(devices):
        #         #         n = n+1
        #         #         continue
        #         #     else:
        #         #         logger.error("The target device was not found, please confirm the device status or previous pyload and try again.")
        #         #         break       

                
        #     if not find_flag:  
        #         logger.error("The target device was not found, please confirm the device status and try again.")  
        #         # 

        # print(" Begin scan:")
        # scanner = Scanner()
        # devices = scanner.scan(timeout=10)
        # for dev in devices:
        #     if dev.addr==tar_mac:
        #         print("find target device:")
        #         print(dev)
        #         print("%-30s %-20s" % (dev.getValueText(9), dev.addr)) 
        #         self._mac = tar_mac 
        #         self._conn = Peripheral(dev.addr, dev.addrType )
        #         self._conn.setDelegate(ReceiveDelegate())
        #         self._conn.setMTU(500)

    
    # hold connect            
    def con_hold(self):
        self.tar_con(self._mac)
        self.open_notify()       # 打开notify

    def print_char(self):
        # Get service & characteristic
        wriList = {}
        services = self._conn.getServices()
        han_list = []
        for svc in services:
            print("[+]        Service: ", svc.uuid)
            for n in range(0,10):
                try:
                    characteristics = svc.getCharacteristics()
                    break
                except:
                    if n < 10:
                        continue
                    else:
                        logger.warning("Service {} char get error.")
                        continue
            for charac in characteristics:
                uu = charac.uuid
                Properties = charac.propertiesToString()
                print("    Characteristic: ", uu)
                print("        Properties: ", Properties)
                print("            handle: ", charac.getHandle())
            
                # listen notification
                #     try:
                #         handl = charac.getHandle()
                #         notify = threading.Thread(target=self.wait_noti, name=str(handl), args=(handl, ))
                #         notify.start()                    
                #     except BTLEException:
                #         # print(uu + "notify failed!!")
                #         continue

                # if Properties.find('INDICATE'):
                #     try:
                #         handl = charac.getHandle()
                #         indicate = threading.Thread(target=self.wait_indications, name=str(handl), args=(handl, ))
                #         indicate.start()                   
                #     except BTLEException:
                #         # print(uu + "notify failed!!")
                #         continue

                # write

                # print(Properties)
                if 'WRITE' in Properties.replace(" ",""):
                    # print("write dadian")
                    han = charac.getHandle()
                    wriList[svc.uuid]= uu                   #保存service uuid和characteristic uuid 
                    if han not in han_list:      
                        han_list.append(han)

                if str(Properties).find('NOTIFY'):
                    handle = charac.getHandle()
                    try:
                        self._conn.writeCharacteristic(handle, b'\x01\x00')  #\x01\x00 for notify
                    except BTLEException:
                        logger.warning("Open handle :{} notification error.".format(str(handle)))
                        continue
                # listen INDICATE
                if str(Properties).find('INDICATE'):
                    handle = charac.getHandle()
                    try:
                        self._conn.writeCharacteristic(handle, b'\x02\x00')
                        # handl = charac.getHandle()
                        # indicate = threading.Thread(target=self.wait_indications, name=str(handl), args=(handl, ))
                        # indicate.start()                   
                    except BTLEException:
                        # print(uu + "notify failed!!")
                        logger.warning("Open handle :{} INDICATE error.".format(str(handle)))
                        continue
                
                # 很神奇，read操作会影响write属性的判断
                # read
                if charac.supportsRead():
                    try:
                        value = charac.read()
                        print("             Value: ", value)
                        print("            charac: ", charac)
                    except BTLEException:
                        # print(uu+" read failed!!")
                        continue 

                
            print(60*'-')
        # self._conn.disconnect()
        return han_list                     # 遍历pher设备handler，防止pcap包不全

    def wri_value(self, handle, val):

        if type(val) != bytes:
            val = val.encode()
        try:
            respon = self._conn.writeCharacteristic(handle, val, withResponse=True)                  ## python3.*  type(val)=byte
            logger.error("Write: {} to: {}  response: {}".format(str(val),str(handle),respon))       # 监听返回值
            self._conn.waitForNotifications(2.0)                                                     # 监听notify
        except BTLEException  as ex:
            logger.info("GATT write no response.")                                                  

    def open_notify(self):
        wriList = {}
        services = self._conn.getServices()
        for svc in services:
            for n in range(0,5):
                try:
                    characteristics = svc.getCharacteristics()
                    break
                except:
                    if n < 5:
                        continue
                    else:
                        logger.warning("Service {} char get error.")
                        continue
            for charac in characteristics:
                uu = charac.uuid
                Properties = charac.propertiesToString()

                # listen NOTIFY
                if Properties.find('NOTIFY'):
                    handle = charac.getHandle()
                    try:
                        self._conn.writeCharacteristic(handle, b'\x01\x00')  #\x01\x00 for notify
                    except BTLEException:
                        logger.warning("Open handle :{} notification error.".format(str(handle)))
                        continue
                # listen INDICATE
                if Properties.find('INDICATE'):
                    handle = charac.getHandle()
                    try:
                        self._conn.writeCharacteristic(handle, b'\x02\x00')
                        # handl = charac.getHandle()
                        # indicate = threading.Thread(target=self.wait_indications, name=str(handl), args=(handl, ))
                        # indicate.start()                   
                    except BTLEException:
                        # print(uu + "notify failed!!")
                        logger.warning("Open handle :{} INDICATE error.".format(str(handle)))
                        continue

    def write_to_csv(self, after_Muta_dic):

        for handle in after_Muta_dic.keys():
            # self.path = './'+ str(handle) +'.csv'                               #把变异数据写入./fuzz_data.csv 
            

            # with open(self.path, 'w+', newline='') as f:
            #     csv_doc = csv.writer(f)

            vlist = after_Muta_dic[handle]

            for k in range(len(vlist)):
                # 每次写之前进行状态判断
                
                if self._conn:
                    logger.info("连接中")
                    self.wri_value(handle, vlist[k])               
                    logger.info("Write value:{} to handle: {}".format(str(vlist[k]),str(handle)))
                    #k = k.decode(encoding="utf-8").replace('|', '')
                    # try:
                    #     csv_doc.writerow(vlist[k])
                    # except:
                    #     # 部分bad strings写入csv会报错，这里先忽略，所以最终的csv文件可能会不全
                    #     continue
                else:
                    logger.info("连接断开，尝试重连")
                    # 1. 扫描是否广播； 2. 扫描是否可连接   
                    if k != 0:
                        # logger.error("Check handle:{},     pyload: {}".format(str(handle), str(vlist(k-1))))
                        logger.error("write error")
                        self.con_hold()
                                                           

    # def wri_handle(self, mac, val, hand):
    #     conn = Peripheral(mac)
    #     if type(val) != bytes:
    #         val = val.encode()
    #     try:
    #         conn.writeCharacteristic(hand, val, withResponse=None)                ## python3.*  type(val)=byte
    #         print("write:" + str(val) +"      to:" + str(hand) )
    #     except BTLEException  as ex:
    #         print(ex)


# tar_mac = "FB:65:D4:C2:BE:5A" 
# tar_mac = "44:27:F3:37:E1:13"
# tar_mac = "60:1d:9d:df:08:90"
# tar_mac = "46:66:77:A8:3D:9C"
# tar_mac = "08:EB:29:50:9B:FB"
# ble = BLEControl()                 
# ble.tar_con(tar_mac.lower())
# bulepy_handles = ble.print_char()