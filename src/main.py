
import curses
from records import get_name, show_records
from game_logic import game
from game_visuals import menu


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
