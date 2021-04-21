"""
    This module stores all of the functions used for 
    accessing the database.
    Michael Murphy
    03/29/2021
"""

import sqlite3 as sl
import string
import bcrypt

keychars = []
[keychars.append(x) for x in string.ascii_uppercase]

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
            MissedKeys TEXT DEFAULT '!',
            MissedMost TEXT,
            UserId INTEGER
            )
    """)
    conn.commit()
   

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
        SELECT * FROM Users WHERE UserName =?
    """, (un,))
    possible = cur.fetchone()                   # (Id,  UserName, Password)
    conn.close()
    if possible == None:
        return None    
    else:
        if bcrypt.checkpw(password2, possible[2]):
            return possible
        else:
            return (1, 1)
    
#################################################################

def user_stats(id):
    """
    retrieves users statistics from the database
    """
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM Stats WHERE UserId = ?
    """,(id,))
    data = cur.fetchone()
    conn.close() 
    return data 

##################################################################

def add_stats(pk, time, wpm, missed):
    """
    adds user data to the statistics table
    """
    conn = sl.connect("userdata.sqlite")
    cur = conn.cursor()
    cur.execute("""
    --sql
        UPDATE Stats SET TotalTime = TotalTime + ? WHERE UserId = ? 
    ;
    """, (time, pk))

    if time > 3:                # only add a completed text if user typed long enought
        cur.execute("""
        --sql
            UPDATE Stats SET Completed = Completed + 1 WHERE UserId = ?
        ;
        """, (pk, ))
        conn.commit()
    
    cur.execute("""
    --sql
        SELECT Completed FROM Stats WHERE UserId = ?
    ;
    """, (pk, ))
    complete = cur.fetchone()
    if complete[0] > 1 and time > 2:

        cur.execute("""
        --sql
            UPDATE Stats SET WpmAverage = (WpmAverage + ?) / 2  WHERE UserId = ?
        ;
        """, (wpm, pk))

    elif complete[0] < 1 and time > 2:
        cur.execute("""
        --sql
            UPDATE Stats SET WpmAverage = ? WHERE UserId = ? 
        ;
        """, (wpm, pk))
    else:
        pass

    conn.commit()


    cur.execute("""
    --sql
        UPDATE Stats SET MissedKeys = MissedKeys || ? WHERE UserId = ? 
    ;
    """, (missed, pk))
    conn.commit()

    cur.execute("""
    --sql
        SELECT MissedKeys FROM Stats WHERE UserId = ?
    ;
    """, (pk, ))
    miss = cur.fetchone()
    key_list = sorted(list(miss[0]))
    key_dict = {}
    for i in key_list:
        key_dict[i] = key_dict.get(i, 1) + 1

    sorted_keys = sorted(key_dict.items(), key=lambda x: x[1])

    mostst = ""
    most = sorted_keys[-3:]
    for k,v in most[::-1]:
        if k == '\n':
            mostst += "ENT, "
        elif k == ' ':
            mostst += "SPC, "
        else:
            mostst += k+", "
        

    cur.execute("""
    --sql
        UPDATE Stats SET MissedMost = ? WHERE UserId = ?
    ;
    """, (mostst, pk))
    conn.commit()
    conn.close()
