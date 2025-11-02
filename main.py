import streamlit as st
from db import getProblems, addProblem, deleteProblem
import pandas as pd
import time

if "page" not in st.session_state:
    st.session_state.page = "home"

if "current_topic" not in  st.session_state:
    st.session_state.current_topic =None

def openTopic(topic_name):
    st.session_state.page  = "topic"
    st.session_state.current_topic = topic_name

def goHome():
    st.session_state.page = "home"
    st.session_state.current_topic = None
def homePage():
    st.title("DSA TRACKPAD")
    st.subheader("Dash Board to track Data Structure and Algorithms")

    st.markdown("---")

    st.write(" 1 % of Progress every day makes u a better person")
    topics= [" Modified Binary Search"," Binary Tree Traversals"," DFS"," BFS","Matrix Traversals"," Back Tracking","Dynamic Programming","Prefix Sum",
            "Two Pointers","Sliding window","Fast and Slow Pointers","Linked List in place Reversal","Monotomic Stack","Top K Elements","Over Lapping Intervals"]

    st.markdown(f"Ther are ***{len(topics)}*** important patterns to learn from DSA")
    st.markdown("---")


    for i in range(0, len(topics) , 3):
        cols = st.columns(3)
        for j , k in enumerate(cols):
            idx = i+j
            if idx< len(topics):
                with k:
                    if(st.button(topics[idx])):
                        openTopic(topics[idx])

    st.divider()
    st.title("The popular sheets to Ace DSA:")
    st.markdown("[Striver's SDE sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2)")
    st.markdown("[SDE sheet by Love Babbar](https://www.geeksforgeeks.org/dsa/dsa-sheet-by-love-babbar/)")
    st.markdown("[Apna College DSA sheet](https://docs.google.com/spreadsheets/d/1hXserPuxVoWMG9Hs7y8wVdRCJTcj3xMBAEYUOXQ5Xag/edit?gid=0#gid=0)")
    st.markdown("[FAANG Interview sheet](https://www.interviewbit.com/faang-interview-questions/)")
    st.markdown("[Neetcode 150 sheet](https://neetcode.io/practice?subpage=practice)")

    st.divider()


def topicPage():
    st.title(f"Topic: {st.session_state.current_topic}")
    st.subheader("The Problems solved in this topic is listed below:")
    data = getProblems(st.session_state.current_topic)
    if data:
        st.subheader("Problems solved till date:")
        df = pd.DataFrame(data, columns=['ID', 'TOPIC', 'NAME','LINK', 'APPROACH'])
        df.index = df.index + 1
        st.table(df)
    else:
        st.write("Make an attempt to add a new problem into the list")

    st.divider()
    st.subheader("Add a new entry:")

    if "show_form" not in st.session_state:
        st.session_state.show_form = False

    if st.button("Add Problem Entry"):
        st.session_state.show_form = not st.session_state.show_form

    if st.session_state.show_form:
        with st.form("add_problems"):
            name = st.text_input("Enter the Problem Name")
            link = st.text_input("Enter the problem Link( LeetCode/ GeeksForGeeks/HackerRank...)")
            approach = st.text_area("Note down the brief description of ur optimised approach to solve the problem")
            submitted= st.form_submit_button("Add Entry")

            if submitted:
                if name.strip() =="" or link.strip()== "" or approach.strip() == "":
                    st.warning("Please fill all the fields")
                else:
                    addProblem(st.session_state.current_topic, name, link, approach)
                    st.success('''Data entry added Successfully!!
                            One dop makes a might ocean!
                            Good Work Boyy!!! ''')
                    st.session_state.show_form = False
                    st.rerun()

    st.divider()
    st.subheader("Delete an entry:")
    if "delete_confirm" not in st.session_state:
        st.session_state.delete_confirm = False

    if st.button("Delete A Entry"):
        st.session_state.delete_confirm = not st.session_state.delete_confirm
    if st.session_state.delete_confirm:
        with st.form("Delete Entry"):
            delete_num = st.number_input("Enter the ID to be dleted", min_value =1, step =1)
            deleted = st.form_submit_button("Delete Entry")
        if deleted:
            deleteProblem(st.session_state.current_topic, delete_num)
            st.success("Entry Deleted Successfully!!")
            time.sleep(1.5)
            st.session_state.delete_confirm = False
            st.rerun()
    st.divider()

    st.button("Back to home" ,on_click = goHome)


if st.session_state.page == "home":
    homePage()

elif st.session_state.page == "topic":
    topicPage()