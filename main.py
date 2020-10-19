import bitstring
import logic

logic.set_message('ЮЩЕ')
print('Сообщение:', logic.get_message())
logic.append_padding_bits()
print('Дописываем 1 бит, а затем добавляем 0:', logic.get_message())
logic.append_length()
print('Дописываем 64-битное представление длины сообщения:', logic.get_message())

logic.const_table_init()
logic.message_blocks_init()
A = logic.get_a0()
B = logic.get_b0()
C = logic.get_c0()
D = logic.get_d0()

for i in range(64):
    F = 0
    g = 0
    if 0 <= i <= 15:
        F = logic.fun_f(B, C, D)
        g = i
    elif 16 <= i <= 31:
        F = logic.fun_g(B, C, D)
        g = (5 * i + 1) % 16
    elif 32 <= i <= 47:
        F = logic.fun_h(B, C, D)
        g = (3 * i + 5) % 16
    elif 48 <= i <= 63:
        F = logic.fun_i(B, C, D)
        g = (7 * i) % 16
    F = bitstring.BitArray(uint=((F.int + A.int + logic.get_const_table(i).int + logic.get_block(g).int) % 0xffffffff),
                           length=32)
    A = D
    D = C
    C = B
    B = bitstring.BitArray(uint=((B.int + (F << logic.get_shift(i)).int) % 0xffffffff), length=32)
    print(f'Раунд {(i + 16) // 16}, итерация {(i + 1) % 16}.', A.hex, B.hex, C.hex, D.hex)
logic.set_a0(bitstring.BitArray(uint=((logic.get_a0().int + A.int) % 0xffffffff), length=32))
logic.set_b0(bitstring.BitArray(uint=((logic.get_b0().int + B.int) % 0xffffffff), length=32))
logic.set_c0(bitstring.BitArray(uint=((logic.get_c0().int + C.int) % 0xffffffff), length=32))
logic.set_d0(bitstring.BitArray(uint=((logic.get_d0().int + D.int) % 0xffffffff), length=32))
print(logic.get_a0(), logic.get_b0(), logic.get_c0(), logic.get_d0())
digest = bitstring.BitArray(f'0b{logic.get_a0().bin + logic.get_b0().bin + logic.get_c0().bin + logic.get_d0().bin}')
print(digest.hex)
