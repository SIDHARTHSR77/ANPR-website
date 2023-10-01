import streamlit as st
from streamlit_option_menu import option_menu
import os
from pymongo import MongoClient                      
from datetime import datetime

st.set_page_config(page_title="Sign In",page_icon="✔️",initial_sidebar_state="collapsed")
selected=option_menu(
    menu_title="Sign In to Registered Role",
    options=["User","Admin","Authority"],
    icons=["person-circle","person-gear","person-lines-fill"],
    menu_icon="person-bounding-box",
    default_index=0,
    orientation="horizontal",
)

def user():
    connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
    client=MongoClient(connect_string)
    dbs= client.list_database_names()
    auth_db=client.Authorization
    usercl=auth_db.Users

    with st.form(key="signin",clear_on_submit=False):
        usr=st.text_input(":blue[Username]",placeholder="Enter Username")
        pwd=st.text_input(":blue[Password]",type="password",placeholder="Enter Password")
        st.form_submit_button()
        
    is_user=[]
    dbuser=usercl.find({"username":usr,"pwd":pwd})
    for i in dbuser:
       is_user.append(i)
    #print(is_user)
    if(is_user):
        st.success("Welcome " + usr)
        user_disp()
    else:
        st.error("Account not found")
def user_disp():
    connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
    client=MongoClient(connect_string)
    dbs= client.list_database_names()
    auth_db=client.Authorization
    usercl=auth_db.Users

    auth_db=client.Authorization
    admincl=auth_db.Admin

    
    username=" "
    _loc_list=[]
    _name_list=[]


    def park_loc():
        loc_find=admincl.find({})
        for li in loc_find:
            _loc_list.append(li["ploc"])
        loc_list=list(set(_loc_list))
        #print(loc_list)

        cur_loc=st.selectbox("Select Location For Parking",loc_list)
        

        loc_find=admincl.find({"ploc":cur_loc})
        for li in loc_find:
            _name_list.append(li["pname"])
        name_list=list(set(_name_list))
        #print(name_list)

        cur_pname=st.selectbox("Select Name of Parking",name_list)
        return cur_loc,cur_pname

    _slot_list=[]
    def slot_disp(cur_loc,cur_pname):
        _slot=admincl.find({"ploc":cur_loc,"pname":cur_pname})
        for i in _slot:
            _slot_list.append(i["pslot"])
        slot_list=list(set(_slot_list))
        #print(slot_list)
        st.success("Total = " + str(slot_list[0]))
        park_db=client[cur_loc]
        cbecl=park_db[cur_pname]
        
        fillslots=cbecl.count_documents(filter={"rem_time":" "})
        num=_slot_list[0]-fillslots
        if(num<5):
            st.error(str(num) + " Slots Remaining")
        else:
            st.success(str(num) + " Slots Remaining")

    
    cur_loc,cur_pname=park_loc()
    slot_disp(cur_loc,cur_pname)


def admin():

    connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
    client=MongoClient(connect_string)
    dbs= client.list_database_names()
    auth_db=client.Authorization
    admincl=auth_db.Admin


    with st.form(key="signin",clear_on_submit=False):
        ploc=st.text_input(":blue[Parking Location]",placeholder="Enter Parking Location")
        pname=st.text_input(":blue[Parking Name]",placeholder="Enter Parking Name")
        pwd=st.text_input(":blue[Password]",type="password",placeholder="Enter Password")
        st.form_submit_button()
    is_admin=[]
    dbuser=admincl.find({"pname":pname,"ploc":ploc,"pwd":pwd})
    for i in dbuser:
       is_admin.append(i)
    #print(is_user)
    if(is_admin and ploc=="Coimbatore"):
        if pname=="Indian" or pname=="Modern":
            st.success("Welcome to " + pname + " parking " + ploc)
            admin_dsip(ploc,pname)
    elif is_admin and ploc=="Erode" and pname=="Hyper":
            st.success("Welcome to " + pname + " parking " + ploc)
            admin_dsip(ploc,pname)
    else:
        st.error("Account not found")   
def admin_dsip(ploc,pname):
    connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
    client=MongoClient(connect_string)
    dbs= client.list_database_names()
    park_db=client[ploc]
    cbecl=park_db[pname]

    st.title("Entry and exit of vehicles")
    st.file_uploader(label="Upload File For Detection")
    st.write("OR")
    st.write("Take A Photo from your webcam")
    photo=st.button("Cheese!!")
    if(photo):
        pic=st.camera_input(label="Use Camera to Auto Detect a Number Plate")

    def text_add():
        date=datetime.now()
        time=date.strftime("%m/%d/%y %H:%M:%S")
        num=st.text_input(":blue[Enter the number plate]",placeholder="TN374587")
        if(st.button("Submit")):
            add_value(num,str(time),date)
            st.balloons()

        num1=st.text_input(":blue[Enter the number plate to be Billed]",placeholder="TN374587")
        if(st.button("Remove")):
            remove_val(num1)

    def add_value(nplate,time,date):
        doc={
            "nplate":nplate,
            "time":time,
            "date":date,
            "rem_time":" "
        }
        nplate_exist=cbecl.find_one({"nplate":nplate})
        if(nplate_exist):
            pass
        else:
            cbecl.insert_one(doc)
            st.balloons()

    _rem_list=[]
    get_list=["nplate","date"]
    def remove_val(nplate):
        bill=30
        rplate=cbecl.find({"nplate":nplate})
        for i in rplate:
            _rem_list=[i[key]for key in get_list]
        rem_list=list(set(_rem_list))
        #cbecl.delete_one({"nplate":rem_list[0]})
        st.success("Removed " + str(rem_list[0]))

        rem_time=datetime.now().strftime("%H:%M:%S")
        ent_time=datetime.strftime(rem_list[1],"%H:%M:%S")
        ent=ent_time.split(":")
        rem=rem_time.split(":")
        cbecl.update_one({"nplate":rem_list[0]},{"$set":{"rem_time":rem_time}})
        if(ent[0]==rem[0]):
            st.success("Bill Amount "+str(bill)+"₹")
        else:
            bill_am=int(rem[0])-int(ent[0])
            st.success("Bill Amount "+str(bill_am*bill)+"₹")
        #hr_rate=rem_time-ent_time
        st.write("Entry time:" + ent_time)
        st.write("Remove Time:" + rem_time)

    def bill():
        bill=st.text_input(":blue[Enter Bill Amount]",placeholder="100₹/hr")
        if(st.button("Bill Amount")):
            st.write("Amount=" + bill + "₹")
    text_add()


def auth():
    connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
    client=MongoClient(connect_string)
    dbs= client.list_database_names()
    auth_db=client.Authorization
    authcl=auth_db.Authority


    with st.form(key="signin",clear_on_submit=False):
        pid=st.text_input(":blue[Police ID]",placeholder="Enter Police ID")
        pwd=st.text_input(":blue[Password]",type="password",placeholder="Enter Password")
        st.form_submit_button()

    is_admin=[]
    dbuser=authcl.find({"pid":pid,"pwd":pwd})
    for i in dbuser:
       is_admin.append(i)
    #print(is_user)
    if(is_admin):
        st.success("Signed In Officer")
        auth_disp()
    else:
        st.error("Account not found")
def auth_disp():

    ploc=st.selectbox(":blue[Parking Location]",options=["Coimbatore","Erode"])
    pname=st.selectbox(":blue[Parking Name]",options=["Indian","Modern","Hyper"])
    
    connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
    client=MongoClient(connect_string)
    pname=str(pname)
    park_db=client[ploc]
    cbecl=park_db[pname]
    coll=cbecl.find()
    st.table(coll)

if selected== "User":
    user()
if selected== "Admin":
    admin()
if selected== "Authority":
    auth()