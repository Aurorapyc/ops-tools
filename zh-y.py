def parse_line(line):
    parts = line.split()
    ip = parts[0]
    code = int(parts[-2])
    return ip, code


def count_codes(lines):
    code_dict = {}
    for line in lines:
        ip, code = parse_line(line)
        if code in code_dict:
            code_dict[code] += 1
        else:
            code_dict[code] = 1
    return code_dict

def top_tips(lines, n=2):
    ip_dict = {}
    for line in lines:
        ip, code = parse_line(line)
        if ip in ip_dict:
            ip_dict[ip] += 1
        else:
            ip_dict[ip] = 1

    sorted_items = sorted(ip_dict.items(), key=lambda x: x[1], reverse=True)
    top_n = sorted_items[:n]
    return [item[0] for item in top_n]

raw = """10.0.0.1 - - [01/Sep/2026:10:00:01] "GET /healthz HTTP/1.1" 200 10
10.0.0.9 - - [01/Sep/2026:10:00:02] "GET /api/list HTTP/1.1" 404 35
10.0.0.1 - - [01/Sep/2026:10:00:03] "POST /api/login HTTP/1.1" 500 12
10.0.0.2 - - [01/Sep/2026:10:00:04] "GET /healthz HTTP/1.1" 200 10
10.0.0.9 - - [01/Sep/2026:10:00:05] "GET /index.html HTTP/1.1" 200 128
10.0.0.1 - - [01/Sep/2026:10:00:06] "GET /healthz HTTP/1.1" 200 10
"""

lines = raw.splitlines()

print(f'总请求行数: {len(lines)}')

codes = count_codes(lines)
sorted_codes = sorted(codes.items(), key=lambda x: x[1], reverse=True)
print('状态码统计: ')
for code, count in sorted_codes:
    print(f'{code}: {count}')

print(f'访问量最高的2个IP: {top_tips(lines, 2)}')

alert_lines = []
for line in lines:
    ip, code = parse_line(line)
    if 400 <= code < 600:
        alert_lines.append(line)

if alert_lines:
    print('\n 以下需要关注:')
    for line in alert_lines:
        print(f' {line}')