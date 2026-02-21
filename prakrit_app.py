import streamlit as st
import sqlite3
import os
import json
import pandas as pd
from components.ui_elements import PrakritUI

# --------------------------------------------------
# 1. GLOBAL INITIALIZATION
# --------------------------------------------------
st.set_page_config(
    page_title="Prakrit | AI Sustainability Ecosystem",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PrakritUI.inject_pro_css()

# --------------------------------------------------
# 2. SESSION STATE INITIALIZATION (Prevents AttributeErrors)
# --------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "registered_id" not in st.session_state:
    st.session_state.registered_id = None
if "show_registration" not in st.session_state:
    st.session_state.show_registration = False
if "temp_role" not in st.session_state:
    st.session_state.temp_role = "Customer"


# --------------------------------------------------
# 3. DATABASE INITIALIZATION (Elite Schema)
# --------------------------------------------------
@st.cache_resource
def init_sqlite():
    conn = sqlite3.connect("prakrit_system.db", check_same_thread=False)
    cursor = conn.cursor()

    # 1. Users Table (Enhanced with Prakrit ID and Branding)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       username
                       TEXT
                       UNIQUE,
                       password
                       TEXT,
                       role
                       TEXT,
                       company
                       TEXT,
                       wallet
                       INTEGER,
                       audited
                       BOOLEAN,
                       score
                       REAL,
                       location
                       TEXT,
                       category
                       TEXT,
                       phone
                       TEXT,
                       about
                       TEXT,
                       address
                       TEXT,
                       map_link
                       TEXT,
                       prakrit_id
                       TEXT
                       UNIQUE
                   )
                   """)

    # 2. Services & Packages
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS services
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       organizer
                       TEXT,
                       name
                       TEXT,
                       desc
                       TEXT,
                       price
                       REAL,
                       image
                       TEXT
                   )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS packages
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       organizer
                       TEXT,
                       name
                       TEXT,
                       desc
                       TEXT,
                       price
                       REAL,
                       image
                       TEXT
                   )
                   """)

    # 3. Bookings (Enhanced for Pathway Audit Tracking)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS bookings
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       booking_id
                       TEXT
                       UNIQUE,
                       customer
                       TEXT,
                       organizer
                       TEXT,
                       timestamp
                       TEXT,
                       status
                       TEXT,
                       items
                       TEXT,
                       total_price
                       REAL,
                       demands
                       TEXT,
                       rating
                       INTEGER,
                       feedback
                       TEXT,
                       audit_score
                       REAL,
                       audit_status
                       TEXT,
                       auditor_name
                       TEXT
                   )
                   """)

    # 4. Transactions (Mudra History)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS transactions
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       username
                       TEXT,
                       amount
                       INTEGER,
                       type
                       TEXT,
                       reason
                       TEXT,
                       timestamp
                       TEXT
                   )
                   """)

    # --- AUTOMATIC MIGRATIONS ---
    for col in [("about", "TEXT"), ("address", "TEXT"), ("map_link", "TEXT"), ("prakrit_id", "TEXT")]:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col[0]} {col[1]}")
        except sqlite3.OperationalError:
            pass

    for col in [("items", "TEXT"), ("total_price", "REAL"), ("demands", "TEXT"), ("rating", "INTEGER"),
                ("feedback", "TEXT"), ("audit_score", "REAL"), ("audit_status", "TEXT"), ("auditor_name", "TEXT")]:
        try:
            cursor.execute(f"ALTER TABLE bookings ADD COLUMN {col[0]} {col[1]}")
        except sqlite3.OperationalError:
            pass

    conn.commit()
    return conn


db_conn = init_sqlite()
st.session_state.db = db_conn


# --------------------------------------------------
# 4. AUTHENTICATION HELPERS
# --------------------------------------------------
def login_success(row):
    st.session_state.user = {
        "id": row[0], "username": row[1], "role": row[3], "company": row[4],
        "wallet": row[5], "audited": row[6], "score": row[7], "location": row[8],
        "category": row[9], "phone": row[10], "about": row[11], "address": row[12],
        "map_link": row[13], "prakrit_id": row[14]
    }
    st.query_params["token"] = str(row[0])
    st.rerun()


def logout():
    st.query_params.clear()
    st.session_state.user = None
    st.rerun()


token = st.query_params.get("token")
if token and st.session_state.user is None:
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (token,))
    user_row = cursor.fetchone()
    if user_row:
        login_success(user_row)

# --------------------------------------------------
# 5. AUTHENTICATION UI
# --------------------------------------------------
if st.session_state.user is None:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.title("🌿 Prakrit")
        st.subheader("Deciphering Nature with AI-Verified Integrity")
    with col2:
        if st.session_state.registered_id:
            st.success("✅ Account Created Successfully!")
            pid = st.session_state.registered_id
            st.markdown(f"""
                <div style="border:2px solid #10b981;padding:20px;border-radius:15px;text-align:center;">
                    <p style="color:#94a3b8; font-size:0.8rem;">OFFICIAL PRAKRIT ID</p>
                    <h2 style="font-family:monospace; letter-spacing:5px; color:#10b981;">{pid}</h2>
                </div>
            """, unsafe_allow_html=True)
            if st.button("PROCEED TO LOGIN", use_container_width=True):
                st.session_state.registered_id = None
                st.session_state.show_registration = False
                st.rerun()
            st.stop()

        if not st.session_state.get("show_registration"):
            tabs = st.tabs(["Login to Dashboard", "Join the Ecosystem"])
            with tabs[0]:
                u_in = st.text_input("Username or Prakrit ID", key="login_username")
                p_in = st.text_input("Password", type="password", key="login_password")
                if st.button("Uplink to Dashboard", use_container_width=True):
                    cursor = db_conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE (username = ? OR prakrit_id = ?) AND password = ?",
                                   (u_in, u_in, p_in))
                    row = cursor.fetchone()
                    if row:
                        login_success(row)
                    else:
                        st.error("Access Denied: Invalid Credentials")
            with tabs[1]:
                st.markdown("## 🌿 Join the Ecosystem as")
                role_select = st.selectbox("Select your role:", ["Customer", "NGO Auditor", "Event Organizer"])
                if st.button("PROCEED TO REGISTRATION", use_container_width=True):
                    st.session_state.temp_role = role_select
                    st.session_state.show_registration = True
                    st.rerun()
        else:
            role = st.session_state.get("temp_role", "Customer")
            st.markdown(f"### 📝 Register as {role}")
            with st.form("detailed_reg"):
                new_u = st.text_input("Choose Username*")
                new_p = st.text_input("Set Password*", type="password")
                comp_val = st.text_input("Full Name / Organization Name*")
                phone_val = st.text_input("Contact Number")
                if st.form_submit_button("Complete Registration"):
                    if not new_u or not new_p or not comp_val:
                        st.error("Please fill mandatory fields.")
                    else:
                        try:
                            cursor = db_conn.cursor()
                            cursor.execute("SELECT COUNT(*) FROM users")
                            count = cursor.fetchone()[0]
                            gen_id = f"PRK-{1001 + count}"
                            cursor.execute("""
                                           INSERT INTO users (username, password, role, company, phone, location,
                                                              prakrit_id, wallet, score, audited)
                                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                           """,
                                           (new_u, new_p, role, comp_val, phone_val, "India", gen_id, 0, 0.0, False))
                            db_conn.commit()
                            st.session_state.registered_id = gen_id
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("Username already exists.")
            if st.button("← Back"):
                st.session_state.show_registration = False
                st.rerun()
    st.stop()

# --------------------------------------------------
# 6. LOGGED IN SECTION
# --------------------------------------------------
u = st.session_state.user

# --- LIVE PATHWAY TICKER (Real-time Pulse) ---
pulse_text = "● SYSTEM INITIALIZING... | ● CONNECTING TO PATHWAY STREAM"
try:
    if os.path.exists("data/live_pulse.jsonl"):
        with open("data/live_pulse.jsonl", "r") as f:
            lines = f.readlines()
            if lines:
                latest_update = json.loads(lines[-1])
                avg_s = latest_update.get('avg_score', 0)
                total = latest_update.get('total_events', 0)
                pulse_text = f"● GLOBAL ECO-INDEX: {avg_s:.2f} | ● TOTAL VERIFIED EVENTS: {total} | ● LIVE PULSE ACTIVE"
except Exception:
    pass
PrakritUI.live_ticker(pulse_text)

# --- PRAKRIT AI CONSULTANT (RAG Assistant) ---
with st.sidebar:
    st.divider()
    st.subheader("💬 AI Consultant")
    st.caption("Real-time RAG Insight")
    if os.path.exists("data/pathway_results.csv"):
        df = pd.read_csv("data/pathway_results.csv")
        if not df.empty:
            latest_tip = df.iloc[-1]['consultant_tip']
            st.info(f"🌿 **Tip:** {latest_tip}")

    if st.button("Secure Logout 🚪", use_container_width=True):
        logout()

# --------------------------------------------------
# 7. AUTO-ROUTING ENGINE
# --------------------------------------------------
role_map = {
    "NGO Auditor": "portals/auditor/verify.py",
    "Event Organizer": "portals/organizer/dashboard.py",
    "Customer": "portals/marketplace/browse.py"
}

path = role_map.get(u["role"])
if path and os.path.exists(path):
    with open(path, "r") as f:
        exec(f.read(), globals(), {"db": db_conn, "u": u})
else:
    st.info("Authorized access established. Dashboard loading...")