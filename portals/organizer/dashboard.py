import streamlit as st
from datetime import datetime
from components.ui_elements import PrakritUI

# --- 1. DATA FETCHING ---
cursor = db.cursor()
# Indices: 0:company, 1:about, 2:address, 3:map_link, 4:score, 5:wallet, 6:audited
cursor.execute("SELECT company, about, address, map_link, score, wallet, audited FROM users WHERE id = ?", (u['id'],))
comp_data = cursor.fetchone()

st.title(f"🏢 {comp_data[0]}")
st.caption("Event Organiser Dashboard")

# --- 2. METRICS DISPLAY ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("Wallet", f"🪙 {comp_data[5]}")
c2.metric("Eco Score", f"{comp_data[4]}/10")
c3.metric("Audit", "Verified ✅" if comp_data[6] else "Pending")
st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Operations", "Branding & Reviews", "Services & Packages", "Audit Badge", "Prakrit Mudra"])

# --- TAB 1: OPERATIONS ---
with tab1:
    sub1, sub2 = st.tabs(["Pending Orders", "Order History"])
    with sub1:
        st.subheader("📬 Pending Requests")
        cursor.execute("SELECT * FROM bookings WHERE organizer = ? AND status = 'Pending'", (u['username'],))
        pending = cursor.fetchall()
        for p in pending:
            with st.expander(f"Order {p[1]} from {p[2]}"):
                st.write(f"**Items:** {p[6]}")
                st.write(f"**Customer Demands:** {p[8]}")
                st.write(f"**Total Revenue:** ₹{p[7]}")
                col_a, col_d = st.columns(2)
                if col_a.button(f"Accept {p[1]}", key=f"acc_{p[1]}"):
                    cursor.execute("UPDATE bookings SET status = 'Accepted' WHERE booking_id = ?", (p[1],))
                    db.commit(); st.rerun()
                if col_d.button(f"Decline {p[1]}", key=f"dec_{p[1]}"):
                    cursor.execute("UPDATE bookings SET status = 'Declined' WHERE booking_id = ?", (p[1],))
                    db.commit(); st.rerun()

    with sub2:
        st.subheader("📚 Completed Events")
        cursor.execute("SELECT * FROM bookings WHERE organizer = ? AND status = 'Paid & Confirmed'", (u['username'],))
        history = cursor.fetchall()
        for h in history: st.write(f"✅ **{h[2]}** | {h[4]} | ₹{h[7]} | {h[6]}")

# --- TAB 2: BRANDING ---
with tab2:
    with st.form("branding"):
        st.subheader("🖼️ Branding Details")
        new_about = st.text_area("About Company", value=comp_data[1] if comp_data[1] else "")
        new_addr = st.text_input("Venue Address", value=comp_data[2] if comp_data[2] else "")
        new_map = st.text_input("Google Maps URL", value=comp_data[3] if comp_data[3] else "")
        st.file_uploader("Upload Venue/Decoration Gallery", accept_multiple_files=True)
        if st.form_submit_button("Save Branding"):
            cursor.execute("UPDATE users SET about=?, address=?, map_link=? WHERE id=?", (new_about, new_addr, new_map, u['id']))
            db.commit(); st.success("Updated!"); st.rerun()

# --- TAB 3: INVENTORY ---
with tab3:
    col_s, col_p = st.columns(2)
    with col_s:
        st.write("### Individual Services")
        with st.expander("Add Service"):
            s_n = st.text_input("Service Name")
            s_d = st.text_area("Description")
            s_p = st.number_input("Price (₹)", min_value=0)
            if st.button("Add"):
                cursor.execute("INSERT INTO services (organizer, name, desc, price) VALUES (?,?,?,?)", (u['username'], s_n, s_d, s_p))
                db.commit(); st.rerun()
    with col_p:
        st.write("### Multi-Service Packages")
        with st.expander("Create Package"):
            p_n = st.text_input("Package Name")
            p_d = st.text_area("What's Included?")
            p_p = st.number_input("Package Price (₹)", min_value=0)
            if st.button("Create"):
                cursor.execute("INSERT INTO packages (organizer, name, desc, price) VALUES (?,?,?,?)", (u['username'], p_n, p_d, p_p))
                db.commit(); st.rerun()

# --- TAB 4: AUDIT BADGE ---
with tab4:
    if comp_data[6]: # audited status
        PrakritUI.green_certificate_ui(comp_data[0], comp_data[4])
    else: st.warning("Audit Pending.")

# --- TAB 5: MUDRA PAYOUTS ---
with tab5:
    st.subheader("🪙 Mudra Wallet & Payouts")
    # Using comp_data[5] for wallet balance
    st.metric("Total Balance", f"🪙 {comp_data[5]} Mudra")

    with st.expander("Cash Out to Bank / UPI"):
        amount_to_cash = st.number_input("Amount to Cash Out", min_value=0, max_value=int(comp_data[5]))
        payout_method = st.selectbox("Payout Method", ["UPI", "Bank Transfer"])
        payout_id = st.text_input("Enter UPI ID or Account Number")

        if st.button("Submit Payout Request"):
            if comp_data[5] >= amount_to_cash and amount_to_cash > 0:
                # 1. Update Wallet
                cursor.execute("UPDATE users SET wallet = wallet - ? WHERE id = ?", (amount_to_cash, u['id']))
                # 2. Log Transaction
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                cursor.execute(
                    "INSERT INTO transactions (username, amount, type, reason, timestamp) VALUES (?,?,?,?,?)",
                    (u['username'], amount_to_cash, "Debit", f"Cash Out via {payout_method}", now))
                db.commit()
                st.success(f"Payout of ₹{amount_to_cash} (from Mudra) initiated to {payout_id}!")
                st.rerun()
            elif amount_to_cash <= 0:
                st.warning("Enter a valid amount to cash out.")
            else:
                st.error("Insufficient Mudra balance.")