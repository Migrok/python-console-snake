import curses


def load_records(filename='records.txt'):
    records = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    name, score = parts
                    try:
                        records.append((name, int(score)))
                    except ValueError:
                        pass
        records = sorted(records, key=lambda x: x[1], reverse=True)
    except FileNotFoundError:
        pass
    return records


def add_records(name, score):
    filename = 'records.txt'
    with open(filename, 'a') as file:
        file.write(f'{name},{score}\n')


def show_records(stdscr, height, width, name):
    stdscr.clear()
    message = "Press 'c' to change name, 'q' to quit\n"
    start_y = height // 2 - 5
    start_x = (width // 2) - (len(message) // 2)
    stdscr.addstr(start_y, start_x, message, curses.A_BOLD)

    name_message = f"Your name: {name}\n"
    stdscr.addstr(start_y + 1, start_x, name_message, curses.A_BOLD)

    records_file = 'records.txt'
    records = load_records(records_file)

    for idx, (name, score) in enumerate(records[0:10], start=1):
        record_message = f'{idx}. {name}: {score}'
        stdscr.addstr(start_y + idx + 2, start_x, record_message)

    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('c'):
            set_name(stdscr, height, width)
            break


def set_name(stdscr, height, width):
    while True:
        stdscr.timeout(-1)
        curses.echo()
        stdscr.clear()
        message = "Enter your name: "
        start_y = height // 2
        start_x = (width // 2) - (len(message) // 2)
        stdscr.addstr(start_y, start_x, message)
        stdscr.refresh()

        name = stdscr.getstr(start_y + 1, start_x).decode('utf-8')
        if len(name) < 32:
            filename = 'records.txt'
            try:
                with open(filename, 'r') as file:
                    lines = file.readlines()
                if lines:
                    lines[0] = name + '\n'
                with open('records.txt', 'w') as file:
                    file.writelines(lines)
            except FileNotFoundError:
                with open('records.txt', 'w') as file:
                    file.writelines(f'{name}\n')
            return name
        else:
            stdscr.clear()
            message = "Name is too long\nPress any button to change name again"
            stdscr.addstr(start_y, start_x, message)
            stdscr.getch()


def get_name(stdscr, height, width):
    try:
        with open('records.txt', 'r') as file:
            name = file.readline().strip()
    except FileNotFoundError:
        name = set_name(stdscr, height, width)
    return name
