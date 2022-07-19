from cgitb import enable
import threading
from urllib import response
from xml.dom import InvalidModificationErr
from bluepy import btle
from bluepy.btle import Peripheral,UUID,DefaultDelegate
from bluepy.btle import BTLEException
import _thread
import time

'''
connect to target device


'''

class ReceiveDelegate(DefaultDelegate):
    def __init__(self):
        super().__init__()
    
    def handleNotification(self, cHandle, data):
        print("handle: " + cHandle + "nofity" "----> ", data)


class BLE_write():

    def tar_con(self, tar_mac):
        print(" Begin connect:")
        self._mac =  tar_mac
        self._conn = Peripheral(tar_mac)

        self._conn.setDelegate(ReceiveDelegate())
        self._conn.setMTU(500)

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
            # handleNotification() was called
                continue
            
                #print("Waiting")


    def wri_with_hand(self, handle, list):
        for v in list:
            if self._conn == True:
                try:
                    respon = self._conn.writeCharacteristic(handle, v, withResponse=True)                ## python3.*  type(val)=byte
                    print("write:" + str(v) +"to:" + str(handle) + "response: " + respon)
                except BTLEException  as ex:
                    print(ex)
            else:
                self.tar_con('b4:60:ed:99:1f:34')
