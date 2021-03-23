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
        totalwords = data[1]
        totaltime = data[2]
        completed = data[3]
        wpm = data[4]
        missed = data[5]
        missedmost = data[6]

        stdscr.addstr(10, 15, f"Welcome Back {un}")
        stdscr.addstr(12, 15, f"You have spent {round(totaltime,1)} miniutes typing")
        stdscr.addstr(13, 15, f"Congratulations you have completed {completed} texts")
        stdscr.addstr(14, 15, f"Your current typing speed average is {round(wpm, 1)} WPM")
        stdscr.addstr(15, 15, f"Your top 3 most often missed keys are {missedmost}")
        stdscr.addstr(17, 15, "Press Enter to play todays text")
        stdscr.addstr(18, 15, "Press Escape to Exit")
        stdscr.refresh()
        key = stdscr.getch()
        if key == escape:
            return
        else:
            stdscr.clear()
            elapsedtime, totwpm, missedkeys = Typing_TestV2.type_test(stdscr)
            usersetup.add_stats(id, elapsedtime, totwpm, missedkeys)
            stdscr.clear()
        
    return