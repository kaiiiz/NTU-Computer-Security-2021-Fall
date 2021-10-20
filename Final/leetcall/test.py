import ast

# iin = input()
# print(iin)

source = '2 and 1'

tree = ast.parse(source, mode='eval')

whitelist = (
    ast.Expression,  # root node of the ast
    ast.Call, ast.Name, ast.Constant,  # only accept call, name and constant
    ast.Load  # call a function need to "load" its function name
)
for node in ast.walk(tree):
    if not isinstance(node, whitelist):
        print(node)
        print("false")
        break

# while True:
# eval(source)
