import csv
from itertools import count
from pickletools import pylist
import random as ran
#import pandas as pd

class Var_string():

    '''

    变异规则：
    1. 边界测试； 0填充/最高位填充
    2. 坏字符串输入；
    3. 列表遍历；
    4. 列表随机输入；
    5. 随机输入。

    # 1和5合为size*16次随机字符串输入
    # 2调用坏字符串列表
    
    '''
    def bad_strs_list(self):

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
            ]
        bad_str_list = []
        for st in bad_strs:
            s = st.encode()
            bad_str_list.append(s)

        
        return bad_str_list 


    #def __init__(self):
        #self.path = './fuzz_data.csv'                               #把变异数据写入./fuzz_data.csv    
        # with open(self.path, 'wb') as fs:                           #其中包括填充数据'NULL'，使用时需要去除
        #     csv_writ = csv.writer(fs)
        #     csv_head = ["pyload", "simple", "string", "count"]
        #     csv_writ.writerow(csv_head)
        
        

    def pyload_var(self, size):         #pyload 随机数填充+边界填充
        min = 0
        max = int('f'*size, 16)               #转为10进制数据

        pyload_list = []
        for n in range(16*size):
            data = "".join([ran.choice("0123456789ABCDEF") for i in range(size)])
            data = data.encode()
            pyload_list.append(data)

        return pyload_list

        '''
        with open(self.path, 'a+') as fs: 
            csv_writ = csv.writer(fs)           
            csv_writ.writerows[
                {"pyload":min, "simple":'NULL', "string":'NULL', "count":'NULL'},
                {"pyload":max, "simple":'NULL', "string":'NULL', "count":'NULL'},
                ]
            for n in range(16*size):
                data = "".join([choice("0123456789ABCDEF") for i in range(size)])
                csv_writ.writerow([data, 'NULL', 'NULL', 'NULL'])
            '''

    # def simple_var(sim_list):             # 2字节数据
    #     py_list = ['NULL']*len(sim_list)
    #     str_list = ['NULL']*len(sim_list)
    #     count_list = ['NULL']*len(sim_list)

    #     csv_write = pd.DataFrame({"pyload":py_list, "simple":sim_list, "string":str_list, "count":count_list})
    #     csv_write.to_csv(self.path)

    def string_var(self, str_len):           #坏字符串填充
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
        bad_str_all = []
        for bad_str in bad_strs:
            if len(bad_str.encode()) <= str_len*2:
                st = bad_str.encode()+(str_len*2-len(bad_str.encode()))*b'0'
                bad_str_all.append(st)
        return bad_str_all

        '''
        py_list = ['NULL']*len(bad_str)
        sim_list = ['NULL']*len(bad_str)
        count_list = ['NULL']*len(bad_str)
            
        csv_write = pd.DataFrame({"pyload":py_list, "simple":sim_list, "string":bad_str, "count":count_list})
        csv_write.to_csv(self.path)
        '''
    def count_var(self,count_str):      #count 边界填充+有界数填充          
        le = len(count_str)
        count_min = '0'*le               #count 取00和ff
        count_max = 'f'*le

        cont_list = []
        cont_list.append(count_min.encode())
        cont_list.append(count_max.encode())
        for n in range(le*16):
            coun = ran.randint(int(count_str,16), int(count_max, 16))
            c = str(hex(coun)).replace('0x','')
            count = c.encode()
            cont_list.append(count)
                   
        return cont_list

        '''
        with open(self.path, 'a+') as fs: 
            csv_writ = csv.writer(fs)  
            csv_writ.writerows[
                {"pyload":'NULL', "simple":'NULL', "string":'NULL', "count":count_min},
                {"pyload":'NULL', "simple":'NULL', "string":'NULL', "count":count_max},
                ]
            for n in range(le*16):
                count = ran.randint(int(str,16), int(count_max, 16))
                csv_writ.writerow(['NULL', 'NULL', 'NULL', count])
                '''

