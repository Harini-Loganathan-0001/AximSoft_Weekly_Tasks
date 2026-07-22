import sqlite3

conn = sqlite3.connect("instance/jobportal.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(jobs);")

for column in cursor.fetchall():
    print(column)

conn.close()