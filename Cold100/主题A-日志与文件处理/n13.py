with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

total_request = len(lines)
error_count = 0

for line in lines:
    code = int(line.split()[-2])
    if 400 <= code <= 599:
        error_count += 1

error_rate = error_count / total_request * 100
print(f'错误率: {error_rate:.1f}%')

# 优化写法

total = 0
errors = 0
for line in open('日志文件/big_access.log', encoding='utf-8'):
    parts = line.split()
    if len(parts) < 9:
        continue
    total += 1
    if parts[-2].startswith('4') or parts[-2].startswith('5'):
        errors += 1

rate = (errors / total * 100) if total else 0
print(f'错误率: {rate:.1f} ({errors}/{total})')

