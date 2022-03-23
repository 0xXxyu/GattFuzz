from urllib import response
from bluepy import btle
from bluepy.btle import Peripheral,UUID
from bluepy.btle import BTLEException


class BLE_write():

    def tar_con(self, tar_mac):
        scanner = btle.Scanner(0)
        devices = scanner.scan(3.0)
        print(" Begin scan:")
        for device in devices:
            if device.addr == self._mac:
                for (adTypeCode, description, valueText) in device.getScanData():
                    addr_type = device.addrType
                    self._conn = Peripheral(self._mac, addr_type)

    def print_char(self):
        # Get service & characteristic
        wriList = {}
        if self._conn == None:
            print("connect device failed!")
        else:
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

                    #read
                    if charac.supportsRead():
                        try:
                            value = charac.read()
                            print("             Value: ", value)
                            print("           charac: ", charac)
                        except BTLEException:
                            # print(uu+" read failed!!")
                            continue 

                    ##监听notification
                    # if Properties.find('NOTIFY'):
                    #     try:
                    #         charac.enable_notifications()    #notify
                    #     except BTLEException:
                    #         # print(uu + "notify failed!!")
                    #         continue


                    # write
                    if Properties.find('WRITE'):
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
            return han_list


    def wri_handle(self, val, hand):

        if self._conn == True:
            try:
                write_respon = self._conn.writeCharacteristic(hand, val, withResponse=True)                ## python3.*  type(val)=byte
                print("write:" + val +"to:" + hand + "response: "+ write_respon)
            except BTLEException as ex:
                print("write:" + val +"to:" + hand + "error" + ex)   
        else:
            try:
                self.tar_con()
            except BTLEException:
                print("------------------connect failed! error" + ex + "please check fuzz result------------------------")
