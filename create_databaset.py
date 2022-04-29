import sqlite3
conn = sqlite3.connect("database.db")
c = conn.cursor()
 c.execute("""CREATE TABLE IF NOT EXISTS Training_Dataset(
              id INTEGER PRIMARY KEY,
              Review TEXT NOT NULL,
              value  INT  NOT NULL); """)

c.execute("""CREATE TABLE IF NOT EXISTS hotel_links(
             link TEXT NOT NULL); """)
conn.commit()
