import curses
import time
import sqlite3 as sq 
import gettext
import usersetup

escape = 27
enter = 10
backspace = 8

def type_test(stdscr):
    """
    this is the main program function it uses gettext.py to 
    generate text that the user practices typing on.
    
    """
    gettext.wiki_pull()
    starttime = time.perf_counter()
    curses.curs_set(0)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.use_default_colors()
    curses.update_lines_cols()
    curses.cbreak()
    curses.resize_term(30, 75)  
    stdscr.keypad(True)
    missedkeys = []

    y = 5                                         # y axis start point
    characters = ""
    with open("typetext.txt", "r") as text:
        for line in text:                         # incomming text is about 60 characters wide 
            stdscr.addstr(y, 0, line)
            y +=1
            for character in line:
                characters += character               # list of all characters for error checking
    text.close()
    
    linelist = characters.split('\n')

    y = 5
    stdscr.move(y, 0)
    characterstyped = 0
    linetyped = 0
    typed = ''
    linenum = 0
    while characterstyped < len(characters):
        try:
            stdscr.addstr(y, 0, typed[:linetyped], curses.color_pair(2))
            stdscr.addstr(y, linetyped, linelist[linenum][linetyped:])
            stdscr.clrtoeol()
            key = stdscr.getch()
            if key == enter and characters[characterstyped] == '\n':               # enter key
                y += 1
                stdscr.move(y, 0)
                typed = ""
                characterstyped += 1
                linetyped = 0
                linenum +=1

            elif key == ord(characters[characterstyped]):
                typed += chr(key)
                characterstyped += 1
                linetyped += 1
            elif key == backspace:
                if characterstyped > 0:                                  # backspace
                    typed = typed[:-1]
                    stdscr.refresh()
                    characterstyped -= 1
                    linetyped -= 1
                else:
                    pass
            elif key == escape:                                                 # escape key
                break
            elif key == enter and characters[characterstyped] == '\n':         # enter key
                y += 1
                stdscr.move(y, 0)
                typed += chr(key)
                characterstyped += 1
                linetyped = 0
            elif key != ord(characters[characterstyped]):                    # missed key
                typed += 'X'
                curses.beep()
                missedkeys.append(characters[characterstyped])
                characterstyped += 1
                linetyped += 1

            else:
                raise AssertionError
            stdscr.refresh()
        except:
            return missedkeys
    endtime = time.perf_counter()
    words = characterstyped / 4.7                                      # avg english word is 4.7 characters 
    elapsedtime = int(endtime - starttime) / 60
    wordspermin = words / elapsedtime
    stdscr.clear()
    stdscr.addstr(10, 10, f"you typed {round(words, 1)} words")
    stdscr.addstr(11, 10, f"you missed {len(missedkeys)} keys")
    stdscr.addstr(12, 10, f"total time typing = {round(elapsedtime, 1)} minutes")
    stdscr.addstr(13, 10, f"you typed {round(wordspermin, 1)} words per min on average")
    stdscr.addstr(14, 10, "press any key to return to the main menu")
    stdscr.getch()
    
    return (elapsedtime, wordspermin, missedkeys)