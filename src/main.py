import time
from snake import *
from fruit import *
from records import *


def game_init(stdscr, height, width):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 2, -1)
    curses.init_pair(2, 3, -1)
    curses.init_pair(3, 1, -1)
    borders(stdscr, height, width)


def game_run(stdscr, height, width, snake, fruit, name):
    score = 0
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            snake.update_direction(key)

        snake.move()

        if fruit_eat(fruit, snake):
            score += 1
            fruit = fruit_init(height, width, snake.current_coords)

        fruit.timer -= 1
        if fruit.timer <= 0:
            fruit = fruit_init(height, width, snake.current_coords)

        if lose_border(height, width, snake) or lose_ouroboros(snake):
            return game_over(stdscr, height, width, score, name)

        frame(stdscr, height, width, snake, fruit, score)


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
        elif key == ord('q'):
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
            if y == 0 or y == height - 1:
                stdscr.addch(y, x, '-')
            elif x == 0 or x == width - 1:
                stdscr.addch(y, x, '|')


def lose_border(height, width, snake):
    if snake.current_coords[0][0] == 0 or snake.current_coords[0][0] == height - 1 or \
            snake.current_coords[0][1] == 0 or snake.current_coords[0][1] == width - 1:
        return True
    return False


def lose_ouroboros(snake):
    head = snake.current_coords[0]
    for i in snake.current_coords[1:]:
        if head[0] == i[0] and head[1] == i[1]:
            return True
    return False


def fruit_eat(fruit, snake):
    if snake.current_coords[0][0] == fruit.coord[0] and snake.current_coords[0][1] == fruit.coord[1]:
        fruit.timer = 0
        snake.grow()
        return True
    return False


def menu(stdscr, height, width):
    stdscr.clear()
    run_message = "1.RUN"
    records_message = "2.RECORDS"
    settings_message = "3.SETTINGS"
    quit_message = "4.QUIT"
    start_y = height // 2
    start_x = (width // 2) - (len(run_message) // 2)
    stdscr.addstr(start_y, start_x, run_message, curses.A_BOLD)
    stdscr.addstr(start_y + 1, start_x, records_message, curses.A_BOLD)
    stdscr.addstr(start_y + 2, start_x, settings_message, curses.A_BOLD)
    stdscr.addstr(start_y + 3, start_x, quit_message, curses.A_BOLD)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('r') or key == ord('1'):
            return 1
        elif key == ord('2'):
            return 2
        elif key == ord('q') or key == ord('4'):
            return 0


def game(stdscr, height, width):
    game_init(stdscr, height, width)
    snake = snake_init(height, width)
    fruit = fruit_init(height, width, snake.current_coords)
    if not game_run(
            stdscr,
            height,
            width,
            snake,
            fruit,
            get_name(
                stdscr,
                height,
                width)):
        return 0


def main(stdscr):
    height, width = 20, 40
    get_name(stdscr, height, width)
    while True:
        player_choice = menu(stdscr, height, width)
        if player_choice == 1:
            while True:
                if not game(stdscr, height, width):
                    break
        elif player_choice == 2:
            show_records(
                stdscr, height, width, get_name(
                    stdscr, height, width))
        elif player_choice == 0:
            break


if __name__ == '__main__':
    curses.wrapper(main)
