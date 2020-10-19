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
