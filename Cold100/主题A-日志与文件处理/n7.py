with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

times = []
for line in lines:
    timestamp = line.split()[3].strip('[]')
    times.append(timestamp)

earliest = min(times)
latest = max(times)

print(f'最早: {earliest}')
print(f'最晚: {latest}')

# 优化写法

from datetime import datetime

times = []
for line in open('日志文件/big_access.log', encoding='utf-8'):
    parts = line.split('[')
    if len(parts) < 2:
        continue
    ts = parts[1].split(']')[0].split()[0]
    times.append(datetime.strptime(ts, "%d/%b/%Y:%H:%M:%S"))

if times:
    print(f'最早: {min(times)}')
    print(f'最晚: {max(times)}')
