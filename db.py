import psycopg2
import streamlit as st

def get_conn():
    if "db_conn" not in st.session_state:
        st.session_state.db_conn = psycopg2.connect(
            st.secrets["DATABASE_URL"],
            sslmode="require")
    return st.session_state.db_conn
    

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id SERIAL PRIMARY KEY,
            topic TEXT NOT NULL,
            name TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            approach TEXT
        )
    """)
    conn.commit()


def getProblems(topic):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, link, approach FROM topics WHERE topic = %s",
        (topic,)
    )
    return cur.fetchall()



def addProblem(topic, name, link, approach):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO topics (topic, name, link, approach)
        VALUES (%s, %s, %s, %s)
        """,
        (topic, name, link, approach)
    )
    conn.commit()


def deleteProblem(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM topics WHERE id = %s",
        (id,)
    )
    conn.commit()

