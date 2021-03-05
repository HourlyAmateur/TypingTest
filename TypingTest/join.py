import curses
import time


def join(stdscr):
    stdscr.clear()
    curses.echo()
    curses.curs_set(2)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.use_default_colors()
    curses.cbreak()
    curses.resize_term(40, 80) 
    curses.update_lines_cols() 
    stdscr.keypad(True)
    stdscr.addstr(10, 32, "CREATE A USERNAME")
    stdscr.addstr(20, 32, "CREATE A PASSWORD")
    username = stdscr.getstr(12, 32, 15)
    password = stdscr.getstr(22, 32, 15)
    curses.curs_set(0)