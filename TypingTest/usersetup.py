from os import unlink
import sqlite3 as sl
import string
import bcrypt



def create_db():
    """
    This creates the database on the first use of the join page
    """
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            UserName TEXT,
            Password TEXT
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
    conn.commit()
    conn.close()





def create_user(un, pswd):
    """
    Runs any time a new user joins
    """
    pswd = pswd.hex()
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Users (UserName, Password) VALUES (?,?)
    """,(un, pswd))
    conn.commit()
    conn.close()


def user_look_up(un):
    """
    Checks to see if a username is taken
    """
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.execute("""
        SELECT UserName FROM Users WHERE UserName =?
    """, (un,))
    if len(cur.fetchall()) > 0:
        conn.close()
        return True
    else:
        conn.close()
        return False

def user_login(un, password):
    """
    retrievs user credentials 
    """
    password = bytes(password, 'utf-8')
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.execute("""
        SELECT Password FROM Users WHERE UserName =?
    """, (un,))
    possible = cur.fetchone()
    possible2 = bytearray.fromhex(possible[0])
    possibilities = ''
    for x in possible2:
        possibilities += chr(x)
    conn.close()
    if len(possible) < 1:
        return "no users by that name"    
    else:
        if bcrypt.checkpw(password, possibilities.encode('utf-8')):
            return "good match"
        else:
            return "no good"