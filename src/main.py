import curses
import time
import random


class Snake:
    def __init__(self, length, direction, current_coords):
        self.length = length
        self.direction = direction
        self.current_coords = current_coords

    def draw(self, stdscr):
        head = 0
        for coord in self.current_coords:
            if head == 0:
                stdscr.addch(coord[0], coord[1], '@')
                head = 1
            else:
                stdscr.addch(coord[0], coord[1], '#')

    def move(self):
        direct_1 = self.direction
        for coord in self.current_coords:
            direct_2 = coord[2]
            coord[2] = direct_1
            direct_1 = direct_2

        for coord in self.current_coords:
            if coord[2] == curses.KEY_RIGHT:
                coord[1] += 1
            elif coord[2] == curses.KEY_LEFT:
                coord[1] -= 1
            elif coord[2] == curses.KEY_UP:
                coord[0] -= 1
            elif coord[2] == curses.KEY_DOWN:
                coord[0] += 1

    def grow(self):
        tail = self.current_coords[-1][:]
        tail[2] = self.current_coords[-1][2]
        if self.current_coords[-1][2] == curses.KEY_RIGHT:
            tail[1] -= 1
        elif self.current_coords[-1][2] == curses.KEY_LEFT:
            tail[1] += 1
        elif self.current_coords[-1][2] == curses.KEY_UP:
            tail[0] += 1
        elif self.current_coords[-1][2] == curses.KEY_DOWN:
            tail[0] -= 1
        self.current_coords.append(tail)

    def update_direction(self, new_direction):
        opposite_directions = {
            curses.KEY_UP: curses.KEY_DOWN,
            curses.KEY_DOWN: curses.KEY_UP,
            curses.KEY_LEFT: curses.KEY_RIGHT,
            curses.KEY_RIGHT: curses.KEY_LEFT
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction


class Fruit:
    def __init__(self, coord, timer):
        self.coord = coord
        self.timer = timer

    def draw(self, stdscr):
        if self.timer >= 20:
            color = 1
        elif self.timer > 8:
            color = 2
        else:
            color = 3

        if self.timer > 8:
            stdscr.addch(
                self.coord[0],
                self.coord[1],
                '$',
                curses.color_pair(color))
        elif self.timer <= 8 and self.timer % 2 == 0:
            stdscr.addch(
                self.coord[0],
                self.coord[1],
                '!',
                curses.color_pair(color))
        else:
            stdscr.addch(
                self.coord[0],
                self.coord[1],
                '$',
                curses.color_pair(color))


def borders(stdscr, height, width):
    for y in range(0, height):
        for x in range(0, width):
            if y == 0 or y == height - 1:
                stdscr.addch(y, x, '-')
            elif x == 0 or x == width - 1:
                stdscr.addch(y, x, '|')


def snake_init(height, width):
    snake = Snake(length=4, direction=curses.KEY_LEFT, current_coords=[])
    for i in range(snake.length):
        x = width // 2
        y = height // 2
        snake.current_coords.append([y, x + i, curses.KEY_LEFT])
    return snake


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


def game_over(stdscr, height, width, score):
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


def fruit_init(height, width, current_coords):
    while True:
        coord_x = random.randint(1, width - 2)
        coord_y = random.randint(1, height - 2)
        if all(coord[0] != coord_y or coord[1] !=
               coord_x for coord in current_coords):
            break
    fruit = Fruit([coord_y, coord_x], 35)
    return fruit


def fruit_eat(fruit, snake):
    if snake.current_coords[0][0] == fruit.coord[0] and snake.current_coords[0][1] == fruit.coord[1]:
        fruit.timer = 0
        snake.grow()
        return True
    return False


def frame(stdscr, height, width, snake, fruit, score):
    stdscr.clear()
    borders(stdscr, height, width)
    stdscr.addstr(0, 2, f'Score: {score}')
    fruit.draw(stdscr)
    snake.draw(stdscr)
    stdscr.refresh()
    time.sleep(0.1)


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


def game_run(stdscr, height, width, snake, fruit):
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
            return game_over(stdscr, height, width, score)

        frame(stdscr, height, width, snake, fruit, score)


def main(stdscr):
    while True:
        height, width = 20, 40

        game_init(stdscr, height, width)

        snake = snake_init(height, width)
        fruit = fruit_init(height, width, snake.current_coords)
        if not game_run(stdscr, height, width, snake, fruit):
            break


if __name__ == '__main__':
    curses.wrapper(main)
