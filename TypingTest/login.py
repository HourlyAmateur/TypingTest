import usersetup
import curses
import sqlite3 as sl

escape = 27
enter = 10
backspace = 8

def log_in(stdscr):
    stdscr.clear()
    curses.echo()
    curses.curs_set(2)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.use_default_colors()
    curses.cbreak()
    curses.resize_term(40, 80) 
    curses.update_lines_cols() 
    stdscr.keypad(True)

    stdscr.addstr(10, 32, "USERNAME")
    stdscr.addstr(20, 32, "PASSWORD")


    stdscr.move(12, 32)
    username = ''
    key = None
    while key != enter:
        key = stdscr.getch()
        if key == escape:                      
            curses.curs_set(0)
            return
        elif key == backspace:
            username = username[:-1]
            stdscr.delch()
        else:
            username += chr(key)


    stdscr.move(22, 32)
    password = ''
    key = None
    while key != enter:
        key = stdscr.getch()
        if key == escape:                      
            curses.curs_set(0)
            return
        elif key == backspace:
            password = password[:-1]
            stdscr.delch()
        else:
            password += chr(key)

    stdscr.addstr(0,0, usersetup.user_login(username, password))
    curses.curs_set(0)
    return