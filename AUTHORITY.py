from pymongo import MongoClient
import streamlit as st


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
       pass
    else:
        authcl.insert_one(doc)
        

username=" "
def auth_sign_up():
    with st.form(key='signup',clear_on_submit=True):
        st.subheader(':green[Authority Sign Up]')
        pid = st.text_input(':blue[Police ID]', placeholder='Enter Your Police ID')
        pwd = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        submit=st.form_submit_button()
    if(submit):
        add_auth(pid,pwd)
        st.balloons()
        st.success("Welcome Officer")
auth_sign_up()
st.table(coll)
st.subheader("nplate=Number Plate")
st.subheader("etime=Entry Time")