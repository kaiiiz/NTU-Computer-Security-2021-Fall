# chal1:

# print(
#     "\n".join(
#         list(
#             map("Hello, %s!".__mod__, open(0).read().split())
#         )
#     )
# )


# print(getattr("\n", "join")(list(map(getattr("Hello, %s!", "__mod__"),getattr(getattr(open(0), "read")(),"split")()))))

# chal2: fibo

# "\n".join(
#     list(
#         map(str,
#         map(round,
#         map((2.23606797749979**(-1)).__mul__,
#         map((1.618033988749895).__pow__,
#         map(int, open(0).read().split()
#         )))))
#     )
# )

# print(getattr("\n","join")(list(map(str,map(round,map(getattr(getattr(2.23606797749979,"__pow__")(getattr(1,"__neg__")()),"__mul__"),map(getattr(1.618033988749895,"__pow__"),map(int, getattr(getattr(open(0), "read")(),"split")()))))))))

# n = int(input())

# def aa(n):
#     x = [0, 1]

#     for _ in range(n):
#         x = x[1], sum(x)

#     return x[0]

# def qq(n):
#     return round(pow(1.618033988749895, n)*pow(2.23606797749979, -1))

# for i in range(70):
#     print(aa(i), qq(i), aa(i) == qq(i))

# chal3: FizzBuzz

# a = list(range(1,10001))
# for i in range(1,10001):
#     if ((i / 15) - (i // 15)) == 0:
#         print("FizzBuzz")
#     elif ((i / 3) - (i // 3)) == 0:
#         print("Fizz")
#     elif ((i / 5) - (i // 5)) == 0:
#         print("Buzz")
#     else:
#         print(i)
# a = map(float(0.2).__mul__, range(1,10))
# print(list(a))

# for idx, aa in enumerate(a, 1):
#     a[idx-1] = (idx / 15).is_integer() and "FizzBuzz" or ((idx / 3).is_integer() and "Fizz" or ((idx / 5).is_integer() and "Buzz" or idx))

# for aa in a:
    # print(aa)

# class Test:
#    @property
#    def aFunction(self):
#         print("you called this function")

# test = Test()
# getattr(test, 'aFunction')

a = map("".join, zip(
    ['', '', 'Fizz'] * 3334,
    ['', '', '', '', 'Buzz'] * 2000,
    iter(" ".__str__, 0),
    map(str, range(1, 10001))
))
print(list(a))