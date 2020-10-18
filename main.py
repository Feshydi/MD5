import math
import numpy as np
import bitstring
import prettytable


def fun_f(x, y, z):
    return (x & y) | (~x & z)


def fun_g(x, y, z):
    return (x & z) | (~z & y)


def fun_h(x, y, z):
    return x ^ y ^ z


def fun_i(x, y, z):
    return y ^ (~z | x)


a0 = bitstring.BitArray('0x67452301')
b0 = bitstring.BitArray('0xefcdab89')
c0 = bitstring.BitArray('0x98badcfe')
d0 = bitstring.BitArray('0x10325476')

s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
     5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
     4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
     6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

T = {}
for i in range(64):
    tmp = np.uint32(2 ** 32 * math.fabs(math.sin(i + 1)))
    T[i] = bitstring.BitArray(uint=tmp, length=32)

string = bitstring.BitArray('0b110111101101100111000101')
print('Сообщение:', string.hex)

str_len = bitstring.BitArray(int=len(string), length=8)
string += '0x80'
while len(string) % 512 != 448:
    string += '0x00'
print('Дописываем 1 бит, а затем добавляем 0:', string.hex)

string += f'0b{str_len.bin}'
while len(string) < 512:
    string += '0x00'
print('Дописываем 64-битное представление длины сообщения:', string.hex)

A = a0
B = b0
C = c0
D = d0

M = {}
i = 0
for nibble in string.cut(32):
    M[i] = nibble
    i += 1

for i in range(64):
    F = 0
    g = 0
    if 0 <= i <= 15:
        F = fun_f(B, C, D)
        g = i
    elif 16 <= i <= 31:
        F = fun_g(B, C, D)
        g = (5 * i + 1) % 16
    elif 32 <= i <= 47:
        F = fun_h(B, C, D)
        g = (3 * i + 5) % 16
    elif 48 <= i <= 63:
        F = fun_i(B, C, D)
        g = (7 * i) % 16
    F = bitstring.BitArray(uint=((F.int + A.int + T[i].int + M[g].int) % 0xffffffff), length=32)
    A = D
    D = C
    C = B
    B = bitstring.BitArray(uint=((B.int + (F << s[i]).int) % 0xffffffff), length=32)
    print(f'Раунд {(i + 16) // 16}, итерация {(i + 1) % 16}.', A.hex, B.hex, C.hex, D.hex)
a0 = bitstring.BitArray(uint=((a0.int + A.int) % 0xffffffff), length=32)
b0 = bitstring.BitArray(uint=((b0.int + B.int) % 0xffffffff), length=32)
c0 = bitstring.BitArray(uint=((c0.int + C.int) % 0xffffffff), length=32)
d0 = bitstring.BitArray(uint=((d0.int + D.int) % 0xffffffff), length=32)
digest = bitstring.BitArray(f'0b{a0.bin + b0.bin + c0.bin + d0.bin}')
print(digest.hex)
