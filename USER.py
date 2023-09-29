from pymongo import MongoClient
import streamlit as st


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
       pass
    else:
        user_id=usercl.insert_one(doc).inserted_id
    
username=" "
_loc_list=[]
_name_list=[]

def user_sign_up():
    with st.form(key='signup',clear_on_submit=True):
        st.subheader(':green[User Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        submit=st.form_submit_button()
    if(submit):
        add_users(username,email,password)
        st.balloons()
        st.success("Welcome "+ username)
        #park_loc()

def park_loc():
    loc_find=admincl.find({})
    for li in loc_find:
        _loc_list.append(li["ploc"])
    loc_list=list(set(_loc_list))
    #print(loc_list)

    cur_loc=st.selectbox("Select Location For Parking",loc_list)
    cloc=st.button("Confirm Location")
    if(cloc):
        st.write("Welcome to " + cur_loc)

    loc_find=admincl.find({"ploc":cur_loc})
    for li in loc_find:
        _name_list.append(li["pname"])
    name_list=list(set(_name_list))
    #print(name_list)

    cur_pname=st.selectbox("Select Name of Parking",name_list)
    cpname=st.button("Confirm Parking Name")
    if(cpname):
        st.write("Welcome to " + cur_pname)
    return cur_loc,cur_pname

_slot_list=[]
def slot_disp(cur_loc,cur_pname):
    _slot=admincl.find({"ploc":cur_loc,"pname":cur_pname})
    for i in _slot:
        _slot_list.append(i["pslot"])
    slot_list=list(set(_slot_list))
    #print(slot_list)
    st.success("Total = " + str(slot_list[0]))
    if(cur_loc=="Coimbatore" and cur_pname=="Indian"):
        fillslots=cbecl.count_documents(filter={})
        num=_slot_list[0]-fillslots
        if(num<5):
            st.error(str(num) + " Slots Remaining")
        else:
            st.success(str(num) + " Slots Remaining")

user_sign_up()
cur_loc,cur_pname=park_loc()
slot_disp(cur_loc,cur_pname)
