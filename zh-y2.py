def check(servers, cpu_th=90, mem_th=90, disk_th=85):
    for server in servers:
        name = server['name']
        cpu = server['cpu']
        mem = server['mem']
        disk = server['disk']

        if cpu > cpu_th or mem > mem_th or disk > disk_th:
            status = '告警'
        else:
            status = '正常'

        print(f'{name} cpu={cpu} mem={mem} disk={disk} {status}')

    total_cpu = 0
    total_disk = 0
    for server in servers:
        total_cpu += server['cpu']
        total_disk += server['disk']

    avg_cpu = total_cpu / len(servers)
    avg_disk = total_disk / len(servers)
    print(f'cpu平均: {avg_cpu:.1f}')
    print(f'磁盘平均: {avg_disk:.1f}')

    max_alert = 0
    most_dangerous = None
    for server in servers:
        cpu = server['cpu']
        mem = server['mem']
        disk = server['disk']

        alert_count = 0
        if cpu > cpu_th:
            alert_count += 1
        if mem > mem_th:
            alert_count += 1
        if disk > disk_th:
            alert_count += 1

        if alert_count > max_alert:
            max_alert = alert_count
            most_dangerous = server

    print(f'最危险: {most_dangerous["name"]}, 告警 {max_alert}项')


servers = [
    {"name": "web-01", "cpu": 92, "mem": 40, "disk": 60},
    {"name": "web-02", "cpu": 55, "mem": 88, "disk": 70},
    {"name": "db-01",  "cpu": 70, "mem": 95, "disk": 45},
    {"name": "cache-01", "cpu": 30, "mem": 35, "disk": 90},
]

check(servers, 95, 80, 90)
