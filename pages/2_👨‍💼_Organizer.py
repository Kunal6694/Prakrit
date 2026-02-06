import streamlit as st
import pandas as pd
import os

st.title("👨‍💼 Organizer Dashboard")

with st.form("service_form"):
    st.subheader("Register New Green Service")
    name = st.text_input("Service Name")
    desc = st.text_area("Green Features (e.g., Solar Powered)")
    price = st.number_input("Price (INR)", min_value=0)
    
    if st.form_submit_button("Add Service"):
        new_data = pd.DataFrame([[name, desc, price]], columns=["Name", "Desc", "Price"])
        path = "../data/services/services.csv"
        # Append to CSV
        if not os.path.exists(path): new_data.to_csv(path, index=False)
        else: new_data.to_csv(path, mode='a', header=False, index=False)
        st.success("Service registered successfully!")
