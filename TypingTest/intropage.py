import curses
import time
import Typing_TestV2
import join


menu = ["FREE PLAY", "LOG IN", "JOIN", "QUIT"]

def printmenu(stdscr, selected):
    
    stdscr.clear()
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
    stdscr.keypad(True)
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    chosen = 0
    printmenu(stdscr, chosen)

    
    
    changeon = True
    while changeon:
        key = stdscr.getch()
        if key == 259 and chosen > 0:                    # up key
            chosen -= 1
            printmenu(stdscr, chosen)

        elif key == 258 and chosen < 3:                  # down key
            chosen += 1 
            printmenu(stdscr, chosen)

        elif key == 10:                                 # enter key
            stdscr.clear()
            stdscr.refresh()
            gohere = printmenu(stdscr, chosen)
            stdscr.clear()
            stdscr.refresh()       
            if menu[gohere] == "QUIT":
                changeon = False
            elif menu[gohere] == "FREE PLAY":
                Typing_TestV2.type_test(stdscr)
                stdscr.clear()
                gohere = printmenu(stdscr, chosen)
                stdscr.refresh()
            elif menu[gohere] == "LOG IN":
                pass
            elif menu[gohere] == "JOIN":
                join.join(stdscr)
                stdscr.clear()
                gohere = printmenu(stdscr, chosen)
                stdscr.refresh()



        elif key == 27:                                 # escape key
            changeon = False
    
    printmenu(stdscr, chosen)
    stdscr.refresh()

curses.wrapper(main)