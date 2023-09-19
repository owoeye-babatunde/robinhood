import streamlit as st

universalName = ''
universalPass = ''

def credential():
        # User login and logout
    global universalName, universalPass
    username = st.text_input("Robinhood Username", type="password")
    password = st.text_input("Robinhood Password", type="password")
    if universalName and universalPass:
        universalName = universalName + str(username)
        universalPass = universalPass + str(password)

    return username, password

def user():
    return universalName, universalPass