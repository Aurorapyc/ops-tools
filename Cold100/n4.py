with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

path_dict = {}
for line in lines:
    if not line.strip():
        continue
    path = line.split('"')[1].split()[1]
    if path in path_dict:
        path_dict[path] += 1
    else:
        path_dict[path] = 1

sorted_paths = sorted(path_dict.items(), key=lambda x: x[1], reverse=True)
for path, count in sorted_paths[:5]:
    print(f'{path}: {count}')
