from pathlib import Path

folder = Path('日志文件')
for file in folder.iterdir():
    if file.is_file():
        new_name = f'bak_{file.name}'
        new_path = file.parent / new_name
        file.rename(new_path)
        print(f'重命名: {file.name} -> {new_name}')

# 优化写法

import os

for name in os.listdir('.'):
    if os.path.isfile(name) and not name.startswith('bak_'):
        os.rename(name, f'bak_{name}')
        print(f'已重命名: {name}')        