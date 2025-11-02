import sqlite3 

def connect_db():
    conn = sqlite3.connect('trackPad.db')
    c= conn.cursor()
    c.execute(''' 
    CREATE TABLE IF NOT EXISTS topics(
              id integer PRIMARY KEY autoincrement,
              topic text,
              name text not null,
              link TEXT NOT NULL,
              approach TEXT)
''')
    conn.commit()
    return conn

def getProblems(topic):
    conn = connect_db()
    c= conn.cursor()
    c.execute("select * from topics where  topic= ?",(topic,))
    data = c.fetchall()
    conn.close()
    return data

def addProblem( topic,name, link, approach):
    conn = connect_db()
    c= conn.cursor()
    c.execute("Insert into topics ( topic,name, link,approach) values(?,?,?,?)", ( topic,name, link, approach))
    conn.commit()
    conn.close()
    return 

def deleteProblem(topic, id):
    conn= connect_db()
    c= conn.cursor()
    c.execute("delete from topics where topic =? and id =?", (topic, id))
    conn.commit()
    conn.close()
    return