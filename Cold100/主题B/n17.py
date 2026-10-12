from pathlib import Path
import hashlib

folder = Path('D:\\Document\\ClaudeCode')
groups = {}

for file in folder.iterdir():
    if file.is_file():
        md5 = hashlib.md5()
        with open(file, 'rb') as f:
            md5.update(f.read())
        digest = md5.hexdigest()

        if digest not in groups:
            groups[digest] = []
        groups[digest].append(file.name)

for digest, files in groups.items():
    if len(files) > 1:
        print(f'重复文件: {",".join(files)}')

# 优化写法

import hashlib
import os
from collections import defaultdict

def md5(path, chunk=8192):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            data = f.read(chunk)
            if not data:
                break
            h.update(data)
    return h.hexdigest()

groups = defaultdict(list)
for root, _, names in os.walk('.'):
    for n in names:
        p = os.path.join(root, n)
        groups[md5(p)].append(p)

for digest, paths in groups.items():
    if len(paths) > 1:
        print(f'重复: | {",".join(paths)}')