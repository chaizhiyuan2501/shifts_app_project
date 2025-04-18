import os

def print_tree(startpath, prefix=""):
    for item in os.listdir(startpath):
        if item == ".git":
            continue  # 跳过 .git 目录
        path = os.path.join(startpath, item)
        if os.path.isdir(path):
            print(prefix + "├── " + item)
            print_tree(path, prefix + "│   ")
        else:
            print(prefix + "├── " + item)

print_tree(".")