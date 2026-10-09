with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('必刷100题/errors.log', 'w', encoding='utf-8') as f:
    for line in lines:
        parts = line.split()
        if parts[-2] == '500':
            f.write(line)

# 优化写法

with open('日志文件/big_access.log', encoding='utf-8') as fin, \
     open('日志文件/errors.log', 'w', encoding='utf-8') as fout:
    for line in fin:
        if '500' in line:
            fout.write(line)
