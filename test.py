import os

for d in os.listdir("."):
    if os.path.isfile(d) or d == ".git":
        continue
    print(type(d))