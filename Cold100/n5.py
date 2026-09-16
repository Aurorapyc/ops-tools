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