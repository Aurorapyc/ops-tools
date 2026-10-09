with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

hours_dict = {}
for line in lines:
    hours = line.split()[3].split(':')[1]
    if hours in hours_dict:
        hours_dict[hours] += 1
    else:
        hours_dict[hours] = 1

for hour in sorted(hours_dict):
    print(f'{hour}点: {hours_dict[hour]}次')


# 优化写法

from collections import Counter
from datetime import datetime

hours = Counter()
for line in open('日志文件/big_access.log', encoding='utf-8'):
    m = line.split('[')
    if len(m) < 2:
        continue
    ts = m[1].split(']')[0].split()[0]
    dt = datetime.strptime(ts, '%d/%b/%Y:%H:%M:%S')
    hours[dt.hour] += 1

for h in sorted(hours):
    print(f'{h:02d}点: {hours[h]}')
