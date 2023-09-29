from pymongo import MongoClient
import streamlit as st

connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
client=MongoClient(connect_string)
dbs= client.list_database_names()
auth_db=client.Authorization
admincl=auth_db.Admin

def add_admin(pname,ploc,pwd,pslot):  
    doc={
        "pname":pname,
        "ploc":ploc,
        "pwd":pwd,
        "pslot":pslot,
    } 
    pname_exist=admincl.find_one({"pname":pname})
    ploc_exist=admincl.find_one({"ploc":ploc})
    if(pname_exist and ploc_exist):
       pass
    else:
        admincl.insert_one(doc)
        

username=" "
ploc=" "
int_range=range(0,1000,10)
_loc_list=[]
def admin_sign_up():
    with st.form(key='signup',clear_on_submit=True):
        st.subheader(':green[Admin Sign Up]')
        pname = st.text_input(':blue[Parking Name]', placeholder='Enter The Name of Your Parking')
        ploc = st.text_input(':blue[Parking Location]', placeholder='Enter Location of The Parking')
        pslot=st.select_slider(":blue[Enter Number of Parking Slots]",options=int_range,value=10)
        pwd = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        submit=st.form_submit_button()
    if(submit):
        add_admin(pname,ploc,pwd,pslot)
        #loc_list.append(ploc)
        st.balloons()
        st.success("Welcome To " + str(pname) + " Parking")

admin_sign_up()

def park_loc():
    loc_find=admincl.find({})
    for li in loc_find:
        _loc_list.append(li["ploc"])
    loc_list=list(set(_loc_list))
    #print(loc_list)
