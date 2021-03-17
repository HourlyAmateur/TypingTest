import sqlite3 as sl
import string
import bcrypt
import time


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


#################################################################
def create_user(un, pswd):
    """
    Runs any time a new user joins
    """
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Users (UserName, Password) VALUES (?,?)
    """,(un, pswd))
    conn.commit()

    cur.execute("""
        SELECT Id FROM Users WHERE UserName = ?
    """, (un, ))
    userid = cur.fetchone()
    cur.execute("""
    --sql
        INSERT INTO Stats (UserId) VALUES (?)
    ;
    """, (userid[0], ))
    conn.commit
    conn.close()


########################################################
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


########################################################
def user_login(un, password):
    """
    retrieves user credentials 
    """
    password2 = bytes(password, 'utf-8')
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.execute("""
        SELECT Password FROM Users WHERE UserName =?
    """, (un,))
    possible = cur.fetchone()
    conn.close()
    if possible == None:
        return None    
    else:
        if bcrypt.checkpw(password2, possible[0]):
            return un
    
#################################################################

def user_stats(un):
    """
    WORK IN PROGRESS
    retrieves users statistics from the database
    """
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM Stats WHERE UserId = ?
    """,(un,))  

##################################################################

def add_stats(un, pk, time, wpm, words):
    """
    WORK IN PROGRESS
    adds user data to the statistics table
    """
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Stats (TotalWords + ?, TotalTime + ?, Completed + 1, (WpmAverage + wpm) / 2)    
        VALUES (?,?,?) WHERE UserId = pk 
    """, (words, time, wpm))

####################################################################

def add_keys(pk, missed):
    """
    WORK IN PROGRESS
    adds missed keys to the database
    """
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO Stats key VALUES (?) WHERE UserId = pk
    """, missed)