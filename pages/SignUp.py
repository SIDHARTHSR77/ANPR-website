import streamlit as st
from streamlit_option_menu import option_menu
import os
from pymongo import MongoClient                      

st.set_page_config(page_title="Sign Up",page_icon="✅",initial_sidebar_state="collapsed")
selected=option_menu(
    menu_title="Sign up to Role",
    options=["User","Admin","Authority"],
    icons=["person-circle","person-gear","person-lines-fill"],
    menu_icon="person-bounding-box",
    default_index=0,
    orientation="horizontal",
)


def admin():
    #------------Start----------#
    sign_up=0 
    
    connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
    client=MongoClient(connect_string)
    dbs= client.list_database_names()
    auth_db=client.Authorization
    admincl=auth_db.Admin

    def add_admin(pname,ploc,pwd,pslot,sign_up):  
        doc={
            "pname":pname,
            "ploc":ploc,
            "pwd":pwd,
            "pslot":pslot,
        } 
        pname_exist=admincl.find_one({"pname":pname})
        ploc_exist=admincl.find_one({"ploc":ploc})
        if(pname_exist and ploc_exist):
            st.warning("Location and Parking Name Exist")
        else:
            admincl.insert_one(doc)
            return 1
            

    username=" "
    ploc=" "
    int_range=range(0,1000,10)
    _loc_list=[]
    def admin_sign_up(sign_up):
        with st.form(key='signup'):
            st.subheader(':green[Admin Sign Up]')
            pname = st.text_input(':blue[Parking Name]', placeholder='Enter The Name of Your Parking')
            ploc = st.text_input(':blue[Parking Location]', placeholder='Enter Location of The Parking')
            pslot=st.select_slider(":blue[Enter Number of Parking Slots]",options=int_range,value=100)
            pwd = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
            pwd2=st.text_input(":blue[Confirm Password]",placeholder="Re-Enter Above Passwrod To Confirm",type="password")
            submit=st.form_submit_button()
        if pwd==pwd2 and pname and ploc and pwd!="":        
            if(submit):
                sign_up=add_admin(pname,ploc,pwd,pslot,sign_up)
                if(sign_up):
                    st.balloons()
                    st.success(str(pname) + " Parking" + " Created Successfully")
        else:
            st.warning("Enter Correct Credentials")
        
    admin_sign_up(sign_up)

    #----------END------------#

def user():
    #--------------START---------#

    connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
    client=MongoClient(connect_string)
    dbs= client.list_database_names()
    auth_db=client.Authorization
    usercl=auth_db.Users

    auth_db=client.Authorization
    admincl=auth_db.Admin

    park_db=client.Parking_Loc
    cbecl=park_db.coimbatore

    def add_users(name,email,pwd):  
        doc={
            "username":name,
            "email":email,
            "pwd":pwd
        } 
        email_exist=usercl.find_one({"email":email})
        if(email_exist):
            st.error("Email Already exists")
        else:
            user_id=usercl.insert_one(doc).inserted_id
            return 1
        

    def user_sign_up():
        with st.form(key='signup',clear_on_submit=False):
            st.subheader(':green[User Sign Up]')
            email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
            username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
            pwd = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
            pwd2 = st.text_input(':blue[Confirm Password]', placeholder='Re-Enter Above Password', type='password')
            submit=st.form_submit_button()
        if(pwd==pwd2 and email and username ):
            if(submit):
                if(pwd!=""):
                    if(add_users(username,email,pwd)):
                        st.balloons()
                        st.success("Welcome "+ username)
                else:
                    st.error("Enter Password")
        else:
            st.warning("Enter Correct Credentials")

    user_sign_up()

    #-------------END-------------#

def auth():
    #-----------START-----------#
    connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
    client=MongoClient(connect_string)
    dbs= client.list_database_names()
    auth_db=client.Authorization
    authcl=auth_db.Authority

    park_db=client.Parking_Loc
    cbecl=park_db.coimbatore
    coll=cbecl.find()

    def add_auth(pid,pwd):  
        doc={
            "pid":pid,
            "pwd":pwd
        } 
        pid_exist=authcl.find_one({"pid":pid})
        if(pid_exist):
            st.warning("Police ID Exists")
        else:
            authcl.insert_one(doc)
            return 1
            

    username=" "
    def auth_sign_up():
        with st.form(key='signup',clear_on_submit=False):
            st.subheader(':green[Authority Sign Up]')
            pid = st.text_input(':blue[Police ID]', placeholder='Enter Your Police ID')
            pwd = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
            pwd2 = st.text_input(':blue[Confirm Password]', placeholder='Re-Enter Above Password', type='password')
            submit=st.form_submit_button()
        if(pwd==pwd2 and pwd!="" and pid):    
            if(submit):
                if(add_auth(pid,pwd)):
                    st.balloons()
                    st.success("Welcome Officer")
        else:
            st.warning("Enter Correct Credentials")
    auth_sign_up()
    #---------------------END---------------#

if selected== "User":
    user()
if selected== "Admin":
    admin()
if selected== "Authority":
    auth()