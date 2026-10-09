with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('必刷100题/masked.log', 'w', encoding='utf-8') as f:
    for line in lines:
        ip = line.split()[0]
        new_line = line.replace(ip, f'<{ip}>')
        f.write(new_line)

# 优化写法

import re

pattern = re.compile(r'\b\d{1,3}(?:\.\d{1,3}){3}')
with open('日志文件/big_access.log', encoding='utf-8') as fin, \
     open('日志文件/marked.log', 'w', encoding='utf-8') as fout:
    for line in fin:
        fout.write(pattern.sub('<IP>', line))
print('已输出 marked.log')
