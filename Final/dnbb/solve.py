import socket
import base64
import hashlib

# code = b'u557357e0ec0c8fbb7b529fe37852b765557357e0ec0c8fbb7b529fe37852b76'
# print(base64.b64encode(code))
# print(len(code)*8)
# print(hashlib.sha256(b'mfdYthgrxkiH4IfzZKBFEe8CJanxPPyD').hexdigest())
# HOST = '127.0.0.1'
# PORT = 5566
# with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
#     s.connect((HOST,PORT))
#     # s.send(b"\x40\x24\x00\x00\x00\x71\x59\x6a\x6d\x16\x53\x10\x16\x3f\x40\x42\x38\x75\x5d\x01\x42\x0c\x04\x5c\x16\x12\x6b\x4d\x17\x05\x5a\x17\x56\x4a\x5b\x47\x45\x1c\x17\x4e\x4c")
#     # data = s.recv(1024)
#     # print('%s',(data))
#     s.close()

with open("dnbd.exe", "rb") as f:
    a = f.read()

with open("TOHOST", "rb") as f:
    b = f.read()

print(len(a), len(b), len(b)-len(a))

c = []

for i in range(len(a)):
    # print(a[i], b[i], a[i]^b[i], chr(a[i]^b[i]))
    c.append(chr(a[i]^b[i+480]))

with open('out', 'wb') as f:
    f.write("".join(c).encode())