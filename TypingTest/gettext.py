import requests
from bs4 import BeautifulSoup as bs
from bs4 import UnicodeDammit as ud
import sys


def wiki_pull():
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    nonbreakingspace = 160

    file = requests.get("https://en.wikipedia.org")
    if file.ok == True:
        soup = bs(file.text, features="html.parser")
        soup = soup.find('p')
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
                elif ord(x) == nonbreakingspace:
                    text.write(' ')
                    count += 1
                elif x == ' ' and count > 60:
                    text.write('\n')
                    count = 0
                else:
                    text.write(x)
                    count += 1 

