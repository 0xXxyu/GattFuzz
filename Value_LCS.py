from asyncore import write
import csv
import time
from distutils.file_util import write_file

#import pandas as pd
from BLE_write import BLE_write
from Var_string import Var_string

from bluepy.btle import Peripheral,UUID
from bluepy.btle import BTLEException

'''
接收pcap字典，value列表逐个比较，给出变异字段
'''

class Value_LCS():

    def __init__(self):
        self._static = '**'
        self._coun = '##'
        self._simple = '^^'
        self._pyload = '++'  
        self._simple_list = []              # 2字节value
        self.var_string = Var_string()


    '''
    对每个value列表中值两两进行横向比较，给出变异数据

    每个handle生成一个变异数据集合
    '''
    def find_lcseque(self, handle, s1, s2):
        from builtins import str
        timest = str(int(time.time()))

        after_var_data = {}
        len1 = int(len(s1)/2)
        len2 = int(len(s2)/2)

        s01 = []
        s02 = []
    
        for ik in range(len1):
            s01.append(s1[ik*2]+s1[ik*2+1])         #按2字节分割字符串
        for jk in range(len2):
            s02.append(s2[jk*2]+s2[jk*2+1])

        str = self._pyload *len(s01)

        ly_count = 0                        # pyload计数位
        #标记static
        for i in range(len(s01)):
            #print("处理位：", s01[i])
            hex0 = abs(int(s01[i],16)-int(s02[i],16))

            if len(s01) == 1:
                if s01[0] not in self._simple_list:
                    self._simple_list.append(s01[0])        #固定输入字节,比如0xfe05，mac
                    if s02[0] not in self._simple_list:
                        self._simple_list.append(s02[0])
                str = str[:i*2] + self._simple + str[(i+1)*2:]  

                simple_var_list = self._simple_list + self.var_string.string_var(1) + self.var_string.bad_strs_list() + self.var_string.pyload_var(2)   # 2字节数据同时调用“坏”字符串进行测试
                
                #self.write_var(simple_var_list)
                after_var_data[0] = simple_var_list

                break    
                # return self._simple_list                                   #2字节数据
            elif s01 == s02:
                
                after_var_data[0] = self.var_string.string_var(len(s01)*2) + self.var_string.pyload_var(len(s01)*2) + self.var_string.bad_strs_list()
                
                break
 
            elif s01[i] == s02[i]:              #当前字节相同  
                str = str[:i*2] + s01[i] + str[(i+1)*2:]

                #self.write_var([s01[i]])

                after_var_data[i]=s01[i].encode()   
                #print("标记static，pyload_cont置0")
                if ly_count>0:
                    #print("标记static后pyload_cont:", ly_count)
                    pyload_list = self.var_string.pyload_var(ly_count) + self.var_string.string_var(ly_count)       #随机字符串变异、坏字符串变异

                    after_var_data[i-1] = pyload_list
                ly_count = 0
            elif hex0 == 1:
                str = str[:i*2] + self._coun + str[(i+1)*2:]                   #标记计数位,一般两个字节
                count_list = self.var_string.count_var(s01[i])
                #self.write_var(count_list)
                after_var_data[i] = count_list
                # print("标记count，pyload_cont置0")
                if ly_count>0:
                    #print("标记count后pyload_cont:", ly_count)
                    pyload_list = self.var_string.pyload_var(ly_count) + self.var_string.string_var(ly_count)

                    after_var_data[i-1] = pyload_list
                ly_count = 0
            else:
                if i == 0:
                    ly_count = 2                                               # else即对应的str2字节标记为++
                #print("当前值：", s01[i])   
                else:
                    if str[i*2] == '+':
                        ly_count += 2
                    #print("pyload_cont:", ly_count+2)

       
        if ly_count != 0:
            pyload_list = self.var_string.pyload_var(ly_count) + self.var_string.string_var(ly_count)
            after_var_data[i-1] = pyload_list
            # print("py_load_count:", ly_count)


        # print("原字符串：", s1) 
        # print("比较字符：", s2)            
        # print("返回规则：", str)
        # print(after_var_data)
        # print(self._simple_list)
        
        self.write_value(handle, after_var_data)              
        '''
        # 生成字符串长度加1的0矩阵，m用来保存对应位置匹配的结果
        m = [[0 for x in range(len2 + 1)] for y in range(len1 + 1)]
        # d用来记录转移方向
        d = [[None for x in range(len2 + 1)] for y in range(len1 + 1)]

        for p1 in range(len1):
            for p2 in range(len2):
                if s01[p1] == s02[p2]:  # 字符匹配成功，则该位置的值为左上方的值加1
                    m[p1 + 1][p2 + 1] = m[p1][p2] + 1
                    d[p1 + 1][p2 + 1] = 'ok'
                elif m[p1 + 1][p2] > m[p1][p2 + 1]:  # 左值大于上值，则该位置的值为左值，并标记回溯时的方向
                    m[p1 + 1][p2 + 1] = m[p1 + 1][p2]
                    d[p1 + 1][p2 + 1] = 'left'
                else:  # 上值大于左值，则该位置的值为上值，并标记方向up
                    m[p1 + 1][p2 + 1] = m[p1][p2 + 1]
                    d[p1 + 1][p2 + 1] = 'up'
        (p1, p2) = (len1, len2)
        #print(numpy.array(d))
        s = []
        while m[p1][p2]:  # 不为None时
            c = d[p1][p2]
            if c == 'ok':  # 匹配成功，插入该字符，并向左上角找下一个
                s.append(s01[p1 - 1])
                str += '**'
                p1 -= 1
                p2 -= 1
            if c == 'left':  # 根据标记，向左找下一个
                str += s01[p1]
                p2 -= 1
            if c == 'up':  # 根据标记，向上找下一个
                str += s01[p1]
                p1 -= 1
        s.reverse()
        print(str)
        return s
        return ''.join(s)
        '''

    #字典处理
    '''
    1. 

    传入pcap处理后的字典 格式：{'handle':['value1','value2']}

    判断value列表大小，调用find_lcseque函数生成变异字符串
    '''
    def pro_dict(self, dic):
        for key in dic.keys():
            handle = key
            valu = dic[key]

            if len(valu) == 1:
                print(handle + "只有一个输入" + valu )
                self.find_lcseque(handle, valu[0], valu[0])
            else:
                for i in range(len(valu)):
                    for j in range(len(valu)):
                        if len(valu[i]) == len(valu[j]):        # 包括一次重放
                            print('-'*60)
                            self.find_lcseque(handle, valu[i],valu[j])             


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
        
        mac = 'b4:60:ed:99:1f:34'
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
            
        
# val = b'B51B6388'
# mac = '6c:ce:44:f5:8f:53'
# hand = 16

# v = Value_LCS()
# v.wri_handle(mac, val, hand)
