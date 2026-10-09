with open('必刷100题/access.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

ip_dict = {}
for line in lines:
    ip = line.split()[0]
    if ip in ip_dict:
        ip_dict[ip] += 1
    else:
        ip_dict[ip] = 1

sorted_ips = sorted(ip_dict.items(), key=lambda x: x[1], reverse=True)
for ip, count in sorted_ips:
    print(f'{ip}: {count}')


