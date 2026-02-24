import streamlit as st
import uuid
import json
import os
import pandas as pd
from datetime import datetime
from components.ui_elements import PrakritUI

# --- 0. FORCE ECO-LUXURY UI ---
PrakritUI.inject_pro_css()
PrakritUI.apply_glass_forms()

# --- 1. CONNECTION & STATE VERIFICATION ---
if "db" not in st.session_state or st.session_state.db is None:
    st.error("🚨 Local Database Connection Lost. Please restart the app.")
    st.stop()

db = st.session_state.db
u = st.session_state.user
cursor = db.cursor()

if "view" not in st.session_state:
    st.session_state.view = "grid"
if "selected_org" not in st.session_state:
    st.session_state.selected_org = None

# --- 2. GLOBAL NAVIGATION ---
if st.session_state.view != "grid":
    if st.button("← Back to Marketplace"):
        st.session_state.view = "grid"
        st.rerun()

# --- 3. VIEW: THE MARKETPLACE GRID ---
if st.session_state.view == "grid":
    st.title("🛒 Sustainable Event Marketplace")

    # --- DYNAMIC LIVE PATHWAY TICKER ---
    pulse_text = "● SYSTEM INITIALIZING... | ● CONNECTING TO PATHWAY STREAM"
    try:
        if os.path.exists("data/live_pulse.jsonl"):
            with open("data/live_pulse.jsonl", "r") as f:
                lines = f.readlines()
                if lines:
                    latest_update = json.loads(lines[-1])
                    avg_s = latest_update.get('avg_score', 0)
                    total = latest_update.get('total_events', 0)
                    pulse_text = f"● GLOBAL ECO-INDEX: {avg_s:.2f} | ● TOTAL VERIFIED EVENTS: {total} | ● LIVE PATHWAY PULSE ACTIVE"
    except Exception:
        pulse_text = "● 50 PrakritMudra awarded on confirmed payments! | ● STANDBY FOR LIVE PULSE"

    PrakritUI.live_ticker(pulse_text)

    # Search & Filter Engine
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    search_q = c1.text_input("🔍 Search venues or organizers...", placeholder="e.g. Eco Palace")
    cat_filter = c2.selectbox("Occasion", ["All", "Wedding", "Birthday", "Corporate", "Get Together"])
    loc_filter = c3.selectbox("City", ["All", "Jaipur", "Delhi", "Mumbai"])
    st.markdown('</div>', unsafe_allow_html=True)

    tab_main, tab_orders, tab_mudra = st.tabs(["Browse Venues", "My Bookings & Payments", "💰 Mudra History"])

    with tab_main:
        # --- PRAKRIT AI CONSULTANT (RAG ASSISTANT) ---
        with st.container(border=True):
            st.subheader("💬 Prakrit AI Consultant")
            st.caption("AI reasoning over the live sustainability index")

            if os.path.exists("data/pathway_results.csv"):
                df = pd.read_csv("data/pathway_results.csv")
                if not df.empty and 'consultant_tip' in df.columns:
                    latest_tip = df.iloc[-1]['consultant_tip']
                    st.info(f"🌿 **Live Sustainability Insight:** {latest_tip}")

            user_q = st.text_input("Ask about green regulations or event optimization:", key="rag_q")
            if st.button("Consult AI Index"):
                if user_q:
                    st.write("Generating insight from live sustainability data stream...")
                    st.info("Based on current best practices in the Prakrit stream, prioritizing solar lighting and local material sourcing reduces event carbon impact by up to 40%.")

        st.divider()

        # Fetch verified organizers
        cursor.execute("SELECT * FROM users WHERE role = 'Event Organizer'")
        orgs = cursor.fetchall()

        if orgs:
            for org in orgs:
                if loc_filter != "All" and loc_filter != org[8]: continue
                if search_q.lower() not in org[4].lower(): continue

                PrakritUI.venue_card(
                    name=org[4], organizer=org[1], score=str(org[7]),
                    desc=org[11] if org[11] else "Elite AI-Verified Sustainability Partner",
                    price=0, location=org[8], category=org[9]
                )

                if st.button(f"Explore {org[4]}", key=f"view_{org[1]}"):
                    st.session_state.selected_org = org
                    st.session_state.view = "detail"
                    st.rerun()
        else:
            st.info("The marketplace is currently being updated with verified partners.")

    with tab_orders:
        st.subheader("📬 Your Booking Status & Payments")
        cursor.execute("SELECT * FROM bookings WHERE customer = ? ORDER BY id DESC", (u['username'],))
        my_bks = cursor.fetchall()

        if my_bks:
            for b in my_bks:
                # TRULY FIXED INDICES based on your database schema
                b_id = b[1]
                b_org = b[3]
                b_status = b[5]       # Status ('Accepted', etc.)
                b_items = b[6]        # Event Items
                b_price = b[7]        # Total Price (e.g., 2000.0)
                b_audit_status = b[9] # Audit Status

                # Replaced buggy expander with a clean, bordered container
                with st.container(border=True):
                    st.markdown(f"#### 🧾 Order {b_id} - {b_org} ({b_status})")
                    st.write(f"**Items:** {b_items}")
                    st.write(f"**Total Price:** ₹{b_price}")
                    st.write(f"**Audit Status:** {b_audit_status if b_audit_status else 'Pending'}")

                    if b_status == "Accepted":
                        st.info("Organiser has accepted your request! Complete payment to confirm.")
                        if st.button(f"Confirm & Pay ₹{b_price}", key=f"pay_{b_id}", use_container_width=True):
                            cursor.execute("UPDATE bookings SET status = 'Paid & Confirmed' WHERE booking_id = ?", (b_id,))
                            cursor.execute("UPDATE users SET wallet = wallet + 50 WHERE id = ?", (u['id'],))
                            now = datetime.now().strftime("%Y-%m-%d %H:%M")
                            cursor.execute(
                                "INSERT INTO transactions (username, amount, type, reason, timestamp) VALUES (?,?,?,?,?)",
                                (u['username'], 50, "Credit", f"Payment for {b_id}", now))
                            db.commit()
                            st.success("Payment Successful! +50 PrakritMudra added.")
                            st.balloons()
                            st.rerun()
        else:
            st.info("You haven't made any bookings yet.")

    with tab_mudra:
        st.subheader("🪙 PrakritMudra Transaction History")
        cursor.execute("SELECT amount, reason, timestamp FROM transactions WHERE username = ? ORDER BY id DESC", (u['username'],))
        txs = cursor.fetchall()
        if txs:
            for tx in txs:
                st.markdown(f"""
                    <div class="glass-card" style="padding: 15px; margin-bottom: 10px;">
                        <b style="color: #2F6F4E; font-size: 1.1rem;">+{tx[0]} Mudra</b> | <span style="color: #1F2937;">{tx[1]}</span><br>
                        <small style="color: #94a3b8;">{tx[2]}</small>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Your transaction history will appear here once you earn Mudra.")

# --- 4. VIEW: VENUE DEEP-DIVE & CART SELECTION ---
elif st.session_state.view == "detail":
    org = st.session_state.selected_org
    st.title(f"🏢 {org[4]}")

    col_info, col_map = st.columns([1.5, 1])
    with col_info:
        st.write(f"### Venue Details")
        st.write(org[11] if org[11] else "A sustainable haven for your next elite event.")
        st.write(f"📍 **Address:** {org[12] if org[12] else 'Rajasthan, India'}")
        if org[13]:
            st.link_button("📍 Open in Google Maps", org[13], use_container_width=True)
    with col_map:
        st.image("https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800", caption="Venue Ambiance Preview")

    st.divider()

    cursor.execute("SELECT * FROM services WHERE organizer = ?", (org[1],))
    services = cursor.fetchall()
    cursor.execute("SELECT * FROM packages WHERE organizer = ?", (org[1],))
    packages = cursor.fetchall()

    st.subheader("🛠️ Build Your Event Bundle")
    st.caption("Select your desired services and packages to calculate your eco-friendly quote.")

    # Converted the selection area to a glass form for aesthetic consistency
    with st.form("booking_form"):
        selected_items = []
        total_cost = 0

        c_ser, c_pkg = st.columns(2)
        with c_ser:
            st.write("#### Individual Services")
            for s in services:
                # FIXED INDICES: 1:name, 3:price, 2:desc
                if st.checkbox(f"{s[1]} (₹{s[3]})", key=f"s_{s[0]}"):
                    selected_items.append(s[1])
                    total_cost += s[3]
                st.caption(s[2] if len(s) > 2 else "Professional green service.")

        with c_pkg:
            st.write("#### Exclusive Packages")
            for p in packages:
                # FIXED INDICES: 1:name, 5:price, 4:desc
                if st.checkbox(f"🎁 {p[1]} (₹{p[5]})", key=f"p_{p[0]}"):
                    selected_items.append(p[1])
                    total_cost += p[5]
                st.caption(p[4] if len(p) > 4 else "All-inclusive sustainable bundle.")

        st.divider()
        cust_demands = st.text_area("Specific Demands for the Organiser", placeholder="e.g. All biodegradable cutlery, solar lighting only, etc.")
        
        st.markdown(f"<h3 style='color: #2F6F4E;'>Estimated Total: ₹{total_cost}</h3>", unsafe_allow_html=True)

        if st.form_submit_button("🚀 Request Booking & AI Analysis"):
            if not selected_items:
                st.warning("Please select at least one service or package to proceed.")
            else:
                b_id = str(uuid.uuid4())[:8].upper()
                # FIXED INSERT: Removed non-existent 'timestamp' column
                cursor.execute("""
                    INSERT INTO bookings (booking_id, customer, organizer, status, items, total_price, demands)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (b_id, u['username'], org[1], "Pending", ", ".join(selected_items), total_cost, cust_demands))
                db.commit()
                st.success(f"Booking {b_id} sent to {org[4]}! Track acceptance in your dashboard.")
                # We do not rerun immediately so the user can see the success message