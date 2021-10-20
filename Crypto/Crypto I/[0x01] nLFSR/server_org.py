#!/bin/env python3 -u
import os


state = 1
poly = 0xaa0d3a677e1be0bf
def step():
    global state
    out = state & 1
    state >>= 1
    if out:
        state ^= poly
    return out
    

def random():
    for _ in range(42):
        step()
    return step()


money = 1.2
while money > 0:
    y = random()
    x = int(input('> '))
    if x == y:
        money += 0.02
    else:
        money -= 0.04
    print(money)
    if money > 2.4:
        print("Here's your flag:")
        with open('./flag.txt') as f:
            print(f.read())
        exit(0)
print('E( G_G)')