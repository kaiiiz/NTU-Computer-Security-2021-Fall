from pwn import *

r = remote('edu-ctf.csie.org', 42069)
money = 1.2

def guess(ans):
    global money, r
    
    r.sendlineafter(b"> ", f"{ans}".encode())
    cur_money = float(r.recvline().decode().strip())
    diff = cur_money - money
    if abs(diff - (-0.04)) < 1e-4: # lose
        ans = 1

    money = cur_money
    return ans, money

def get_64_ans():
    first_64_ans = []
    for _ in range(64):
        ans, money = guess(0)
        first_64_ans.append(ans)
    return first_64_ans

def get_init_state(first_64_ans):
    poly = f'{0xaa0d3a677e1be0bf:0>64b}'

    P.<x> = PolynomialRing(GF(2))
    P = x^64

    for i, t in enumerate(poly):
        if t == '1':
            P += x^i

    C = companion_matrix(P, format='left')

    M = Matrix(GF(2), 64)
    V = vector(GF(2), 64)
    D = C ^ 43

    for idx, ans in enumerate(first_64_ans):
        M[idx] = (D ^ (idx+1))[0]
        V[idx] = ans

    init_state = M ^ -1 * V

    return init_state, D

def recover_state(init_state, step):
    s = init_state
    for _ in range(64):
        s = step * s
    return s

def solve():
    first_64_ans = get_64_ans()
    print(f"First 64 ans: {first_64_ans}")

    init_state, step = get_init_state(first_64_ans)
    state = recover_state(init_state, step)

    while True:
        try:
            state = step * state
            ans, money = guess(state[0])
            print(ans, money)
        except EOFError:
            break

    print(r.recvline().decode())
    print(r.recvline().decode())
    
solve()