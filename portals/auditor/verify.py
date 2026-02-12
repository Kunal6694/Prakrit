import streamlit as st
import google.generativeai as genai
from datetime import datetime
from components.ui_elements import PrakritUI
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
cursor = db.cursor()

st.title("🛡️ NGO Verification Portal")

tab_cl, tab_aud = st.tabs(["📋 Active Stream", "✅ Audit History"])

with tab_cl:
    st.subheader("Bookings Requiring Verification")
    # Fetch Paid & Confirmed bookings not yet audited
    cursor.execute("""SELECT * FROM bookings WHERE status = 'Paid & Confirmed' 
                      AND (audit_status IS NULL OR audit_status = '')""")
    active = cursor.fetchall()

    for b in active:
        with st.expander(f"Audit Order {b[1]} - {b[3]}"):
            st.write(f"**Event Details:** {b[6]}")
            if st.button(f"Claim Audit for {b[1]}", key=f"cl_{b[1]}"):
                cursor.execute("UPDATE bookings SET audit_status = 'Claimed', auditor_name = ? WHERE booking_id = ?",
                               (u['username'], b[1]))
                db.commit(); st.rerun()

# --- Audit Execution Section ---
st.divider()
cursor.execute("SELECT * FROM bookings WHERE auditor_name = ? AND audit_status = 'Claimed'", (u['username'],))
claims = cursor.fetchall()

if claims:
    st.subheader("🚀 Execute AI Audit")
    sel_b = st.selectbox("Select Booking to Audit", [c[1] for c in claims])
    pdf_report = st.file_uploader(f"Upload Audit PDF for {sel_b}", type=['pdf'])

    if st.button("Submit to Gemini AI"):
        if pdf_report:
            with st.spinner("Gemini AI Analyzing Geolocation & Proofs..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = "Analyze this sustainability audit report. Provide a score from 1.0 to 10.0. Return ONLY the number."
                    pdf_data = pdf_report.read()
                    response = model.generate_content([prompt, {"mime_type": "application/pdf", "data": pdf_data}])

                    score = float(response.text.strip())
                    is_eco = score >= 7.5
                    now = datetime.now().strftime("%Y-%m-%d %H:%M")

                    # Update Booking & Status
                    cursor.execute("""UPDATE bookings SET audit_score = ?, audit_status = 'Verified', 
                                      status = ? WHERE booking_id = ?""",
                                   (score, 'Verified Eco-Friendly' if is_eco else 'Audit Failed', sel_b))

                    if is_eco:
                        # 1. Credit Organizer +100 Mudra
                        cursor.execute("SELECT organizer FROM bookings WHERE booking_id = ?", (sel_b,))
                        org_user = cursor.fetchone()[0]
                        cursor.execute("UPDATE users SET wallet = wallet + 100 WHERE username = ?", (org_user,))
                        cursor.execute("INSERT INTO transactions (username, amount, type, reason, timestamp) VALUES (?,?,?,?,?)",
                                       (org_user, 100, "Credit", f"Verified Audit: {sel_b}", now))

                        # 2. Update Organizer Average Score
                        cursor.execute("SELECT AVG(audit_score) FROM bookings WHERE organizer = ?", (org_user,))
                        avg_s = cursor.fetchone()[0]
                        cursor.execute("UPDATE users SET score = ?, audited = 1 WHERE username = ?", (round(avg_s, 1), org_user))

                    db.commit(); st.success(f"Audit Complete! Score: {score}"); st.rerun()
                except Exception as e: st.error(f"AI Failure: {e}")