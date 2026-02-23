import streamlit as st
from datetime import datetime
from components.ui_elements import PrakritUI

# --- 0. FORCE ECO-LUXURY UI ---
PrakritUI.inject_pro_css()
PrakritUI.apply_glass_forms()

# --- 1. DATA FETCHING ---
cursor = db.cursor()
# Indices: 0:company, 1:about, 2:address, 3:map_link, 4:score, 5:wallet, 6:audited
cursor.execute("SELECT company, about, address, map_link, score, wallet, audited FROM users WHERE id = ?", (u['id'],))
comp_data = cursor.fetchone()

st.title(f"🏢 {comp_data[0]}")
st.caption("Event Organiser Dashboard")

# --- 2. METRICS DISPLAY (Custom Eco-Luxury Glass Cards) ---
audit_status = "Verified ✅" if comp_data[6] else "Pending"

st.markdown(f"""
<div class="glass-card" style="display: flex; flex-wrap: wrap; justify-content: space-between; padding: 25px 40px; margin-top: 10px; margin-bottom: 20px;">
    <div style="min-width: 150px;">
        <div style="color: #4B5563; font-size: 1rem; font-weight: 600; margin-bottom: 5px;">Wallet</div>
        <div style="color: #1F2937; font-size: 2.2rem; font-weight: 700; font-family: 'Alegreya', serif;">🪙 {comp_data[5]}</div>
    </div>
    <div style="min-width: 150px;">
        <div style="color: #4B5563; font-size: 1rem; font-weight: 600; margin-bottom: 5px;">Eco Score</div>
        <div style="color: #1F2937; font-size: 2.2rem; font-weight: 700; font-family: 'Alegreya', serif;">{comp_data[4]}<span style="font-size: 1.2rem; color: #8BAE66;"> /10</span></div>
    </div>
    <div style="min-width: 150px;">
        <div style="color: #4B5563; font-size: 1rem; font-weight: 600; margin-bottom: 5px;">Audit</div>
        <div style="color: #1F2937; font-size: 2.2rem; font-weight: 700; font-family: 'Alegreya', serif;">{audit_status}</div>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Operations", "Branding & Reviews", "Services & Packages", "Audit Badge", "Prakrit Mudra"])

# --- TAB 1: OPERATIONS ---
with tab1:
    sub1, sub2 = st.tabs(["Pending Orders", "Order History"])
    with sub1:
        st.subheader("📬 Pending Requests")
        cursor.execute("SELECT * FROM bookings WHERE organizer = ? AND status = 'Pending'", (u['username'],))
        pending = cursor.fetchall()
        if pending:
            for p in pending:
                # Replaced the buggy expander with a clean, bordered container
                with st.container(border=True): 
                    st.markdown(f"#### 📦 Order {p[1]} from {p[2]}")
                    st.write(f"**Items:** {p[6]}")
                    st.write(f"**Customer Demands:** {p[8]}")
                    st.write(f"**Total Revenue:** ₹{p[7]}")
                    
                    st.markdown("---") # Adds a nice divider line above buttons
                    col_a, col_d = st.columns(2)
                    
                    if col_a.button(f"Accept {p[1]}", key=f"acc_{p[1]}", use_container_width=True):
                        cursor.execute("UPDATE bookings SET status = 'Accepted' WHERE booking_id = ?", (p[1],))
                        db.commit()
                        st.rerun()
                        
                    if col_d.button(f"Decline {p[1]}", key=f"dec_{p[1]}", use_container_width=True):
                        cursor.execute("UPDATE bookings SET status = 'Declined' WHERE booking_id = ?", (p[1],))
                        db.commit()
                        st.rerun()
        else:
            st.info("No pending requests right now.")

    with sub2:
        st.subheader("📚 Completed Events")
        
        # Pulls REAL data exactly matching your database structure
        cursor.execute("SELECT * FROM bookings WHERE organizer = ? AND status = 'Paid & Confirmed'", (u['username'],))
        history = cursor.fetchall()
        
        if history:
            for h in history: 
                with st.container(border=True):
                    # h[1] = Booking ID, h[2] = Customer Name, h[5] = Price, h[10] = Items
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"#### ✅ Order {h[1]}")
                        st.write(f"**Customer:** {h[2]}")
                        # Check if items exist before printing to avoid index errors
                        items = h[10] if len(h) > 10 else "Standard Package"
                        st.write(f"**Items Provided:** {items}")
                    with col2:
                        st.markdown(f"<h3 style='color: #2E7D32;'>₹{h[5]}</h3>", unsafe_allow_html=True)
        else:
            st.info("No completed events yet.")
            

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
            db.commit()
            st.success("Updated!")
            st.rerun()

# --- TAB 3: INVENTORY ---
with tab3:
    col_s, col_p = st.columns(2)
    with col_s:
        st.write("### Individual Services")
        # Converted to st.form to apply the glass UI (removes the black box)
        with st.form("add_service_form"):
            st.write("Add New Service")
            s_n = st.text_input("Service Name")
            s_d = st.text_area("Description")
            s_p = st.number_input("Price (₹)", min_value=0)
            if st.form_submit_button("Add Service"):
                # Fixed Kunal's 'desc' column name to 'description' to match the database
                cursor.execute("INSERT INTO services (organizer, name, description, price) VALUES (?,?,?,?)", (u['username'], s_n, s_d, s_p))
                db.commit()
                st.rerun()
    with col_p:
        st.write("### Multi-Service Packages")
        # Converted to st.form to apply the glass UI (removes the black box)
        with st.form("add_package_form"):
            st.write("Create Package")
            p_n = st.text_input("Package Name")
            p_d = st.text_area("What's Included?")
            p_p = st.number_input("Package Price (₹)", min_value=0)
            if st.form_submit_button("Create Package"):
                # Fixed Kunal's 'desc' column name to 'description'
                cursor.execute("INSERT INTO packages (organizer, name, description, price) VALUES (?,?,?,?)", (u['username'], p_n, p_d, p_p))
                db.commit()
                st.rerun()

# --- TAB 4: AUDIT BADGE ---
with tab4:
    if comp_data[6]: # audited status
        PrakritUI.green_certificate_ui(comp_data[0], comp_data[4])
    else: 
        st.warning("Audit Pending.")

# --- TAB 5: MUDRA PAYOUTS ---
with tab5:
    st.subheader("🪙 Mudra Wallet & Payouts")
    st.metric("Total Balance", f"🪙 {comp_data[5]} Mudra")

    # Converted to st.form to apply the glass UI (removes the black box)
    with st.form("payout_form"):
        st.write("Cash Out to Bank / UPI")
        amount_to_cash = st.number_input("Amount to Cash Out", min_value=0, max_value=int(comp_data[5]))
        payout_method = st.selectbox("Payout Method", ["UPI", "Bank Transfer"])
        payout_id = st.text_input("Enter UPI ID or Account Number")

        if st.form_submit_button("Submit Payout Request"):
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