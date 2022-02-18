import csv
from distutils.file_util import write_file
import pandas as pd
from re import S
import time
import numpy
from Var_string import Var_string

class Value_LCS():

    def __init__(self):
        self._static = '**'
        self._coun = '##'
        self._simple = '^^'
        self._pyload = '++'  
        self._simple_list = []              # 2字节value
        self.var_string = Var_string()

        

        timest = str(int(time.time()))
        self.path = './'+ timest +'.csv'                               #把变异数据写入./fuzz_data.csv    
        # with open(self.path, 'w+') as fs:                           #其中包括填充数据'NULL'，使用时需要去除
        #     csv_writ = csv.writer(fs)
            #csv_head = ["pyload", "simple", "string", "count"]
            # csv_writ.writerow(csv_head)

    #输入value字符串，比较标记给出fuzz规则
    def find_lcseque(self, s1, s2):
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

        #标记static
        for i in range(len(s01)):
            hex0 = abs(int(s01[i],16)-int(s02[i],16))

            if len(s01) == 1:
                if s01[0] not in self._simple_list:
                    self._simple_list.append(s01[0])        #固定输入字节,比如0xfe05，mac
                    if s02[0] not in self._simple_list:
                        self._simple_list.append(s02[0])
                str = str[:i*2] + self._simple + str[(i+1)*2:]  
                #print('2字节输入：', self._simple_list)

                simple_var_list = self._simple_list + self.var_string.string_var()                        # 2字节数据同时调用“坏”字符串进行测试
                #self.write_var(simple_var_list)
                after_var_data[0] = simple_var_list

                break    
                # return self._simple_list                                   #2字节数据
            elif s01[i] == s02[i]:              #当前字节相同  
                #str = str[:i*2] + _static + str[(i+1)*2:]                 #static用*标记
                str = str[:i*2] + s01[i] + str[(i+1)*2:]

                #self.write_var([s01[i]])

                after_var_data[i]=s01[i].encode()
            elif hex0 == 1:
                str = str[:i*2] + self._coun + str[(i+1)*2:]                   #标记计数位,一般两个字节
                count_list = self.var_string.count_var(s01[i])

                #self.write_var(count_list)

                after_var_data[i] = count_list
            else:                                   #pyload 处理
                
        print('-'*60)
        print("原字符串：", s1) 
        print("比较字符：", s2)            
        print("返回规则：", str)
        print(after_var_data)
        # print(self._simple_list)
        
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

    def pro_dict(self, dic):
        for key in dic.keys():
            handle = key
            valu = dic[key]

            if len(valu) == 1:
                print(handle + "只有一个输入" + valu )
            else:
                for i in range(len(valu)):
                    for j in range(len(valu)):
                        if len(valu[i]) == len(valu[j]):        # 包括一次重放
                            self.find_lcseque(valu[i],valu[j])
                         
    def write_var(self, all_lis):                           #按行写入
        with open(self.path, 'a+', newline='') as f:
            csv_doc = csv.writer(f)
            csv_doc.writerow(all_lis)


dic = {'58': ['0c008711f27d99c68c31795591b1e0ff1b0b79ee', '0d003265d97a0c126e43e98305', '0e004eeb7f5f5886e35ceb05e85aad72889358ab', '0f002d32bed929', '41005f9eccc9aa29e46d334098e7ab3d2ee9c62c', '4200857b1a7843fcfa1eb45730', '4300e72073131873dd499235c856', '44002efde832adba2128aa21c9d5', '45009214ae13b573711457fed9f1', '46008345e592d885e6f1fab528bb', '47004bbe788329c3b26baae508ab', '48006933a60987975765fdbd2486', '49005e83eefb76d9854a3f85c921', '4a00601832aad28fbf8f6f67eb70', '4b007040096a26813a0240bd9df6'], '64': ['0400e498bb0ad1981d9543b9af0335b2e8099664', '05008976d5f538de3ab0cf23d53a', '0600cf63cdc0f31aec5713ebf7e1', '0700be36030e2d980e4caf08efb5', '0800cbdf9b051634f022b123d11d9d2282ea06cf', '09009b38b329c319f5350a7d3784', '0a00429c76beb56da9c9c96e1de1']}
val = Value_LCS()
val.pro_dict(dic)
