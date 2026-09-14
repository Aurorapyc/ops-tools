def add_task(tasks):
    global next_id
    title = input('请输入任务标题: ')
    if tasks:
        next_id = max(task['id'] for task in tasks) +1
    else:
        next_id += 1
    print(f'已添加任务: id={next_id}')


def remove_task(tasks, task_id):
        for task in tasks:
            if task_id == task['id']:
                tasks.remove(task)
                print(f'已删除 id={task_id}')
                return
        print(f'id={task_id} 不存在')


def show_tasks(tasks):
    if not tasks:
        print('暂无任务')
        return

    for task in tasks:
        task_id = task['id']
        title = task['title']
        done = task['done']
        status = '✓' if done else '✗'
        print(f'id={task_id} {title} {status}')


def toggle_done(tasks, task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task['done']
            print(f'已切换 id={task_id}')
            return
    print(f'id={task_id} 不存在')


def main():
    tasks = []

    while True:
        print("\n1. 增加任务")
        print("2. 删除任务")
        print("3. 显示任务")
        print("4. 切换完成")
        print("0. 退出")
        choice = input("请选择：")

        match choice:
            case '1':
                add_task(tasks)
            case '2':
                task_id = int(input('请输入要删除的id: '))
                remove_task(tasks, task_id)
            case '3':
                show_tasks(tasks)
            case '4':
                task_id = int(input('请输入要切换的id: '))
                toggle_done(tasks, task_id)
            case '0':
                print('再见!')
                break
            case _:
                print('无效选择，请重新输入')

main()
