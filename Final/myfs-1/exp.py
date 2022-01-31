#!/usr/bin/env python3

from pwn import *

context.terminal = ['tmux', 'split', '-h']
context.arch = 'amd64'
context.binary = "/home/myfs/myfs"
# context.log_level = "debug"

# p = process("./fullchain-buff")
p = gdb.debug("/home/myfs/myfs", """
b mock
b *mock+687
""")

p.interactive()
