from os import unlink
import sqlite3 as sl
import string


def init_user(un, pswd):
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            UserName TEXT UNIQUE,
            Password INTEGER 
            )        
    """)

    
    cur.execute("""CREATE TABLE IF NOT EXISTS {} (
            Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            Key TEXT UNIQUE,
            Total INTEGER,
            TotalWords REAL,
            TotalTime REAL,
            Completed INTEGER,
            WpmAverage REAL,
            3Missed TEXT 
            )
    """.format(un))
   
    printable = list(string.printable)
    tots = [0] * len(printable) 
    base = zip(printable, tots)
    cur.execute("""
        INSERT OR IGNORE INTO Users (UserName, Password) VALUES (?,?)
    """, (un, pswd))
    
    cur.executemany("""INSERT OR IGNORE INTO {} (Key, Total) VALUES (?,?) 
    """.format(un), base)
    
    cur.execute("""INSERT OR IGNORE INTO {} (
        TotalWords, TotalTime, Completed, WpmAverage, 3Missed
        ) VALUES (?,?,?,?,?)
    """.format(un), (0,0,0,0,0))
    conn.commit()
    conn.close()