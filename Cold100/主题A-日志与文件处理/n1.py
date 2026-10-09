with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

total = len(lines)
non_empty = 0
comments = 0

for line in lines:
    if line.strip():
        non_empty += 1
    if line.strip().startswith('#'):
        comments += 1

print(f'总行数: {total}')
print(f'非空行数: {non_empty}')
print(f'#开头行数: {comments}')