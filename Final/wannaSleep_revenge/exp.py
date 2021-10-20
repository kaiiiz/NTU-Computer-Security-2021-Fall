import string
import os

with open("wannasleeeeeeep.txt.enc", "rb") as f:
    ans = f.read()

with open("in", "r") as f:
    plaintext = f.read()

def check_correct(out):
    for i in range(len(out)-4):
        if out[i] != ans[i]:
            return False
    return True

while True:
    print(len(plaintext))
    for c in string.printable:
        try_plaintext = plaintext + c
        with open("in_tmp", "w") as f:
            f.write(try_plaintext)

        os.system("wannaSleep_revenge.exe in_tmp")

        with open("in_tmp.enc", "rb") as f:
            out2 = f.read()

        os.system("del in_tmp.enc")

        if check_correct(out2):
            print("hit!", c)
            plaintext = try_plaintext
            break
        else:
            print(len(try_plaintext), c, "not correct")
    
    with open("in", "w") as f:
        f.write(try_plaintext)

