import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random.random import getrandbits

FLAG = b"FLAG{????????????????????????????????????????}"


class LFSR:
    def __init__(self, key, taps):
        d = max(taps)
        assert len(key) == d, "Error: key of wrong size."
        self._s = key
        self._t = [d - t for t in taps]

    def _sum(self, L):
        s = 0
        for x in L:
            s ^= x
        return s

    def _clock(self):
        b = self._s[0]
        self._s = self._s[1:] + [self._sum(self._s[p] for p in self._t)]
        return b

    def getbit(self):
        return self._clock()


class Geffe:
    def __init__(self, key):
        assert key.bit_length() <= 19 + 23 + 27 # shard up 69+ bit key for 3 separate lfsrs
        key = [int(i) for i in list("{:069b}".format(key))] # convert int to list of bits
        self.LFSR = [
            LFSR(key[:19], [19, 18, 17, 14]),
            LFSR(key[19:46], [27, 26, 25, 22]),
            LFSR(key[46:], [23, 22, 20, 18]),
        ]

    def getbit(self):
        b = [lfsr.getbit() for lfsr in self.LFSR]
        return b[1] if b[0] else b[2]


def encrypt_flag(key):
    sha1 = hashlib.sha1()
    sha1.update(str(key).encode('ascii'))
    key = sha1.digest()[:16]
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    data = {}
    data['iv'] = iv.hex()
    data['encrypted_flag'] = ciphertext.hex()
    return data


key = getrandbits(69)
J = Geffe(key)
stream = [J.getbit() for _ in range(256)]
print(stream)
print(encrypt_flag(key))
