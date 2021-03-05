import sqlite3 as sl
import string

conn = sl.connect("missedkeys.sqlite")
cur = conn.cursor()

cur.executescript("""
    DROP TABLE IF EXISTS Keys;
    CREATE TABLE IF NOT EXISTS Keys(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE,
        total INTIGER
    );
""")
printable = list(string.printable)
tots = [0] * len(printable) 
base = zip(printable, tots)
cur.executemany("""
    INSERT OR IGNORE INTO Keys (name, total) VALUES (?,?)
""", base)
conn.commit()
conn.close()