with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

total_len = 0
avg_len = 0
for line in lines:
    length = len(line)
    total_len += length

avg_len = total_len / len(lines)
longest = max(lines, key=len)

print(f'平均长度: {avg_len:.1f}')
print(f'最长行: {longest}')