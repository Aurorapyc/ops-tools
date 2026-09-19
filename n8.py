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
    