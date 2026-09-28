with open('日志文件/big_access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(0, len(lines), 100):
    chunk = lines[i:i+100]                  #切片返回的是列表,切片左闭右开
    part_num = i // 100 + 1
    filename = f'part_{part_num}.txt'
    with open(f'日志文件/{filename}', 'w', encoding='utf-8') as f:
        f.writelines(chunk)