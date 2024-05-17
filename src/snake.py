import curses


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


def snake_init(height, width):
    snake = Snake(length=4, direction=curses.KEY_LEFT, current_coords=[])
    for i in range(snake.length):
        x = width // 2
        y = height // 2
        snake.current_coords.append([y, x + i, curses.KEY_LEFT])
    return snake
