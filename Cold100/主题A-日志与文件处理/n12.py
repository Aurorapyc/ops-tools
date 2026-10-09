with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

total_size = 0
for line in lines:
    size = line.split()[-1]
    int_size = int(size)
    total_size += int_size

if total_size < 1024:
    print(f'总流量: {total_size}B')
elif total_size < 1024 * 1024:
    print(f'总流量: {total_size / 1024:.2f}KB')
else:
    print(f'总流量: {total_size / 1024 / 1024:.2f}MB')

# 优化写法

def human(n):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if n < 1024:
            return f'{n:.1f}{unit}'
        n /= 1024
    return f'{n:.1f}TB'

total = 0
for line in open('日志文件/big_access.log', encoding='utf-8'):
    parts = line.split()
    if len(parts) >= 9 and parts[-1].isdigit():
        total += int(parts[-1])

print(f'总流量: {human(total)}')