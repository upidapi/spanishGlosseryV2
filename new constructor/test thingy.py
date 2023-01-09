

class TreeNode:
    def __init__(self, data):
        self.children = []
        self.data = data

    def adopt(self, child):
        self.children.append(child)

    def subscribe(self, parent):
        parent.children.append(self)

"""
    hello (im (not/am) well) rn
split the thing at parentheses to make multiple parts
    0 hello "1" rn
    1 im "2" well
    2 not
start with the inner parts and resolve logic
    0 hello "1" rn
    1 im "2" well
    2 not "or" am
merge those inner parts into the larger ones
    0 hello "1" rn
    1 im ´not "or" am´ well
resolve outer parts 
    etc
"""

# inp = "what hi/hello (you (or me)) ..."
inp = "what hi/ hello im/you're blue ..."

# inp = inp.split("/")
# out = []
# for part in inp:
#     out.append(part.strip().split(" "))

last = TreeNode("")
for char in inp:
    cur = TreeNode(char)
    cur.subscribe(last)
    last = cur


# inp = [x.strip() for x in inp]

# print(out)
# chunks = [[TreeNode("")]]
# last = TreeNode("")
#
# for char in inp:
#     if char == "/":
#         chunks.append([])
#     else:
#         cur = TreeNode(char)
#         cur.subscribe(last)
#         chunks[-1].append(cur)
#
#
#     if last.data != "/":
#         cur = TreeNode(char)
#         cur.subscribe(last)
#         chunks[-1].append(cur)
#     else:
#
#     last = char



