"""
    This is the entire point of the program.
    The user types the paragraph produced. Feedback is 
    provided via that aweful windows sound as well as color changes 
    to know what has been typed.
    Michael Murphy
    03/29/2021


    I have included the wiki_pull function into this version of the 
    program bucause for some reason pyinstaller would not include 
    the function in the build. 
"""
import curses
import time
import requests
from bs4 import BeautifulSoup as bs
from bs4 import UnicodeDammit as ud
import sys
import selenium.webdriver as webdriver

escape = 27
enter = 10
backspace = 8
space = 32

def wiki_pull():
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    nonbreakingspace = 160

    try:
        file = requests.get("https://en.wikipedia.org")
        if file.ok == True:
            soup = bs(file.text, features="html.parser") 
            soup = soup.find('p')
            href = soup.find_next('a')
            href = href.get('href')
            href = "https://en.wikipedia.org"+href
            if len(soup) < 10:
                soup = soup.find(id='mp-tfa')
            soup = soup.text.translate(non_bmp_map)
            soup = str(soup)
            soup = soup.lstrip().rstrip()
            
            with open("typetext.txt", "w", encoding="utf8") as text:
                count = 0
                for x in soup:
                    if x == '\n':
                        break
                    elif ord(x) > 127:
                        text.write(' ')
                        count += 1
                    elif x == ' ' and count > 55:
                        text.write('\n')
                        count = 0
                    else:
                        text.write(x)
                        count += 1 
        return href
    except:
        return 



def type_test(stdscr):
    """
    this is the main program function it uses gettext.py to 
    generate text that the user practices typing on.
    
    """
    href = wiki_pull()
    starttime = time.perf_counter()
    curses.curs_set(0)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.use_default_colors()
    curses.update_lines_cols()
    curses.cbreak()
    curses.resize_term(30, 80)  
    stdscr.keypad(True)
    missed_keys = ""

    y = 5                                         # y axis start point
    characters = ""
    with open("typetext.txt", "r") as text:
        for line in text:                         # incomming text is about 60 characters wide 
            stdscr.addstr(y, 0, line)
            y +=1
            for character in line:
                characters += character               # list of all characters for error checking
    text.close()
    
    line_list = characters.split('\n')

    y = 5
    stdscr.move(y, 0)
    characters_typed = 0
    line_typed = 0
    typed = ''
    line_number = 0
    while characters_typed < len(characters):
        try:
            stdscr.addstr(y, 0, typed[:line_typed], curses.color_pair(2))
            stdscr.addstr(y, line_typed, line_list[line_number][line_typed:])
            stdscr.clrtoeol()
            key = stdscr.getch()
            if key == enter and characters[characters_typed] == '\n':               # enter key
                y += 1
                stdscr.move(y, 0)
                typed = ""
                characters_typed += 1
                line_typed = 0
                line_number +=1

            elif key == ord(characters[characters_typed]):
                typed += chr(key)
                characters_typed += 1
                line_typed += 1
            elif key == backspace:
                if line_typed > 0:                                  # backspace
                    typed = typed[:-1]
                    stdscr.refresh()
                    characters_typed -= 1
                    line_typed -= 1
                else:
                    curses.beep()
            elif key == escape:                                                 # escape key
                break
            elif key == enter and characters[characters_typed] == '\n':         # enter key
                y += 1
                stdscr.move(y, 0)
                typed += chr(key)
                characters_typed += 1
                line_typed = 0
            elif key != ord(characters[characters_typed]):                    # missed key
                typed += 'X'
                curses.beep()
                missed_keys += characters[characters_typed]
                characters_typed += 1
                line_typed += 1

            else:
                raise AssertionError
            stdscr.refresh()
        except:
            return missed_keys
    endtime = time.perf_counter()
    words = (characters_typed - len(missed_keys)) / 4.7                                      # avg english word is 4.7 characters 
    elapsed_time = int(endtime - starttime) / 60
    
    if words == 0:
            words_per_min = 0
    else:
        words_per_min = words / elapsed_time
    
    stdscr.clear()
    stdscr.addstr(10, 10, f"You typed {round(words, 1)} words")
    stdscr.addstr(11, 10, f"You missed {len(missed_keys)} keys")
    stdscr.addstr(12, 10, f"Total time typing = {round(elapsed_time, 1)} minutes")
    stdscr.addstr(13, 10, f"You typed {round(words_per_min, 1)} words per min on average")
    stdscr.addstr(14, 10, "Press Enter to return to the main menu")
    stdscr.addstr(17, 10, "Press Space if you would like to read more about the topic")
    next = stdscr.getch()
    if next == space:
        browser = webdriver.Chrome("C:\\Users\\clean\\Desktop\\Utilities\\chromedriver")
        browser.get(href)
    
    return (elapsed_time, words_per_min, missed_keys)