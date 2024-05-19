import curses
import time
from records import add_records


def game_over(stdscr, height, width, score, name):
    add_records(name, score)
    stdscr.clear()
    message = "GAME OVER"
    score_message = f"Score: {score}"
    restart_message = "Press 'r' to restart or 'q' to quit"
    start_y = height // 2
    start_x = (width // 2) - (len(message) // 2)
    stdscr.addstr(start_y, start_x, message, curses.A_BOLD)
    stdscr.addstr(start_y + 1, start_x, score_message, curses.A_BOLD)
    stdscr.addstr(start_y + 2, start_x, restart_message, curses.A_BOLD)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('r'):
            return True
        if key == ord('q'):
            return False


def frame(stdscr, height, width, snake, fruit, score):
    stdscr.clear()
    borders(stdscr, height, width)
    stdscr.addstr(0, 2, f'Score: {score}')
    fruit.draw(stdscr)
    snake.draw(stdscr)
    stdscr.refresh()
    time.sleep(0.1)


def borders(stdscr, height, width):
    for y in range(0, height):
        for x in range(0, width):
            if y in (0, height - 1):
                stdscr.addch(y, x, '-')
            elif x in (0, width - 1):
                stdscr.addch(y, x, '|')


def menu(stdscr, height, width):
    stdscr.clear()
    run_message = "1.RUN"
    records_message = "2.RECORDS"
    quit_message = "3.QUIT"
    start_y = height // 2
    start_x = (width // 2) - (len(run_message) // 2)
    stdscr.addstr(start_y, start_x, run_message, curses.A_BOLD)
    stdscr.addstr(start_y + 1, start_x, records_message, curses.A_BOLD)
    stdscr.addstr(start_y + 2, start_x, quit_message, curses.A_BOLD)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('r') or key == ord('1'):
            return 1
        if key == ord('2'):
            return 2
        if key == ord('q') or key == ord('3'):
            return 0
