import sys

from bluepy import btle
from bluepy.btle import (UUID, BTLEException, DefaultDelegate, Peripheral,
                         Scanner)
from gattfuzz.lib.Logger import Logger

logger = Logger(loggername='Gatt_Write').get_logger()

'''
connect to target device

'''

class ReceiveDelegate(DefaultDelegate):
    def __init__(self):
        super().__init__()
    
    def handleNotification(self, cHandle, data):
        logger.error("Recevied handle: {}  nofity  ----> {} ".format(str(cHandle), str(data)))


class BLEControl():

    def __init__(self, mac, iface=0):
        self._conn = None
        self._mac = mac
        self.iface = iface
    
    # connect to target mac
    def tar_con(self):
        logger.info("Begin sacn")
        n = 1
        scanner = Scanner()
        devices = scanner.scan(timeout=10)
        logger.info("发现 %d 个设备", len(devices))          
        for dev in devices:    
            if dev.addr==self._mac:
                logger.info("Find target device::"+ self._mac)
                # logger.info("\n")
                for i in range(0,10):
                    # logger.info("i = %d ", i)
                    try: 
                        logger.info("...龟速连接中，第 " + str(i+1) +" 次尝试...")
                        self._conn = Peripheral(dev.addr, dev.addrType, self.iface)
                        break
                    except:
                        if i<10:
                            continue
                        else:
                            logger.info('\n')
                            # logger.error("The device connection failed, check the device status or previous payload and try again.")
                            logger.error("未找到目标设备，请确定设备状态并重试")
                            # sys.exit()
                if self._conn:
                    self._conn.setDelegate(ReceiveDelegate())
                    self._conn.setMTU(500)
                    # self.print_char()              
            else: 
                if n < len(devices):
                    n = n+1
                    continue
                else:
                    # logger.error("The target device was not found, please confirm the device status or previous payload and try again.")
                    logger.error("未找到目标设备，请确定设备状态并重试")
                    sys.exit(0)     

    def con_age(self, tar_mac):
        logger.info("……reconnecting……")
        n = 1
        for _ in range(15):  
            scanner = Scanner()
            devices = scanner.scan(timeout=10)
            # logger.info("发现 %d 个设备", len(devices))               
            for dev in devices:    
                if dev.addr==tar_mac:
                    logger.info("Find target device::"+ tar_mac)
                    for i in range(0,5):
                        # logger.info("i = %d ", i)
                        try: 
                            # logger.info("...龟速连接中，第 " + str(i+1) +" 次尝试...")
                            self._conn = Peripheral(dev.addr, dev.addrType, self.iface)
                            break
                        except:
                            if i<4:
                                continue
                            else:
                                logger.info('\n')
                                logger.error("未找到目标设备，请确定设备状态并重试上一条指令。")
                                # sys.exit()
                    if self._conn:
                        self._mac = tar_mac
                        self._conn.setDelegate(ReceiveDelegate())
                        self._conn.setMTU(500)
                        # self.print_char()
                    
                    break
                else: 
                    if n < len(devices):
                        n = n+1
                        continue
                    else:
                        logger.error("未找到目标设备，请确定设备状态并重试上一条指令。")
                        sys.exit(0)

    
    # hold connect            
    def con_hold(self):
        self.con_age(self._mac)
        self.open_notify()       # 打开notify

    def print_char(self):
        # Get service & characteristic
        if self._conn:
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

                    if 'WRITE' in Properties.replace(" ",""):
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
        else:
            logger.info("连接断开，尝试重连...")
            self.con_hold()
            self.print_char()

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
        logger = self.logger
        wriList = {}
        services = self._conn.getServices()
        
        for svc in services:
            characteristics = []
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
        logger = self.logger
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
                        # logger.error("Check handle:{},     payload: {}".format(str(handle), str(vlist(k-1))))
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


# tar_mac = "DD:59:F8:7A:21:7A"
# ble = BLEControl(tar_mac.lower())                 
# ble.tar_con()
# han_list = ble.print_char()
# print(han_list)