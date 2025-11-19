import sqlite3
import streamlit as st
import os

# Use absolute DB path
DB_PATH = os.path.join(os.getcwd(), "trackPad.db")

def init_db():
    # If DB connection doesn't exist OR is closed, recreate it
    if (
        "db_conn" not in st.session_state
        or st.session_state.db_conn is None
    ):
        st.session_state.db_conn = sqlite3.connect(
            DB_PATH,
            check_same_thread=False
        )

    # Extra safety: verify connection is alive
    try:
        st.session_state.db_conn.execute("SELECT 1")
    except sqlite3.ProgrammingError:
        # Recreate connection if closed
        st.session_state.db_conn = sqlite3.connect(
            DB_PATH,
            check_same_thread=False
        )

    # Ensure table exists
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

# Initialize DB ONCE
init_db()


def getProblems(topic):
    conn = st.session_state.db_conn
    c = conn.cursor()
    c.execute("SELECT id, name, link, approach FROM topics WHERE topic = ?", (topic,))
    data = c.fetchall()
    return data  # ❗ NO conn.close()


def addProblem(topic, name, link, approach):
    conn = st.session_state.db_conn
    c = conn.cursor()
    c.execute(
        "INSERT INTO topics (topic, name, link, approach) VALUES (?, ?, ?, ?)",
        (topic, name, link, approach)
    )
    conn.commit()
    return  # ❗ NO conn.close()


def deleteProblem(id):
    conn = st.session_state.db_conn
    c = conn.cursor()
    c.execute("DELETE FROM topics WHERE id = ?", (id,))
    conn.commit()
    return  # ❗ NO conn.close()
