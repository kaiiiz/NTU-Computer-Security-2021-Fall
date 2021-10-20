#!/usr/bin/env python3
import os
from Crypto.Cipher import AES

key = os.urandom(16)
with open('flag', 'rb') as f:
    flag = f.read()

class PaddingError(Exception):
    pass

def pad(data):
    padlen = 16 - len(data) % 16
    return data + int('1' + '0' * (padlen * 8 - 1), 2).to_bytes(padlen, 'big')

def unpad(data):
    for i in range(len(data) - 1, len(data) - 1 - 16, -1):
        if data[i] == 0x80:
            return data[:i]
        elif data[i] != 0x00:
            raise PaddingError
    raise PaddingError

def encrypt(plain):
    # random iv
    iv = os.urandom(16)
    # encrypt
    aes = AES.new(key, AES.MODE_CBC, iv) 
    cipher = aes.encrypt(pad(plain))
    return iv + cipher

def decrypt(cipher):
    # split iv, cipher
    iv, cipher = cipher[:16], cipher[16:]
    # decrypt
    aes = AES.new(key, AES.MODE_CBC, iv) 
    plain = aes.decrypt(cipher)
    return unpad(plain)

def main():
    print(f'cipher = {encrypt(flag).hex()}')
    while True:
        try:
            decrypt(bytes.fromhex(input('cipher = ')))
            print('YESSSSSSSS')
        except PaddingError:
            print('NOOOOOOOOO')
        except:
            return

if __name__ == '__main__':
    main()
