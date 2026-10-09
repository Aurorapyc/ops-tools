from datetime import datetime

with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

months = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
}

groups = {}
for line in lines:
    timestamp = line.split()[3].strip('[]')
    dt = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S')
    date = dt.strftime('%Y-%m-%d')
    # date_part = timestamp.split(':')[0]
    # day, month, year = date_part.split('/')
    # date = f'{year}-{months[month]}-{day}'
    if date not in groups:
        groups[date] = []
    groups[date].append(line)

for date, lines_list in groups.items():
    with open(f'日志文件/{date}.log', 'w', encoding='utf-8') as f:
        f.writelines(lines_list)

# 优化写法

from collections import defaultdict
from datetime import datetime

buckets = defaultdict(list)
for line in open('日志文件/big_access.log', encoding='utf-8'):
    parts = line.split('[')
    if len(parts) < 2:
        continue
    date_part = parts[1].split(':')[0]
    d = datetime.strptime(date_part, '%d/%b/%Y').strftime('%Y-%m-%d')
    buckets[d].append(line)

for d, lines in buckets.items():
    with open(f'日志文件/{d}.log', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f'{d}.log: {len(lines)}行')