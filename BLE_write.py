from cgitb import enable
import csv
import threading
from urllib import response
from xml.dom import InvalidModificationErr
from bluepy import btle
from bluepy.btle import Peripheral,UUID,DefaultDelegate,Scanner
from bluepy.btle import BTLEException
import _thread
import time
from log import Logger
logger = Logger(loggername='Gatt_Write').get_logger()

'''
connect to target device


'''

class ReceiveDelegate(DefaultDelegate):
    def __init__(self):
        super().__init__()
    
    def handleNotification(self, cHandle, data):
        print("handle: " + cHandle + "nofity" "----> ", data)



class BLE_control():
 
    # connect to target mac
    def tar_con(self, tar_mac):
        scanner = Scanner()
        devices = scanner.scan(timeout=10)
        logger.info("Begin sacn")
        # logger.info("发现 %d 个设备", len(devices))
        n = 1
        for dev in devices:    
            if dev.addr==tar_mac:
                logger.info("Find target device::"+ tar_mac)
                # logger.info("\n")
                # logger.info("               ---------广播信息------------             ")
                # logger.info("\n")
                # for (adtype, desc, value) in dev.getScanData():
                #     logger.info("%s = %s" % (desc, value))
                # logger.info("\n")
                # logger.info("               ---------广播信息------------             ")
                for i in range(0,5):
                    # logger.info("i = %d ", i)
                    try: 
                        # logger.info("...龟速连接中，第 " + str(i+1) +" 次尝试...")
                        self._conn = Peripheral(dev.addr, dev.addrType)
                        break
                    except:
                        if i<4:
                            continue
                        else:
                            logger.info('\n')
                            logger.error("The device connection failed, check the device status or previous pyload and try again.")
                            break
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

    def print_char(self):
        # Get service & characteristic
        wriList = {}
        services = self._conn.getServices()
        han_list = []
        for svc in services:
            print("[+]        Service: ", svc.uuid)
            characteristics = svc.getCharacteristics()
            for charac in characteristics:
                uu = charac.uuid
                Properties = charac.propertiesToString()
                print("    Characteristic: ", uu)
                print("        Properties: ", Properties)
                print("               handle:", charac.getHandle())

                #read
                if charac.supportsRead():
                    try:
                        value = charac.read()
                        print("             Value: ", value)
                        print("           charac: ", charac)
                    except BTLEException:
                        # print(uu+" read failed!!")
                        continue 

                # listen notification
                # if Properties.find('NOTIFY'):
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
                #         continu

                # write
                if 'WRITE' in Properties:
                    han = charac.getHandle()
                    wriList[svc.uuid]= uu                   #保存service uuid和characteristic uuid 
                    if han not in han_list:      
                        han_list.append(han)

                '''
                if  Properties.find('WRITE NO RESPONSE WRITE'):
                    print("WRITE NO RESPONSE WRITE")
                    try:
                        response = charac.write(data, withResponse=True)
                        print("        try fuzz0 ", uu )
                        print("        write data: ", data)
                        print("     write_response: ", response)
                    except BTLEException:
                        print("no response") 

                elif  Properties.find('WRITE NO RESPONSE'):
                    print("WRITE NO RESPONSE")
                    try:
                        charac.write(data, withResponse=False)
                        print("       try fuzz-1: ", uu)
                        print("no response write data: ", data)
                    except BTLEException:
                        print("no response write faild!")

                elif Properties.find('WRITE'):
                    print("JUST WRITE")
                    try:
                        response = charac.write(data, withResponse=True)
                        print("       try fuzz2:  ", uu )
                        print("    write data:  ", data)
                        print(" write_response: ", response)
                    except BTLEException:
                        print("no response") 
                else:
                    continue
                '''
            print(60*'-')
        self._conn.disconnect()
        return han_list

    def wait_noti(self, handle):

        self._conn.writeCharacteristic(handle, b'\x01\x00')  #\x01\x00 for notify

        while True:
            if self._conn.waitForNotifications(3.0):
            # handleNotification() was called
                continue
            
                #print("Waiting")

    def wait_indications(self, handle):

        self._conn.writeCharacteristic(handle, b'\x02\x00')  #\x01\x00 for indications
        while True:
            if self._conn.waitForNotifications(3.0):
                continue            
                #print("Waiting")


    # def wri_with_hand(self, handle, list):
    #     for v in list:
    #         if self._conn == True:
    #             try:
    #                 respon = self._conn.writeCharacteristic(handle, v, withResponse=True)                ## python3.*  type(val)=byte
    #                 print("write:" + str(v) +"to:" + str(handle) + "response: " + respon)
    #             except BTLEException  as ex:
    #                 print(ex)
    #         else:
    #             self.con_hold()
    #             try:
    #                 respon = self._conn.writeCharacteristic(handle, v, withResponse=True)                ## python3.*  type(val)=byte
    #                 print("write:" + str(v) +"to:" + str(handle) + "response: " + respon)
    #             except BTLEException  as ex:
    #                 print(ex)
    
    # write value to target device


    def wri_value(self, handle, val):

        if type(val) != bytes:
            val = val.encode()
        try:
            respon = self._conn.writeCharacteristic(handle, val, withResponse=True)                ## python3.*  type(val)=byte
            logger.info("Write: {} to: {}  response: {}".format(str(val),str(handle),respon))
        except BTLEException  as ex:
            logger.error("GATT write error: {}".format(str(ex)))

        # else:
        #     self.con_hold()
        #     try:
        #         respon = self._conn.writeCharacteristic(handle, val, withResponse=True)                ## python3.*  type(val)=byte
        #         logger.info("Write: {} to: {}  response: {}".format(str(val),str(handle),respon))
        #     except BTLEException  as ex:
        #         logger.error("GATT write error: {}".format(str(ex)))


    def write_to_csv(self, after_Muta_dic):

        for handle in after_Muta_dic.keys():
            self.path = './'+ str(handle) +'.csv'                               #把变异数据写入./fuzz_data.csv 
            
            with open(self.path, 'w+', newline='') as f:
                csv_doc = csv.writer(f)

                vlist = after_Muta_dic[handle]

                for k in range(len(vlist)):
                    # TODO 在每次写之前进行状态判断
                    
                    if self._conn == True:
                        self.wri_value(handle, vlist(k))               
                        logger.info("Write value:{} to handle: {}".format(str(vlist(k)),str(handle)))
                        #k = k.decode(encoding="utf-8").replace('|', '')
                        try:
                            csv_doc.writerow(vlist(k))
                        except:
                            # 部分bad strings写入csv会报错，这里先忽略，所以最终的csv文件可能会不全
                            continue
                    else:
                        # 1. 扫描是否广播； 2. 扫描是否可连接   
                        if k != 0:
                            logger.error("Check handle:{},     pyload: {}".format(str(handle), str(vlist(k-1))))
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