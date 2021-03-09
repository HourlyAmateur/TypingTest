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
    conn.commit()
    conn.close()





def create_user(un, pswd):
    """
    Runs any time a new user joins
    """
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Users (UserName, Password) VALUES (?,?)
    """, (un, pswd))
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
    password = bytes(password, "UTF-8")
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.execute("""
        SELECT Password FROM Users WHERE UserName =?
    """, (un,))
    users = cur.fetchall()
    conn.close()
    if len(users) < 1:
        return "there are no users by that name"
        
    else:
        if bcrypt.checkpw(password, users[0][0]):
            print("good match")
        else:
            print("no good")