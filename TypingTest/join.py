import curses
import time
import bcrypt
import usersetup

# macros
escape = 27
enter = 10
backspace = 8

def join(stdscr):

    usersetup.create_db()                  
    noname = True
    while noname:
        stdscr.clear()
        curses.echo()
        curses.curs_set(2)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.use_default_colors()
        curses.cbreak()
        curses.resize_term(30, 75) 
        curses.update_lines_cols() 
        stdscr.keypad(True)

        
        stdscr.addstr(10, 32, "CREATE A USERNAME")
        stdscr.addstr(15, 25, "When completed you will be redirected")
        stdscr.addstr(16, 32, "to the main page to log in")
        stdscr.addstr(20, 32, "CREATE A PASSWORD")
        
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
        username = username[:-1]
        noname = usersetup.user_look_up(username) 
        if noname == True:
            stdscr.addstr(8, 32, "There is already a user by that name")
            stdscr.addstr(9, 32, "Please try again.")
            stdscr.refresh()
            time.sleep(3)
            stdscr.clear()
        else:
            stdscr.addstr(8, 32, f"Welcome to the party {username}")
            stdscr.refresh()
        


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
    
    password2 = bytes(password[:-1], "utf-8")
    hashedpw = bcrypt.hashpw(password2, bcrypt.gensalt())
    usersetup.create_user(username, hashedpw)

    curses.curs_set(0)
    curses.noecho()
    return

