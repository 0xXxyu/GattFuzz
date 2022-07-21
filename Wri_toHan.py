


from BLE_write import BLE_write


class Wri_toHan():
    
    def write_value(self, handle, dic):
        shx = sorted(dic.keys())
        dic_shx = {}
        for sx in shx:
            dic_shx[sx] = dic[sx]
        after_var_value = self.fn(dic_shx)
        self.write_to_handle(handle, after_var_value)
                        
                        
    def write_var(self, mac, handle, dic):                           #按行写入
        shx = sorted(dic.keys())
        dic_shx = {}
        for sx in shx:
            dic_shx[sx] = dic[sx]
        after_var_value = self.fn(dic_shx)
        self.write_to_handle(mac, handle, after_var_value)
        # return handle, after_var_value
        

    def write_to_handle(self,  handle, after_var_value):
        ble = BLE_write()
        self.path = './'+ str(handle) +'.csv'                               #把变异数据写入./fuzz_data.csv 
        
        with open(self.path, 'w+', newline='') as f:
            csv_doc = csv.writer(f)
            for k in after_var_value:
                self.wri_handle( mac, k, handle)                #mac, value, handle
                print("write value："+ str(k) + "to handle:"+str(handle)) 
                #k = k.decode(encoding="utf-8").replace('|', '')
                try:
                    csv_doc.writerow(k)
                except:
                    continue
                          

    def fn(self, dict):
        lists = list(dict.values())    
        from functools import reduce
            
        def myfunc(list1, list2):
            return [str(i)+str(j) for i in list1 for j in list2]
        return reduce(myfunc, lists)


    def var_no_pcap(self,  mac, handles):
        
        after_strs = self.var_string.bad_strs_list() + self.var_string.pyload_var(2) + self.var_string.pyload_var(4) + self.var_string.pyload_var(6) + self.var_string.pyload_var(8) + self.var_string.pyload_var(10) + self.var_string.pyload_var(12) + self.var_string.pyload_var(20)

        for hand in handles:
            self.write_to_handle(hand, after_strs)

    def wri_handle(self, mac, val, hand):
        conn = Peripheral(mac)
        if type(val) != bytes:
            val = val.encode()
        try:
            conn.writeCharacteristic(hand, val, withResponse=None)                ## python3.*  type(val)=byte
            print("write:" + str(val) +"      to:" + str(hand) )
        except BTLEException  as ex:
            print(ex)