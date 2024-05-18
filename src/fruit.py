import curses
import random


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


def fruit_init(height, width, current_coords):
    while True:
        coord_x = random.randint(1, width - 2)
        coord_y = random.randint(1, height - 2)
        if all(coord[0] != coord_y or coord[1] !=
               coord_x for coord in current_coords):
            break
    fruit = Fruit([coord_y, coord_x], 35)
    return fruit
