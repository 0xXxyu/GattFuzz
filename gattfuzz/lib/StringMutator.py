import random as ran
import binascii


class StringMutator():

    '''

    变异规则：
    1. 边界测试； 0填充/最高位填充
    2. 坏字符串输入；
    3. 列表遍历；
    4. 列表随机输入；
    5. 随机输入。

    # 1和5合为size*16次随机字符串输入
    # 2调用坏字符串列表

    # add payload
    
    '''

    def __init__(self):
        self.bad_strs = [
                    "!@#$%%^#$%#$@#$%$$@#$%^^**(()",
                "", 
                "$(reboot)",
                "$;reboot",
                "%00",
                "%00/",
                '%0DCMD=$"reboot";$CMD',
                "%0Dreboot",
                "%n" * 500,
                "%s" * 100,
                "%s" * 500,
                "%u0000",
                "& reboot &",
                "& reboot",
                "&&CMD=$'reboot';$CMD",
                '&&CMD=$"reboot";$CMD',
                "&&reboot",
                "&&reboot&&",
                "..:..:..:..:..:..:..:..:..:..:..:..:..:",
                "/%00/",
                "/." * 5000,
                "/.../" + "B" * 5000 + "\x00\x00",
                "/.../.../.../.../.../.../.../.../.../.../",
                "/../../../../../../../../../../../../boot.ini",
                "/../../../../../../../../../../../../etc/passwd",
                "/.:/" + "A" * 5000 + "\x00\x00",
                "/\\" * 5000,
                "/index.html|reboot|",
                "; reboot",
                ";CMD=$'reboot';$CMD",
                ';CMD=$"reboot";$CMD',
                ";id",
                "id",
                ",id",
                ";id",
                ";id;",
                "'id'",
                "''id",
                "''id''",
                "''id''&",
                "*id",
                "*id*",
                "**id**",
                "(id)",
                "`id`",
                "`id`&",
                "`id` &",
                ""
                ]

    def bad_strs_list(self):
        encoded_bad_str_list = []
        for st in self.bad_strs:
            s = st.encode()
            encoded_bad_str_list.append(s)
        return encoded_bad_str_list 


    #def __init__(self):
        #self.path = './fuzz_data.csv'                               #把变异数据写入./fuzz_data.csv    
        # with open(self.path, 'wb') as fs:                           #其中包括填充数据'NULL'，使用时需要去除
        #     csv_writ = csv.writer(fs)
        #     csv_head = ["payload", "simple", "string", "count"]
        #     csv_writ.writerow(csv_head)
        
        

    def get_payload_mutation(self, size):         #payload 随机数填充+边界填充
        min = 0
        max = int('f'*size, 16)               #转为10进制数据

        payload_mutation_record = []
        for n in range(16*size):
            data = "".join([ran.choice("0123456789ABCDEF") for i in range(size)])
            data = data.encode()
            payload_mutation_record.append(data)

        return payload_mutation_record

        '''
        with open(self.path, 'a+') as fs: 
            csv_writ = csv.writer(fs)           
            csv_writ.writerows[
                {"payload":min, "simple":'NULL', "string":'NULL', "count":'NULL'},
                {"payload":max, "simple":'NULL', "string":'NULL', "count":'NULL'},
                ]
            for n in range(16*size):
                data = "".join([choice("0123456789ABCDEF") for i in range(size)])
                csv_writ.writerow([data, 'NULL', 'NULL', 'NULL'])
            '''
    # def simple_var(sim_list):             # 2字节数据
    #     py_list = ['NULL']*len(sim_list)
    #     str_list = ['NULL']*len(sim_list)
    #     count_list = ['NULL']*len(sim_list)

    #     csv_write = pd.DataFrame({"payload":py_list, "simple":sim_list, "string":str_list, "count":count_list})
    #     csv_write.to_csv(self.path)

    def get_string_mutation(self, str_len):           #坏字符串填充
        bad_strs = [
            "!@#$%%^#$%#$@#$%$$@#$%^^**(()",
        "", 
        "$(reboot)",
        "$;reboot",
        "%00",
        "%00/",
        '%0DCMD=$"reboot";$CMD',
        "%0Dreboot",
        "%n" * 500,
        "%s" * 100,
        "%s" * 500,
        "%u0000",
        "& reboot &",
        "& reboot",
        "&&CMD=$'reboot';$CMD",
        '&&CMD=$"reboot";$CMD',
        "&&reboot",
        "&&reboot&&",
        "..:..:..:..:..:..:..:..:..:..:..:..:..:",
        "/%00/",
        "/." * 5000,
        "/.../" + "B" * 5000 + "\x00\x00",
        "/.../.../.../.../.../.../.../.../.../.../",
        "/../../../../../../../../../../../../boot.ini",
        "/../../../../../../../../../../../../etc/passwd",
        "/.:/" + "A" * 5000 + "\x00\x00",
        "/\\" * 5000,
        "/index.html|reboot|",
        "; reboot",
        ";CMD=$'reboot';$CMD",
        ';CMD=$"reboot";$CMD',
        ";id",
        ]

        bad_str_mutation_record = []
        for bad_str in bad_strs:
            if len(bad_str.encode()) <= str_len*2:
                st = bad_str.encode()+(str_len*2-len(bad_str.encode()))*b'0'
                bad_str_mutation_record.append(st)
        return bad_str_mutation_record

        '''
        py_list = ['NULL']*len(bad_str)
        sim_list = ['NULL']*len(bad_str)
        count_list = ['NULL']*len(bad_str)
            
        csv_write = pd.DataFrame({"payload":py_list, "simple":sim_list, "string":bad_str, "count":count_list})
        csv_write.to_csv(self.path)
        '''
    def get_count_mutation(self, count_str):      #count 边界填充+有界数填充          
        count_len  = len(count_str)
        count_min = '0' * count_len               #count 取00和ff
        count_max = 'f' * count_len

        count_mutation_record = []
        count_mutation_record.append(count_min.encode())
        count_mutation_record.append(count_max.encode())

        for n in range(count_len * 16):
            count_random = ran.randint(int(count_str, 16), int(count_max, 16))
            count_hex = str(hex(count_random)).replace('0x','')
            count_mutated = count_hex.encode()
            count_mutation_record.append(count_mutated)
                   
        return count_mutation_record

        '''
        with open(self.path, 'a+') as fs: 
            csv_writ = csv.writer(fs)  
            csv_writ.writerows[
                {"payload":'NULL', "simple":'NULL', "string":'NULL', "count":count_min},
                {"payload":'NULL', "simple":'NULL', "string":'NULL', "count":count_max},
                ]
            for n in range(le*16):
                count = ran.randint(int(str,16), int(count_max, 16))
                csv_writ.writerow(['NULL', 'NULL', 'NULL', count])
                '''

    def calculate_crc32(data):
        crc = binascii.crc32(data) & 0xffffffff
        return crc


    def input_list(self, list_path):
        # 接收外部bad string 输入
        add_strings = []
        f = open(list_path,'r')
        for add_str in f.readlines():
            add_str = add_str.strip('\n')
            add_strings.append(add_str)

        self.bad_strs = add_strings + self.bad_strs

        # print("更新后列表:", self.bad_strs)

