import streamlit as st
from components.ui_elements import PrakritUI
from streamlit_lottie import st_lottie

st.title("🛡️ AI Verification Authority")

cursor = db.cursor()
lottie_scan = PrakritUI.load_lottie("https://lottie.host/7e00845a-6058-4505-8704-8742d4a205a2/Fis7I6P1U6.json")

col1, col2 = st.columns([1.5, 1])
with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Data Uplink Stream")

    # 1. Fetch organizers to audit
    cursor.execute("SELECT username, company FROM users WHERE role = 'Event Organizer'")
    orgs = cursor.fetchall()
    org_list = {f"{o[1]} (@{o[0]})": o[0] for o in orgs}

    selected_label = st.selectbox("Select Organizer to Audit",
                                  list(org_list.keys()) if org_list else ["No Organizers Found"])

    report = st.file_uploader("Upload Sustainability Proof", type=['txt', 'pdf'])

    if st.button("🚀 Execute AI Audit"):
        if report and org_list:
            # Simulate AI analysis and update SQLite database
            target_username = org_list[selected_label]
            cursor.execute("UPDATE users SET audited = 1, score = 9.8 WHERE username = ?", (target_username,))
            db.commit()
            st.success(f"Audit Complete! {selected_label} score updated to 9.8.")
        else:
            st.warning("Please upload a file and select a valid organizer.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if lottie_scan:
        st_lottie(lottie_scan, height=250)

# Real-time Audit Log from SQLite
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.write("### 📈 Verified Partners Feed")
cursor.execute("SELECT company, score, location FROM users WHERE audited = 1")
audited_df = cursor.fetchall()
if audited_df:
    import pandas as pd

    df = pd.DataFrame(audited_df, columns=["Company", "AI Score", "Location"])
    st.dataframe(df, use_container_width=True)
else:
    st.write("System status: Idle. Awaiting audit execution.")
st.markdown('</div>', unsafe_allow_html=True)