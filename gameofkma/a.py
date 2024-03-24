#!/usr/bin/python3
from pwn import *
from ctypes import CDLL

libc = CDLL("./libc.so.6")
libc.srand(libc.time(0))
print(str(libc.rand()))
