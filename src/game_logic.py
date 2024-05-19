import curses
from fruit import fruit_init
from snake import snake_init
from game_visuals import game_over, frame, borders
from records import get_name


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
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT,
                   curses.KEY_UP, curses.KEY_DOWN]:
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


def lose_border(height, width, snake):
    if (snake.current_coords[0][0] == 0
            or snake.current_coords[0][0] == height - 1
            or snake.current_coords[0][1] == 0
            or snake.current_coords[0][1] == width - 1):
        return True
    return False


def lose_ouroboros(snake):
    head = snake.current_coords[0]
    for i in snake.current_coords[1:]:
        if head[0] == i[0] and head[1] == i[1]:
            return True
    return False


def fruit_eat(fruit, snake):
    if (snake.current_coords[0][0] == fruit.coord[0]
            and snake.current_coords[0][1] == fruit.coord[1]):
        fruit.timer = 0
        snake.grow()
        return True
    return False


def game(stdscr, height, width):
    while True:
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
