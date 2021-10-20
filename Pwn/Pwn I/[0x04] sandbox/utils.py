from pwn import *

context.arch = 'amd64'

sc = {
    "a": b"H\xbc\xb8\xb8\xb8\xb8\xb8\xb8\xb8\xb8",
    "b": b"H\xbd\xb8\xb8\xb8\xb8\xb8\xb8\xb8\xb8",
    "epilogue": b"H\xc7\xc0<\x00\x00\x00\x0f\x05",
    "syscall_pattern": b"\x0f\x05",
    "mov_r8_prefix": b"I\xb8\xb8\xb8\xb8\xb8\xb8\xb8\xb8\xb8",
    "call_r8": b"A\xff\xd0",
    "call_reg_patterns[0]": b"\xff\xd0",
    "call_reg_patterns[1]": b"\xff\xd3",
    "call_reg_patterns[2]": b"\xff\xd1",
    "call_reg_patterns[3]": b"\xff\xd2",
    "call_reg_patterns[4]": b"\xff\xd7",
    "call_reg_patterns[5]": b"\xff\xd6",
    "call_reg_patterns[6]": b"A\xff\xd0",
    "call_reg_patterns[7]": b"A\xff\xd1",
    "call_reg_patterns[8]": b"A\xff\xd2",
    "call_reg_patterns[9]": b"A\xff\xd3",
    "call_reg_patterns[10]": b"A\xff\xd4",
    "call_reg_patterns[11]": b"A\xff\xd5",
    "call_reg_patterns[12]": b"A\xff\xd6",
    "call_reg_patterns[13]": b"A\xff\xd7",
}

for k, v in sc.items():
    print("---", k)
    print(disasm(v))
