with open ('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

count_dict = {}
for line in lines:
    key = line.strip()
    if key in count_dict:
        count_dict[key] += 1
    else:
        count_dict[key] = 1

sorted_items = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

for line, count in sorted_items:
    if count >= 2:
        print(f'{count}次: {line.strip()}')
