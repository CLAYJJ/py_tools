import os
import sys
"""
计算代码行数，以及注释覆盖率
"""

def usage():
    if len(sys.argv) != 2:
        print("need a path arg")
        exit()


def get_suffix(file_name):
    return os.path.splitext(file_name)[1]

backend_allowed = ['.java']
allowed = [".jsp", ".java", ".js", ".html", ".css", ".scss", ".vue", ".xml"]


if __name__ == "__main__":
    usage()
    path = sys.argv[1]
    count = 0
    comment_count = 0
    for root, dirs, files in os.walk(path):
        if len(files) != 0:
            print(f"文件夹：{root}")
            for f in files:
                try:
                    with open(os.path.join(root, f), encoding='UTF-8', errors='ignore') as file:
                        suffix = get_suffix(file.name)
                        if suffix in backend_allowed:
                            for line in file:
                                line = line.strip()
                                if len(line):
                                    count += 1
                                    if line.startswith("/*") or line.startswith("*") or line.startswith("//"):
                                        comment_count += 1
                except Exception as e:
                    pass
    print(f"代码行数：{count}")
    print(f"注释行数：{comment_count}")
    print("注释覆盖率：{:.2%}".format(comment_count/count))


