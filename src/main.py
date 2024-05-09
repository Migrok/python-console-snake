import curses

class Snake:
    def __init__(self, length, speed, direction, current_coord):
        self.length = length
        self.speed = speed
        self.direction = direction
        self.current_coord = current_coord

    def draw(self, stdscr):
        for i in self.current_coord:
            if i == 0:
                stdscr.addch(i[0], i[1], '+')

def borders(stdscr, height, width):
    for y in range(0, height):
        for x in range(0, width):
            if y == 0 or y == height - 1:
                stdscr.addch(y, x, '-')
            elif x == 0 or x == width - 1:
                stdscr.addch(y, x, '|')
            elif (y, x) in [(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)]:
                stdscr.addch(y, x, '+')

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)

    height, width = 20, 40
    borders(stdscr, height, width)


    snake = Snake(length=4, speed=1, direction='west', current_coord=[])
    for i in range(snake.length):
        x = width // 2
        y = height // 2
        snake.current_coord.append([y+i, x])

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        stdscr.refresh()

curses.wrapper(main)
