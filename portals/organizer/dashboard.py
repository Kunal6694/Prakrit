import streamlit as st
from components.ui_elements import PrakritUI

# Refresh user data from the database to show updated wallet/score
cursor = db.cursor()
cursor.execute("SELECT wallet, audited, score FROM users WHERE id = ?", (u['id'],))
fresh_u = cursor.fetchone()

st.title(f"👨‍💼 {u['company']} | Command Center")

# Dynamic Metrics pulled from SQLite indices
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.metric("Wallet Balance", f"🪙 {fresh_u[0]}")
col2.metric("Sustainability Status", "Audited ✅" if fresh_u[1] else "Pending")
col3.metric("AI Score", f"{fresh_u[2]}/10")
st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["⚡ Operations", "📜 Green Certification", "🎨 Branding"])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Incoming Booking Requests")

    # Fetch bookings from SQLite for this specific organizer
    cursor.execute("SELECT * FROM bookings WHERE organizer = ?", (u['username'],))
    my_bookings = cursor.fetchall()

    if my_bookings:
        for b in my_bookings:
            # b[2] = customer name, b[4] = timestamp
            st.write(f"✅ **{b[2]}** confirmed a booking on {b[4]}")
            st.caption(f"Booking ID: {b[1]}")
    else:
        st.info("Awaiting new requests from the marketplace.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    if fresh_u[1]:  # Check audited status
        PrakritUI.green_certificate_ui(u['company'], fresh_u[2])
        st.button("Download PDF Certificate", use_container_width=True)
    else:
        st.warning("Complete your first Sustainability Proof upload in the 'Branding' tab to trigger an audit.")

with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Visual Identity")
    st.file_uploader("Upload Venue Images", accept_multiple_files=True)
    st.text_input("Google Maps Location URL", value="https://maps.google.com/...")
    st.button("Update Presence")
    st.markdown('</div>', unsafe_allow_html=True)