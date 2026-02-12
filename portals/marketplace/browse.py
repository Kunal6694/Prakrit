import streamlit as st
import uuid
from datetime import datetime
from components.ui_elements import PrakritUI

# --- 1. CONNECTION & STATE VERIFICATION ---
# We use session_state to ensure the database connection persists through view changes
if "db" not in st.session_state or st.session_state.db is None:
    st.error("🚨 Local Database Connection Lost. Please restart the app.")
    st.stop()

db = st.session_state.db
u = st.session_state.user
cursor = db.cursor()

# Control the toggle between the marketplace grid and the venue detail view
if "view" not in st.session_state: st.session_state.view = "grid"
if "selected_org" not in st.session_state: st.session_state.selected_org = None

# --- 2. GLOBAL NAVIGATION ---
if st.session_state.view != "grid":
    if st.button("← Back to Marketplace"):
        st.session_state.view = "grid"
        st.rerun()

# --- 3. VIEW: THE MARKETPLACE GRID ---
if st.session_state.view == "grid":
    st.title("🛒 Sustainable Event Marketplace")
    PrakritUI.live_ticker(
        "● 50 PrakritMudra awarded on all confirmed payments! | ● LIVE: New eco-packages added by verified partners.")

    # Search & Filter Engine
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    search_q = c1.text_input("🔍 Search venues or organizers...", placeholder="e.g. Eco Palace")
    cat_filter = c2.selectbox("Occasion", ["All", "Wedding", "Birthday", "Corporate", "Get Together"])
    loc_filter = c3.selectbox("City", ["All", "Jaipur", "Delhi", "Mumbai"])
    st.markdown('</div>', unsafe_allow_html=True)

    tab_main, tab_orders, tab_mudra = st.tabs(["Browse Venues", "My Bookings & Payments", "💰 Mudra History"])

    with tab_main:
        # Fetch verified organizers from the database
        cursor.execute("SELECT * FROM users WHERE role = 'Event Organizer'")
        orgs = cursor.fetchall()

        if orgs:
            for org in orgs:
                # Filter Logic
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
        # Fetch only the bookings belonging to the logged-in customer
        cursor.execute("SELECT * FROM bookings WHERE customer = ? ORDER BY id DESC", (u['username'],))
        my_bks = cursor.fetchall()

        if my_bks:
            for b in my_bks:
                with st.expander(f"Order {b[1]} - {b[3]} ({b[5]})"):
                    st.write(f"**Items:** {b[6]}")
                    st.write(f"**Total Price:** ₹{b[7]}")
                    st.write(f"**Audit Status:** {b[12] if b[12] else 'Pending'}")

                    # Payment Logic: Mudra is only awarded after payment is completed
                    if b[5] == "Accepted":
                        st.info("Organiser has accepted your request! Complete payment to confirm.")
                        if st.button(f"Confirm & Pay ₹{b[7]}", key=f"pay_{b[1]}"):
                            # 1. Update Booking Status
                            cursor.execute("UPDATE bookings SET status = 'Paid & Confirmed' WHERE booking_id = ?",
                                           (b[1],))
                            # 2. Award Mudra to Customer (+50)
                            cursor.execute("UPDATE users SET wallet = wallet + 50 WHERE id = ?", (u['id'],))
                            # 3. Log the Transaction
                            now = datetime.now().strftime("%Y-%m-%d %H:%M")
                            cursor.execute(
                                "INSERT INTO transactions (username, amount, type, reason, timestamp) VALUES (?,?,?,?,?)",
                                (u['username'], 50, "Credit", f"Payment for {b[1]}", now))
                            db.commit()
                            st.success("Payment Successful! +50 PrakritMudra added.")
                            st.balloons()
                            st.rerun()
        else:
            st.info("No active bookings. Start exploring to place your first request.")

    with tab_mudra:
        st.subheader("🪙 PrakritMudra Transaction History")
        cursor.execute("SELECT amount, reason, timestamp FROM transactions WHERE username = ? ORDER BY id DESC",
                       (u['username'],))
        txs = cursor.fetchall()
        if txs:
            for tx in txs:
                st.markdown(f"""
                    <div class="glass-card">
                        <b>+{tx[0]} Mudra</b> | {tx[1]}<br>
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
        st.image("https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800",
                 caption="Venue Ambiance Preview")

    st.divider()

    # Selection logic for custom bundles
    cursor.execute("SELECT * FROM services WHERE organizer = ?", (org[1],))
    services = cursor.fetchall()
    cursor.execute("SELECT * FROM packages WHERE organizer = ?", (org[1],))
    packages = cursor.fetchall()

    st.subheader("🛠️ Build Your Event Bundle")
    st.caption("Select your desired services and packages to calculate your eco-friendly quote.")

    selected_items = []
    total_cost = 0

    c_ser, c_pkg = st.columns(2)
    with c_ser:
        st.write("#### Individual Services")
        for s in services:
            # Checkbox logic for price calculation
            if st.checkbox(f"{s[2]} (₹{s[4]})", key=f"s_{s[0]}"):
                selected_items.append(s[2])
                total_cost += s[4]
            st.caption(s[3] if len(s) > 3 else "Professional green service.")

    with c_pkg:
        st.write("#### Exclusive Packages")
        for p in packages:
            if st.checkbox(f"🎁 {p[2]} (₹{p[4]})", key=f"p_{p[0]}"):
                selected_items.append(p[2])
                total_cost += p[4]
            st.caption(p[3] if len(p) > 3 else "All-inclusive sustainable bundle.")

    st.divider()
    cust_demands = st.text_area("Specific Demands for the Organiser",
                                placeholder="e.g. All biodegradable cutlery, solar lighting only, etc.")

    st.metric("Estimated Event Total", f"₹{total_cost}")

    if st.button("🚀 Request Booking & AI Analysis", use_container_width=True):
        if not selected_items:
            st.warning("Please select at least one service or package to proceed.")
        else:
            b_id = str(uuid.uuid4())[:8].upper()
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            # Save the full booking request to the database
            cursor.execute("""
                           INSERT INTO bookings (booking_id, customer, organizer, timestamp, status, items, total_price,
                                                 demands)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                           (b_id, u['username'], org[1], now, "Pending", ", ".join(selected_items), total_cost,
                            cust_demands))
            db.commit()
            st.success(f"Booking {b_id} sent to {org[4]}! Track acceptance in your dashboard.")
            st.session_state.view = "grid"
            st.rerun()