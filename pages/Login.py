import streamlit as st
from streamlit_option_menu import option_menu
import os
from pymongo import MongoClient                      

st.set_page_config(page_title="Sign Up",page_icon="✅")
selected=option_menu(
    menu_title="Login to Role",
    options=["User","Admin","Authority"],
    icons=["person-circle","person-gear","person-lines-fill"],
    menu_icon="person-bounding-box",
    default_index=0,
    orientation="horizontal",
)

def user():
    pass

def admin():
    pass

def auth():
    pass


if selected== "User":
    user()
if selected== "Admin":
    admin()
if selected== "Authority":
    auth()