
import binascii
import time

# h = '0029'
# m = int(h, 16)
# print(m)

# handl = b'\x02\x18\x00\x81A1:\xf2\x86[\x9e\x9aE\x16^\x05@nJ'
# s = binascii.hexlify(binascii.unhexlify(handl)[::-1])
# print("大端：")

s = ';CMD=$"reboot";$CMD'
tch = b'0'

#print(s.encode()+tch*2)

if len(s) <= 22:
    #print(s.encode+2*tch)
    print(s.encode()+tch*(22-len(s.encode())))