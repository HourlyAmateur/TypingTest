import curses
import time
import bcrypt
import usersetup


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
    stdscr.addstr(15, 25, "When completed you will be redirected")
    stdscr.addstr(16, 32, "to the main page to log in")
    stdscr.addstr(20, 32, "CREATE A PASSWORD")
    
    stdscr.move(12, 32)
    username = ''
    key = None
    while key != 10:
        key = stdscr.getch()
        if key == 27:
            curses.curs_set(0)
            return 0
        elif key == 8:
            username = username[:-1]
            stdscr.delch()
        else:
            username += str(key)
    
    stdscr.addstr(8, 25, usersetup.user_look_up(username))


    stdscr.move(22, 32)
    password = ''
    key = None
    while key != 10:
        key = stdscr.getch()
        if key == 27:
            curses.curs_set(0)
            return 0
        elif key == 8:
            password = password[:-1]
            stdscr.delch()
        else:
            password += chr(key)
    
    password = bytes(password, "utf-8")
    hashedpw = bcrypt.hashpw(password, bcrypt.gensalt())
    usersetup.init_user(str(username), str(hashedpw))
    curses.curs_set(0)
    
