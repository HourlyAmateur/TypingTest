import curses
import time

def user_page(stdscr, un):
    stdscr.clear()
    curses.echo()
    curses.curs_set(2)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.use_default_colors()
    curses.cbreak()
    curses.resize_term(40, 80) 
    curses.update_lines_cols() 
    stdscr.keypad(True)

    stdscr.addstr(15, 20, f"Welcome Back {un}")
    stdscr.refresh()
    time.sleep(3)
    stdscr.clear()
    
    return