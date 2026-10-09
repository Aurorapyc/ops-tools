with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

groups = {}
for line in lines:
    code = line.split()[-2]
    if code not in groups:
        groups[code] = []
    groups[code].append(line)

for code, lines_list in groups.items():
    with open(f'日志文件/{code}.log', 'w', encoding='utf-8') as f:
        f.writelines(lines_list)

# 优化写法

handles = {}                     # 字柄字典：同一个文件对象反复使用
for line in open('日志文件/big_access.log', encoding='utf-8'):
    parts = line.split()
    if len(parts) < 9:
        continue
    code = parts[-2]
    if code not in handles:
        handles[code] = open(f'日志文件/{code}.log', 'w', encoding='utf-8')
    handles[code].write(line)

for h in handles.values():
    h.close()
print(f'拆分完成: {",".join(sorted(handles))}')
    