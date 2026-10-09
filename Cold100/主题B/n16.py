# import os

# files = []
# folder = 'D:\\Document\\Claude'

# for name in os.listdir(folder):
#     size = os.path.getsize(os.path.join(folder, name))
#     files.append((name, size))

# sorted_files = sorted(files, key=lambda x: x[1], reverse=True)

# for name, size in sorted_files[:10]:
#     print(f'{name}: {size}字节')


from pathlib import Path

folder = Path('D:\\Document\\ClaudeCode')
files = []

for file in folder.iterdir():
    if file.is_file():
        files.append((file.name, file.stat().st_size))

sorted_files = sorted(files, key=lambda x: x[1], reverse=True)

for name, size in sorted_files[:5]:
    print(f'{name}: {size}字节')

# 优化写法

import os

files = []
for root, _, names in os.walk('日志文件'):
    for n in names:
        p = os.path.join(root, n)
        files.append((os.path.getsize(p), p))

for size, path in sorted(files, reverse=True)[:10]:
    print(f'{size:8.1f}KB {path}')