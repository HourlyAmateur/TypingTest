import curses
import time
import usersetup
import Typing_TestV2

escape = 27
play = True
def user_page(stdscr, id, un):
    while play == True:
        stdscr.clear()
        curses.echo()
        curses.curs_set(2)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.use_default_colors()
        curses.cbreak()
        curses.resize_term(30, 75) 
        curses.update_lines_cols() 
        stdscr.keypad(True)

        data = usersetup.user_stats(id)
        totalwords = data[0]
        totaltime = data[1]
        completed = data[2]
        wpm = data[3]
        missed = data[4]
        missedmost = data[5]

        stdscr.addstr(10, 20, f"Welcome Back {un}")
        stdscr.addstr(12, 20, f"You have spent {totaltime} miniutes typing")
        stdscr.addstr(13, 20, f"Congratulations you have completed {completed} texts")
        stdscr.addstr(14, 20, f"Your current typing speed average is {wpm} Words per miniute")
        stdscr.addstr(15, 20, f"Your top 3 most often missed keys are {missedmost}")
        stdscr.addstr(17, 20, "Press enter to play todays text")
        stdscr.refresh()
        key = stdscr.getch()
        if key == escape:
            return
        else:
            stdscr.clear()
            Typing_TestV2.type_test(stdscr)
            stdscr.clear()
        
    return