from pwn import *

context.arch = 'amd64'

elf = ELF("./fullchain")
g = elf.symbols['__libc_csu_init']
# got_exit = elf.got["gets"]
# print((got_exit - g) / 8)
print(elf.got)
