import streamlit as st
import pandas as pd
import os

st.title("🛒 Prakrit Marketplace")
st.subheader("Book Verified Eco-Friendly Events")

if os.path.exists("../data/services/services.csv"):
    services = pd.read_csv("../data/services/services.csv")
    for i, row in services.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            col1.write(f"### {row['Name']}")
            col1.write(row['Desc'])
            if col2.button(f"Book for ₹{row['Price']}", key=i):
                st.balloons()
                st.success(f"Booking request sent for {row['Name']}!")
else:
    st.info("Marketplace is currently empty. Waiting for organizers to list services.")
