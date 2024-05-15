import curses

class Snake:
    def __init__(self, length, speed, direction, current_coords):
        self.length = length
        self.speed = speed
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




def borders(stdscr, height, width):
    for y in range(0, height):
        for x in range(0, width):
            if y == 0 or y == height - 1:
                stdscr.addch(y, x, '-')
            elif x == 0 or x == width - 1:
                stdscr.addch(y, x, '|')
            elif (y, x) in [(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)]:
                stdscr.addch(y, x, '+')

def snake_init(stdscr, height, width):
    snake = Snake(length=4, speed=1, direction=curses.KEY_LEFT, current_coords=[])
    for i in range(snake.length):
        x = width // 2
        y = height // 2
        snake.current_coords.append([y, x+i, curses.KEY_LEFT])
    snake.draw(stdscr)
    return snake

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)

    height, width = 20, 40
    borders(stdscr, height, width)

    snake = snake_init(stdscr, height, width)


    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            snake.direction = key
            snake.move()
            stdscr.clear()
            borders(stdscr, height, width)
            snake.draw(stdscr)
        stdscr.refresh()

curses.wrapper(main)
