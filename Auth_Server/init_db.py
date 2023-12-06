import sqlite3

connection = sqlite3.connect('./db/database.db')


with open('./db/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (name, phone, email, password) VALUES ('kareem el-giushy', '+123456789', 'kareem@k.c', '123')")

connection.commit()
connection.close()