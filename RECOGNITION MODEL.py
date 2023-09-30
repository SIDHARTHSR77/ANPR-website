from pymongo import MongoClient
import streamlit as st
from datetime import datetime


connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
client=MongoClient(connect_string)
dbs= client.list_database_names()
park_db=client.Parking_Loc
cbecl=park_db.coimbatore


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
        "date":date
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
    rplate=cbecl.find({"nplate":nplate})
    for i in rplate:
        _rem_list=[i[key]for key in get_list]
    rem_list=list(set(_rem_list))
    cbecl.delete_one({"nplate":rem_list[1]})
    st.success("Removed " + rem_list[1])
    rem_date=datetime.now()
    rem_time=rem_date.strftime("%H:%M:%S")
    ent_time=datetime.strftime(rem_list[0],"%H:%M:%S")
    #hr_rate=rem_time-ent_time
    st.write("Entry time:" + ent_time)
    
    st.write("Remove Time:" + rem_time)
    bill()

def bill():
    bill=st.text_input(":blue[Enter Bill Amount]",placeholder="100₹/hr")
    if(st.button("Bill Amount")):
        st.write("Amount=" + bill + "₹")
text_add()