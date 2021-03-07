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

    conn.commit()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Stats (
            Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            TotalWords REAL DEFAULT 0.0,
            TotalTime REAL DEFAULT 0.0,
            Completed INTEGER DEFAULT 0,
            WpmAverage REAL DEFAULT 0.0,
            MissedKeys TEXT,
            MissedMost TEXT,
            UserId INTEGER
            )
    """)
   
    cur.execute("""
        INSERT OR IGNORE INTO Users (UserName, Password) VALUES (?,?)
    """, (un, pswd))
    
    conn.commit()
    conn.close()


def user_look_up(un):
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    out = ''
    cur.execute("""
        SELECT UserName FROM Users WHERE UserName =?
    """, (un,))
    if len(cur.fetchall()) > 0:
        out += "there is already a user by that name"

    else:
        out += "Welcome "+str(un)
    conn.close()
    return out
