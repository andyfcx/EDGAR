import random

num = random.randint(0,3)
print("random num:{}".format(num))
try:
    if num!=3:
        5/0
except Exception as exc:
    pass
    