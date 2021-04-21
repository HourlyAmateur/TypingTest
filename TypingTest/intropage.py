"""
    This module is the entry point for this program. 
    This program grabs the days featured article from wikipedia
    stores it in a txt file that we use to practice typing. 
    Michael Murphy
    03/29/2021
"""


import curses 
import Typing_TestV2
import join
import login


menu = ["FREE PLAY", "LOG IN", "JOIN", "QUIT"]

def print_menu(stdscr, selected):
    "draws the main screen menu"
    
    curses.noecho()
    stdscr.clear()
    curses.resize_term(30, 70)
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
           stdscr.addstr(y, x, row) 
    stdscr.refresh()
    return selected


def main(stdscr):
    "runs the business logic of the intro page"

    stdscr.keypad(True)
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    chosen = 0
    print_menu(stdscr, chosen)

    
    
    change = True
    while change:
        key = stdscr.getch()
        if key == 259 and chosen > 0:                    # up key
            chosen -= 1
            print_menu(stdscr, chosen)

        elif key == 258 and chosen < 3:                  # down key
            chosen += 1 
            print_menu(stdscr, chosen)

        elif key == 10:                                 # enter key
            stdscr.clear()
            stdscr.refresh()
            go_here = print_menu(stdscr, chosen)
            stdscr.clear()
            stdscr.refresh()       
            if menu[go_here] == "QUIT":
                change = False
            elif menu[go_here] == "FREE PLAY":
                Typing_TestV2.type_test(stdscr)
                stdscr.clear()
                go_here = print_menu(stdscr, chosen)
                stdscr.refresh()
            elif menu[go_here] == "LOG IN":
                login.log_in(stdscr)
                stdscr.clear()
                go_here = print_menu(stdscr, chosen)
                stdscr.refresh()
            elif menu[go_here] == "JOIN":
                join.join(stdscr)
                stdscr.clear()
                go_here = print_menu(stdscr, chosen)
                stdscr.refresh()



        elif key == 27:                                 # escape key
            change = False
    
    print_menu(stdscr, chosen)
    stdscr.refresh()

curses.wrapper(main)