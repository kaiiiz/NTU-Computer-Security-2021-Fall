user_cnt = 0
addr_log = {}
has_parse_user = False
line_is_user = False

def parse_addr(line):
    return line.split()[0]

with open('log', 'r') as f:
    for i, cmd in enumerate(f.read().split("pwndbg>")):
        if 'print users' in cmd:
            users = cmd.split('\n')[1].split("{")[1].split("}")[0].split(', ')
            for i, u in enumerate(users):
                if u not in addr_log:
                    addr_log[u] = []
                addr_log[u].append(f"users{i}")
            continue

        if " = {" in cmd:
            cmd_line = cmd.split("\n")
            def p(s):
                return s.strip(" ,").split(" ")[2]

            def add(useri, addr, type):
                if addr not in addr_log:
                    addr_log[addr] = []
                addr_log[addr].append(f"user{useri}.{type}")

            name = p(cmd_line[2])
            desc = p(cmd_line[3])
            job = p(cmd_line[4])
            fifo0 = p(cmd_line[6])
            fifo1 = p(cmd_line[7])
            add(user_cnt, name, "name")
            add(user_cnt, desc, "desc")
            add(user_cnt, job, "job")
            add(user_cnt, fifo0, "fifo0")
            add(user_cnt, fifo1, "fifo1")

            user_cnt += 1


for addr in addr_log:
    print(addr, addr_log[addr])