with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

path_dict = {}
for line in lines:
    if not line.strip():
        continue
    path = line.split('"')[1].split()[1]
    if path in path_dict:
        path_dict[path] += 1
    else:
        path_dict[path] = 1

sorted_paths = sorted(path_dict.items(), key=lambda x: x[1], reverse=True)
for path, count in sorted_paths[:5]:
    print(f'{path}: {count}')

# 优化写法

from collections import Counter
import re

paths = Counter()
for line in open('日志文件/big_access.log', encoding='utf-8'):
    m = re.search(r'"(?:GET|PUT|POST|DELETE|HEAD) (\S+)', line)
    if m:
        paths[m.group(1)] += 1

for path, n in paths.most_common():
    print(f'{n:>4} {path}')
