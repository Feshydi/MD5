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


def set_a0(value):
    """ Принимает значени и устанавливает его в буфер A """
    global a0
    a0 = value


def set_b0(value):
    """ Принимает значени и устанавливает его в буфер B """
    global b0
    b0 = value


def set_c0(value):
    """ Принимает значени и устанавливает его в буфер C """
    global c0
    c0 = value


def set_d0(value):
    """ Принимает значени и устанавливает его в буфер D """
    global d0
    d0 = value


def get_shift(iteration_num):
    """
    Принимает номер итерации
    Возвращает соответствующий циклический сдвиг
    """
    return s[iteration_num]


def const_table_init():
    """ Инициализирует таблицу констант T """
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
    """ Возвращает обрабатываемую переменную типа BitArray """
    return bit_message


def append_padding_bits():
    """ Выравнивает поток, пока его длинна не будет равна 448 по модулю 512 """
    update_message('0x80')
    print(get_message())
    while len(get_message()) % 512 != 448:
        update_message('0x00')


def append_length():
    """ Добавление 64-битного представления длины данных """
    update_message(message_len)
    while len(get_message()) < 512:
        update_message('0x00')


def message_blocks_init():
    """ Разбивает 512-битный блок на массив из 16 слов по 32 бита """
    i = 0
    for nibble in bit_message.cut(32):
        M[i] = nibble
        i += 1


def get_block(iteration_num):
    """
    Принимает номер итерации
    Возвращает соответствующий 32-битный блок
    """
    return M[iteration_num]
