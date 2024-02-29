#!/usr/bin/env python3

from pwn import *

exe = ELF("notes_patched")
libc = ELF("libc.so.6")
ld = ELF("./ld-2.35.so")


p = process(exe.path) 
p.sendlineafter("Choice:", "\0/bin/sh\0")
# good luck pwning :)

p.interactive()


