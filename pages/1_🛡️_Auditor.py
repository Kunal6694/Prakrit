
import streamlit as st
import pandas as pd
import os

st.title("🛡️ NGO Auditor Portal")
st.info("Upload sustainability reports here for AI-powered verification.")

uploaded_file = st.file_uploader("Upload Organizer Report (.txt)", type="txt")

if uploaded_file:
    # Save to the 'Hot Folder' your Pathway main.py is watching
    save_path = f"../data/input/{uploaded_file.name}"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Audit started for: {uploaded_file.name}")

st.divider()
st.subheader("Live Verification Feed")
if os.path.exists("../audit_results.csv"):
    df = pd.read_csv("../audit_results.csv")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No audit results yet. Drop a file to begin.")
