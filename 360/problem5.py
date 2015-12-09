
__author__="F4nt45i4-ZHG"
import struct
for i in range(1, 9):
    with open('b' + str(i) + '.txt', 'wb') as w:
        with open('b.txt', 'r') as r:
            for l in r.readlines():
                t = 0
                a = 1
                for j in range(1, 9):
                    if j != i:
                        if l[j] == '1':
                            t += a
                        a <<= 1
                print(t)
                w.write(struct.pack('1B', t))
