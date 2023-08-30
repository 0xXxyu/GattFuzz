from gattfuzz.lib.Logger import Logger
from gattfuzz.lib.StringMutator import StringMutator


logger = Logger(loggername='Value_LCS').get_logger()

'''
接收pcap字典，value列表逐个比较，给出变异字段
'''

class ValueLCS():

    def __init__(self):
        self._static = '**'
        self._count = '##'
        self._simple = '^^'
        self._payload = '++'  
        self._simple_list = []              # 2字节value
        self.string_mutator = StringMutator()
        self.Muta_dic = {}
        self._crc = None


    def get_lcs_rule(self, str1, str2):
        """
        比较两个输入字符串，得到 lcs_rule
        lcs_rule 由指定标记组成 -- _static, _coun, _simple, _payload
        : return :lcs_rule
        : type : list
        : eg: ['12', '++', '++', '##', '++', '++', '++', '++', '++', '++']
        """
        if len(str1) != len(str2):
            logger.warning('输入字符串长度不等: len(str1):{}\tlen(str2):{}'.format(len(str1), len(str2)))
        
        str_len = len(str1)

        # if (str_len % 2) != 0:
        #     str1 = '0' + str1
        #     str2 = '0' + str2
        #     str_len += 1

        str_list_01 = []
        str_list_02 = []

        for i in range(int(str_len/2)):
            str_list_01.append(str1[i*2] + str1[i*2 + 1])
            str_list_02.append(str2[i*2] + str2[i*2 + 1])

        # 字节长度等于 1， 认为属于 _simple
        if str_len == 1:
            if str_list_01[0] not in self._simple_list:
                self._simple_list.append(str_list_01[0])
            if str_list_02[0] not in self._simple_list:
                self._simple_list.append(str_list_02[0])
            lcs_rule = [self._simple]
            return lcs_rule
        
        # 字节长度不等于 1 且相同，认为整体为 _payload
        elif str1 == str2:
            lcs_rule = ['++'] * int(str_len/2)
            return lcs_rule
        
        # 初始均为 --
        # 以下开始标记规则
        lcs_rule = ['--'] * int(str_len/2)
        for i in range(int(str_len/2)):
            hex_diff = abs(int(str_list_01[i], 16) - int(str_list_02[i], 16))

            # 当前字节相同，认为固定不变
            if str_list_01[i] == str_list_02[i]:
                lcs_rule[i] = str_list_01[i]
            # 差值为 1，认为是 _coun
            elif hex_diff == 1:
                lcs_rule[i] = self._count
            # 否则，认为是 _payload
            else:
                lcs_rule[i] = self._payload

        return lcs_rule
    

    def find_lcseque_with_lcs_rule(self, lcs_rule, str_1, str_2):
        """
        根据 lcs_rule 进行变异
        """
        mutation_data_dic = {}
        count = 0
        payload_count = 0
        for i in range(len(lcs_rule)):
            lcs_tag = lcs_rule[i]
            str1_sub_content = str_1[i*2] + str_1[i*2 + 1]
            str2_sub_content = str_2[i*2] + str_2[i*2 + 1]

            if lcs_tag == self._static:
                pass
            elif lcs_tag == self._count:
                # 生成 count 变异数据
                count_mutation_data_list = self.string_mutator.get_count_mutation(str1_sub_content)
                # 生成 payload 变异数据
                if payload_count > 0:
                    payload_mutation_data_list = self.string_mutator.get_payload_mutation(payload_count) + self.string_mutator.get_string_mutation(payload_count)       #随机字符串变异、坏字符串变异
                    payload_count = 0
                    mutation_data_dic[count] = payload_mutation_data_list
                    count += 1
                
                mutation_data_dic[count] = count_mutation_data_list
                count += 1
            elif lcs_tag == self._simple:
                pass
            elif lcs_tag == self._payload:
                payload_count += 2
            else:
                # 生成 payload 变异数据
                if payload_count > 0:
                    payload_mutation_data_list = self.string_mutator.get_payload_mutation(payload_count) + self.string_mutator.get_string_mutation(payload_count)       #随机字符串变异、坏字符串变异
                    payload_count = 0
                    mutation_data_dic[count] = payload_mutation_data_list
                    count += 1
                mutation_data_dic[count] = [lcs_tag.encode()]
                count += 1
        
        # 以 payload 结尾
        if payload_count != 0:
            payload_var_data_list = self.string_mutator.get_payload_mutation(payload_count) + self.string_mutator.get_string_mutation(payload_count)       #随机字符串变异、坏字符串变异
            payload_count = 0
            mutation_data_dic[count] = payload_var_data_list
            count += 1

        print('===============')
        for i in mutation_data_dic:
            print('--------------------')
            mutation_data = mutation_data_dic[i]
            # logger.info(len(mutation_data))
            # logger.info(mutation_data)
        return mutation_data_dic


    '''
    对每个value列表中值两两进行横向比较，给出变异数据

    每个handle生成一个变异数据集合
    '''
    def find_lcseque(self, handle, str1, str2):
        # from builtins import str
        # timest = str(int(time.time()))

        mutation_data_dic = {}
        len1 = int(len(str1) / 2)
        len2 = int(len(str2) / 2)

        str1_splited_list = []
        str2_splited_list = []
    
        for ik in range(len1):
            str1_splited_list.append(str1[ik*2] + str1[ik*2 + 1])         #按2字节分割字符串
        for jk in range(len2):
            str2_splited_list.append(str2[jk*2] + str2[jk*2 + 1])

        str = self._payload * len(str1_splited_list)

        ly_count = 0                        # payload计数位
        #标记static
        for i in range(len(str1_splited_list)):
            # logger.info("处理位：{}".format(s01[i]))
            hex0 = abs(int(str1_splited_list[i], 16) - int(str2_splited_list[i], 16))

            if len(str1_splited_list) == 1:
                if str1_splited_list[0] not in self._simple_list:
                    self._simple_list.append(str1_splited_list[0])        #固定输入字节,比如0xfe05，mac
                    if str2_splited_list[0] not in self._simple_list:
                        self._simple_list.append(str2_splited_list[0])
                str = str[:i*2] + self._simple + str[(i+1)*2:]

                simple_var_list = self._simple_list + self.string_mutator.get_string_mutation(1) + self.string_mutator.bad_strs_list() + self.string_mutator.get_payload_mutation(2)   # 2字节数据同时调用“坏”字符串进行测试
                
                #self.write_var(simple_var_list)
                mutation_data_dic[0] = simple_var_list

                break    
                # return self._simple_list                                   #2字节数据
            elif str1_splited_list == str2_splited_list:
                
                mutation_data_dic[0] = self.string_mutator.get_string_mutation(len(str1_splited_list) * 2) + self.string_mutator.get_payload_mutation(len(str1_splited_list) * 2) + self.string_mutator.bad_strs_list()
                
                break
 
            elif str1_splited_list[i] == str2_splited_list[i]:              #当前字节相同  
                str = str[:i*2] + str1_splited_list[i] + str[(i+1)*2:]

                #self.write_var([s01[i]])

                mutation_data_dic[i]=[str1_splited_list[i].encode()]
                #print("标记static，payload_cont置0")
                if ly_count > 0:
                    #print("标记static后payload_cont:", ly_count)
                    payload_mutation_list = self.string_mutator.get_payload_mutation(ly_count) + self.string_mutator.get_string_mutation(ly_count)       #随机字符串变异、坏字符串变异

                    mutation_data_dic[i-1] = payload_mutation_list
                ly_count = 0
            elif hex0 == 1:
                str = str[:i*2] + self._count + str[(i+1)*2:]                   #标记计数位,一般两个字节
                count_mutation_list = self.string_mutator.get_count_mutation(str1_splited_list[i])
                #self.write_var(count_list)
                mutation_data_dic[i] = count_mutation_list
                # print("标记count，payload_cont置0")
                if ly_count > 0:
                    #print("标记count后payload_cont:", ly_count)
                    payload_mutation_list = self.string_mutator.get_payload_mutation(ly_count) + self.string_mutator.get_string_mutation(ly_count)

                    mutation_data_dic[i-1] = payload_mutation_list
                ly_count = 0
            else:
                if i == 0:
                    ly_count = 2                                               # else即对应的str2字节标记为++
                #print("当前值：", s01[i])   
                else:
                    if str[i*2] == '+':
                        ly_count += 2
                    #print("payload_cont:", ly_count+2)

       
        if ly_count != 0:
            payload_mutation_list = self.string_mutator.get_payload_mutation(ly_count) + self.string_mutator.get_string_mutation(ly_count)
            mutation_data_dic[i-1] = payload_mutation_list
            # print("py_load_count:", ly_count)


        # print("原字符串：", s1) 
        # print("比较字符：", s2)            
        # print("返回规则：", str)
        # print(var_data_dic)
        # print(self._simple_list)

        # print("value_lcs:", handle)
        # logger.info(str)
        print('===============')
        for i in mutation_data_dic:
            # print('--------------------')
            var_data = mutation_data_dic[i]
            # logger.info(len(var_data))
            # logger.info(var_data)
        self.write_value(handle, mutation_data_dic)              
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
                #print(str(handle) + "只有一个输入" + valu )
                self.find_lcseque(handle, valu[0], valu[0])                        # 使用变异后的{handle：[v1,v2]}填充字典
            elif len(valu) == 0:                                                   # 处理pcap包中没有的handle fuzz
                # print("fuzz pcap中没有的handle")                                    
                self.pro_a_hand(handle)                                         
            else:
                for i in range(len(valu)):
                    for j in range(len(valu)):
                        if len(valu[i]) == len(valu[j]):        # 包括一次重放
                            print('-'*60)
                            self.find_lcseque(handle, valu[i],valu[j])            

        logger.info("--变异完成--")
        return self.Muta_dic                                                        # 返回变异后字典          



    def write_value(self, handle, dic):
        shx = sorted(dic.keys())
        dic_shx = {}
        for sx in shx:
            dic_shx[sx] = dic[sx]
        after_var_value = self.fn(dic_shx)
        

        # print("muta handle:", handle)
        # print("muta after_var_value:", type(after_var_value))
        if not bool(self.Muta_dic):
            self.Muta_dic[handle] = after_var_value
        # elif self.Muta_dic[handle] == []:
        #     print("handle value:", self.Muta_dic[handle])
        #     self.Muta_dic[handle] = after_var_value
        elif handle not in self.Muta_dic.keys():
            #print(self.Muta_dic.keys()) 
            self.Muta_dic[handle] = after_var_value      #   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        else:
            self.Muta_dic[handle] = self.Muta_dic[handle] + after_var_value
        # logger.info("mula_dic:")

        # return handle, after_var_value
        # self.write_to_handle(handle, after_var_value)
                        
                        
    # def write_var(self, mac, handle, dic):                           #按行写入
    #     shx = sorted(dic.keys())
    #     dic_shx = {}
    #     for sx in shx:
    #         dic_shx[sx] = dic[sx]
    #     after_var_value = self.fn(dic_shx)
    #     self.write_to_handle(mac, handle, after_var_value)
    #     # return handle, after_var_value
        

    # def write_to_handle(self,  handle, after_var_value):
    #     ble = BLEWrite()
    #     self.path = './'+ str(handle) +'.csv'                               #把变异数据写入./fuzz_data.csv 
        
    #     mac = 'b4:60:ed:99:1f:34'
    #     with open(self.path, 'w+', newline='') as f:
    #         csv_doc = csv.writer(f)
    #         for k in after_var_value:
    #             self.wri_handle( mac, k, handle)                #mac, value, handle
    #             print("write value："+ str(k) + "to handle:"+str(handle)) 
    #             #k = k.decode(encoding="utf-8").replace('|', '')
    #             try:
    #                 csv_doc.writerow(k)
    #             except:
    #                 continue
                          

    def fn(self, dict):
        lists = list(dict.values())    
        from functools import reduce
            
        def myfunc(list1, list2):
            return [str(i)+str(j) for i in list1 for j in list2]
        return reduce(myfunc, lists)



    def var_no_pcap(self, handlelist):
        for handle in handlelist:
            after_strs = self.string_mutator.bad_strs_list() + self.string_mutator.get_payload_mutation(2) + self.string_mutator.get_payload_mutation(4) + self.string_mutator.get_payload_mutation(6) + self.string_mutator.get_payload_mutation(8) + self.string_mutator.get_payload_mutation(10) + self.string_mutator.get_payload_mutation(12) + self.string_mutator.get_payload_mutation(20)
            self.Muta_dic[handle] = after_strs
        return self.Muta_dic
        
    def pro_a_hand(self, hand):
        after_strs = self.string_mutator.bad_strs_list() + self.string_mutator.get_payload_mutation(2) + self.string_mutator.get_payload_mutation(4) + self.string_mutator.get_payload_mutation(6) + self.string_mutator.get_payload_mutation(8) + self.string_mutator.get_payload_mutation(10) + self.string_mutator.get_payload_mutation(12) + self.string_mutator.get_payload_mutation(20)
        self.Muta_dic[hand] = after_strs


    # def wri_handle(self, mac, val, hand):
    #     conn = Peripheral(mac)
    #     if type(val) != bytes:
    #         val = val.encode()
    #     try:
    #         conn.writeCharacteristic(hand, val, withResponse=None)                ## python3.*  type(val)=byte
    #         print("write:" + str(val) +"      to:" + str(hand) )
    #     except BTLEException  as ex:
    #         print(ex)


# if __name__ == '__main__':
#     s1 = '125678'
#     s2 = '129906'

#     test_dic={'23':['123456','123357'], '24':[]}
    # val = ValueLCS()
#     Muta_di = val.pro_dict(test_dic)
#     print(Muta_di)
    # t1_s = time.time()
    # val.find_lcseque(11, s1, s2)
    # t1_e = time.time()

    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # t2_s = time.time()
    # val.find_lcseque_with_lcs_rule(val.get_lcs_rule(s1, s2), s1, s2)
    # t2_e = time.time()

    # logger.info(t1_e - t1_s)
    # logger.info(t2_e - t2_s)

    # s1 = '00'
    # s2 = '11'

    # s= val.get_lcs_rule(s1,s2)
    # print(s)


