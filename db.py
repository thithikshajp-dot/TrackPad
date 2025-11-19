import sqlite3
import streamlit as st
import os

Db_Path = os.path.join(os.getcwd(), "trackPad.db")

def init_db():
    if "db_conn" not in st.session_state:
        st.session_state.db_conn = sqlite3.connect(Db_Path, check_same_thread=False)

    # test connection
    try:
        st.session_state.db_conn.execute("SELECT 1")
    except sqlite3.ProgrammingError:
        st.session_state.db_conn = sqlite3.connect(Db_Path, check_same_thread=False)

    # ensure table
    c = st.session_state.db_conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            name TEXT NOT NULL,
            link TEXT NOT NULL,
            approach TEXT
        )
    """)
    st.session_state.db_conn.commit()


def getProblems(topic):
    init_db()  # ensure connection exists
    conn = st.session_state.db_conn
    c = conn.cursor()
    c.execute("SELECT id, name, link, approach FROM topics WHERE topic=?", (topic,))
    return c.fetchall()


def addProblem(topic, name, link, approach):
    init_db()
    conn = st.session_state.db_conn
    c = conn.cursor()
    c.execute(
        "INSERT INTO topics (topic, name, link, approach) VALUES (?, ?, ?, ?)",
        (topic, name, link, approach)
    )
    conn.commit()


def deleteProblem(id):
    init_db()
    conn = st.session_state.db_conn
    c = conn.cursor()
    c.execute("DELETE FROM topics WHERE id=?", (id,))
    conn.commit()
