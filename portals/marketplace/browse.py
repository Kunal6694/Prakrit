import streamlit as st
import uuid
from datetime import datetime
from components.ui_elements import PrakritUI

# --- 1. CONNECTION VERIFICATION ---
if "db" not in globals() or db is None:
    st.error("🚨 Local Database Connection Lost. Please restart the app.")
    st.stop()

cursor = db.cursor()

# --- 2. UI & MARKETPLACE ENGINE ---
st.title("🛒 Sustainable Event Marketplace")
PrakritUI.live_ticker("● 50 PrakritMudra awarded on all Wedding bookings! | ● LIVE: 'The Grand Green' verified at 9.9")

# Search & Filters
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([2, 1, 1])
search_q = c1.text_input("🔍 Search venues or organizers...", placeholder="e.g. Eco Palace")
cat_filter = c2.selectbox("Occasion", ["All", "Wedding", "Birthday", "Office Party", "Get Together"])
loc_filter = c3.selectbox("City", ["All", "Jaipur", "Delhi", "Mumbai"])
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. DYNAMIC SQL QUERY ---
# SQLite Table indices: 0:id, 1:username, 4:company, 5:wallet, 6:audited, 7:score, 8:location, 9:category
sql = "SELECT * FROM users WHERE role = 'Event Organizer'"
params = []

if loc_filter != "All":
    sql += " AND location = ?"
    params.append(loc_filter)
if cat_filter != "All":
    sql += " AND category = ?"
    params.append(cat_filter)

cursor.execute(sql, params)
organizers = cursor.fetchall()

if organizers:
    for i, org in enumerate(organizers):
        # Apply search text filter
        if search_q.lower() not in org[4].lower(): continue

        PrakritUI.venue_card(
            name=org[4] if org[4] else "Elite Venue",
            organizer=org[1],
            score=str(org[7]) if org[7] else "8.5",
            desc="AI-Verified Sustainability Partner",
            price=45000,
            location=org[8],
            category=org[9]
        )

        if st.button(f"⚡ Secure Booking for {org[4]}", key=f"bk_{org[0]}"):
            booking_id = str(uuid.uuid4())[:8].upper()
            now = datetime.now().strftime("%Y-%m-%d %H:%M")

            # 1. Save booking to SQLite
            cursor.execute('''INSERT INTO bookings (booking_id, customer, organizer, timestamp, status) 
                            VALUES (?, ?, ?, ?, ?)''',
                            (booking_id, u['username'], org[1], now, "Confirmed"))

            # 2. Update Local User Wallet (+50 PrakritMudra)
            cursor.execute("UPDATE users SET wallet = wallet + 50 WHERE id = ?", (u['id'],))
            db.commit() # Save changes to the .db file

            st.balloons()
            st.success(f"Booking {booking_id} Confirmed! Details shared with {org[4]}.")
            st.toast("Elite Booking Confirmed! +50 PrakritMudra added.", icon="🪙")
else:
    st.info("The marketplace is currently being updated with verified partners.")