from pathlib import Path
import time

folder = Path('日志文件2')

for file in folder.rglob('*'):
    if file.is_file():
        t = time.localtime(file.stat().st_mtime)
        year_month = time.strftime('%Y-%m', t)

        subdir = folder / year_month
        subdir.mkdir(exist_ok=True)

        new_path = subdir / file.name
        file.rename(new_path)
        print(f'移动: {file.name} -> {new_path}')