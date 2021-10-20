#!/usr/bin/python3
import tempfile
import os
import sys

exp_len = int(input('your exploit len> '))
exp_data = sys.stdin.read(exp_len)

with tempfile.NamedTemporaryFile('w') as f:
    f.write(exp_data)
    f.flush()
    os.system(f"./d8 {f.name}")
