"""
    This page is where the user will log into their 
    account.
    Michael Murphy
    03/29/2021 
"""

import usersetup
import userpage
import curses
import time

escape = 27
enter = 10
backspace = 8

def log_in(stdscr):
    "Runs the business logic of the login page"

    trying = True
    while trying:
        stdscr.clear()
        curses.echo()
        curses.curs_set(2)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.use_default_colors()
        curses.cbreak()
        curses.resize_term(30, 80) 
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
            elif key == enter:
                break
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
            elif key == enter:
                break
            elif key == backspace:
                password = password[:-1]
                stdscr.delch()
            else:
                password += chr(key)

        
        name = usersetup.user_login(username, password)        # returns a tuple (Id, UserName, Password) 
        if name == None:
            stdscr.clear()
            stdscr.refresh()
            stdscr.addstr(15,20, "Invalid Credentials Please Try Again")
            stdscr.refresh()
            time.sleep(3)
        elif name[1] == username:
            userpage.user_page(stdscr, name[0], name[1])
            trying = False
            
        else:
            stdscr.clear()
            stdscr.refresh()
            stdscr.addstr(15,20, "Invalid Credentials Please Try Again")
            stdscr.refresh()
            time.sleep(3)
    curses.curs_set(0)
    curses.noecho()
    return