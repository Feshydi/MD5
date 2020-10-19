import math
import numpy as np
import bitstring
import codecs

# a0 = bitstring.BitArray('0x01234567')
# b0 = bitstring.BitArray('0x89abcdef')
# c0 = bitstring.BitArray('0xfedcba98')
# d0 = bitstring.BitArray('0x76543210')
a0 = bitstring.BitArray('0x67452301')
b0 = bitstring.BitArray('0xefcdab89')
c0 = bitstring.BitArray('0x98badcfe')
d0 = bitstring.BitArray('0x10325476')

s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
     5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
     4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
     6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

T = {}

M = {}

bit_message = bitstring.BitArray('0b0')
message_len = 0


def fun_f(x, y, z):
    """
    Принимает 3 одноразмерные логические переменные: x, y, z
    Возвращает логическую функция для раунда 1
    """
    return (x & y) | (~x & z)


def fun_g(x, y, z):
    """
    Принимает 3 одноразмерные логические переменные: x, y, z
    Возвращает логическую функция для раунда 2
    """
    return (x & z) | (~z & y)


def fun_h(x, y, z):
    """
    Принимает 3 одноразмерные логические переменные: x, y, z
    Возвращает логическую функция для раунда 3
    """
    return x ^ y ^ z


def fun_i(x, y, z):
    """
    Принимает 3 одноразмерные логические переменные: x, y, z
    Возвращает логическую функция для раунда 4
    """
    return y ^ (~z | x)


def get_a0():
    """ Возвращает буфер A """
    return a0


def get_b0():
    """ Возвращает буфер B """
    return b0


def get_c0():
    """ Возвращает буфер C """
    return c0


def get_d0():
    """ Возвращает буфер D """
    return d0


def get_shift(iteration_num):
    """
    Принимает номер итерации
    Возвращает соответствующий циклический сдвиг
    """
    return s[iteration_num]


def const_table_init():
    """
    Инициализирует таблицу констант T
    """
    for i in range(64):
        tmp = np.uint32(2 ** 32 * math.fabs(math.sin(i + 1)))
        T[i] = bitstring.BitArray(uint=tmp, length=32)


def get_const_table(iteration_num):
    """
    Принимает номер итерации
    Возвращает соответствующую константу
    """
    return T[iteration_num]


def set_message(message):
    """
    Принимает сообщение
    Записывает в переменную типа BitArray
    Записывает длинну начального сообщения
    """
    global bit_message, message_len
    message_c = codecs.encode(message, encoding='cp1251')
    bit_message = bitstring.BitArray(message_c)
    message_len = bitstring.BitArray(int=len(get_message()), length=8)


def update_message(tmp):
    """
    Принимает переменную типа BitArray
    Дописывает биты в конец сообщения
    """
    global bit_message
    bit_message += tmp


def get_message():
    """
    Возвращает обрабатываемую переменную типа BitArray
    """
    return bit_message


def append_padding_bits():
    """
    Выравнивает поток, пока его длинна не будет равна 448 по модулю 512
    """
    update_message('0x80')
    print(get_message())
    while len(get_message()) % 512 != 448:
        update_message('0x00')


def append_length():
    """
    Добавление 64-битного представления длины данных
    """
    update_message(message_len)
    while len(get_message()) < 512:
        update_message('0x00')


def message_blocks_init():
    i = 0
    for nibble in bit_message.cut(32):
        M[i] = nibble
        i += 1

# i = 0
# for nibble in bit_message.cut(32):
#     M[i] = nibble
#     i += 1

# for i in range(64):
#     F = 0
#     g = 0
#     if 0 <= i <= 15:
#         F = fun_f(B, C, D)
#         g = i
#     elif 16 <= i <= 31:
#         F = fun_g(B, C, D)
#         g = (5 * i + 1) % 16
#     elif 32 <= i <= 47:
#         F = fun_h(B, C, D)
#         g = (3 * i + 5) % 16
#     elif 48 <= i <= 63:
#         F = fun_i(B, C, D)
#         g = (7 * i) % 16
#     F = bitstring.BitArray(uint=((F.int + A.int + T[i].int + M[g].int) % 0xffffffff), length=32)
#     A = D
#     D = C
#     C = B
#     B = bitstring.BitArray(uint=((B.int + (F << s[i]).int) % 0xffffffff), length=32)
#     print(f'Раунд {(i + 16) // 16}, итерация {(i + 1) % 16}.', A.hex, B.hex, C.hex, D.hex)
# a0 = bitstring.BitArray(uint=((a0.int + A.int) % 0xffffffff), length=32)
# b0 = bitstring.BitArray(uint=((b0.int + B.int) % 0xffffffff), length=32)
# c0 = bitstring.BitArray(uint=((c0.int + C.int) % 0xffffffff), length=32)
# d0 = bitstring.BitArray(uint=((d0.int + D.int) % 0xffffffff), length=32)
# print(a0, b0, c0, d0)
# digest = bitstring.BitArray(f'0b{a0.bin + b0.bin + c0.bin + d0.bin}')
# print(digest.hex)
