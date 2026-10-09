all_lines = []
for filename in ['必刷100题/errors.log', '日志文件/2026-09-01.log']:
    with open(filename, 'r', encoding='utf-8') as f:
        all_lines.extend(f.readlines())

unique_lines = set(all_lines)

for line in sorted(unique_lines):
    print(line.strip())

# 优化写法

import glob

out_name = '日志文件/merged.log'
files = [p for p in glob.glob('日志文件/*.log') if p != out_name]

seen = set()
with open(out_name, 'w', encoding='utf-8') as fout:
    for path in files:
        with open(path, encoding='utf-8') as f:
            for line in f:
                if line not in seen:
                    seen.add(line)
                    fout.write(line)

print(f'合并后: {len(seen)}行(去重后)')
 