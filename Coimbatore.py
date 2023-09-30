from pymongo import MongoClient
import streamlit as st


connect_string=f"mongodb+srv://sidhu:UBFgxiKtIQOAPmUg@test03.cswex3i.mongodb.net/"
client=MongoClient(connect_string)
dbs= client.list_database_names()
park_db=client.Parking_Loc
cbecl=park_db.coimbatore

fslots=cbecl.count_documents(filter={})
st.write(fslots)
