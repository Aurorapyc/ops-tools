with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

code_dict = {}

for line in lines:
    code = line.split()[-2]
    if code in code_dict:
        code_dict[code] += 1
    else:
        code_dict[code] = 1

sorted_items = sorted(code_dict.items(), key=lambda x: x[1], reverse=True)
for code, count in sorted_items:
    print(f'{code}: {count}')

