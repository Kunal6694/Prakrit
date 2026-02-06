import streamlit as st
import os
import sqlite3
from components.ui_elements import PrakritUI

# --- 1. GLOBAL INITIALIZATION ---
st.set_page_config(page_title="Prakrit | AI Sustainability Ecosystem", layout="wide", initial_sidebar_state="collapsed")
PrakritUI.inject_pro_css()


# --- 2. SQLITE DATABASE ENGINE (Bypassing MongoDB DNS Issues) ---
def init_sqlite():
    # check_same_thread=False is required for Streamlit's multi-threaded environment
    conn = sqlite3.connect('prakrit_system.db', check_same_thread=False)
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
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
                          TEXT
                      )''')

    # Create Bookings Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings
                      (
                          id
                          INTEGER
                          PRIMARY
                          KEY
                          AUTOINCREMENT,
                          booking_id
                          TEXT,
                          customer
                          TEXT,
                          organizer
                          TEXT,
                          timestamp
                          TEXT,
                          status
                          TEXT
                      )''')
    conn.commit()
    return conn


# Establish the local connection
db_conn = init_sqlite()
st.session_state.db = db_conn

# --- 3. SESSION PERSISTENCE (Fixes Refresh Logout) ---
if "user" not in st.session_state:
    st.session_state.user = None

# Recover session using a URL token (User ID)
token = st.query_params.get("token")
if token and st.session_state.user is None:
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (token,))
    user_row = cursor.fetchone()
    if user_row:
        # Convert row to dictionary for easier access in portals
        st.session_state.user = {
            "id": user_row[0], "username": user_row[1], "role": user_row[3],
            "company": user_row[4], "wallet": user_row[5], "audited": user_row[6],
            "score": user_row[7], "location": user_row[8], "category": user_row[9]
        }


def login_success(user_row):
    """Stores user in session and sets URL token for refresh persistence."""
    st.session_state.user = {
        "id": user_row[0], "username": user_row[1], "role": user_row[3],
        "company": user_row[4], "wallet": user_row[5], "audited": user_row[6],
        "score": user_row[7], "location": user_row[8], "category": user_row[9]
    }
    st.query_params["token"] = str(user_row[0])
    st.rerun()


def logout():
    """Wipes session and URL tokens."""
    st.query_params.clear()
    st.session_state.user = None
    st.rerun()


# --- 4. AUTHENTICATION UI (Buttons and Styling Preserved) ---
if st.session_state.user is None:
    lottie_welcome = PrakritUI.load_lottie("https://lottie.host/8282361a-7e0e-473d-9d41-3b7c8441164a/H9m1m5WjN6.json")
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.title("🌿 Prakrit")
        st.subheader("The AI Sustainability Standard")
        if lottie_welcome:
            from streamlit_lottie import st_lottie

            st_lottie(lottie_welcome, height=350, key="welcome_anim")

    with col2:
        st.write("### Elite Access Portal")
        t1, t2 = st.tabs(["Login to Dashboard", "Join the Ecosystem"])

        with t2:
            n_u = st.text_input("Choose Username", key="reg_u")
            n_p = st.text_input("Create Password", type="password", key="reg_p")
            n_r = st.selectbox("Role", ["Customer", "NGO Auditor", "Event Organizer"])
            n_c = st.text_input("Organization / Venue Name")
            if st.button("Initialize Elite Account"):
                try:
                    cursor = db_conn.cursor()
                    cursor.execute('''INSERT INTO users
                                      (username, password, role, company, wallet, audited, score, location, category,
                                       phone)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                   (n_u, n_p, n_r, n_c, 100, False, 0.0, "Jaipur", "Premium", "9876543210"))
                    db_conn.commit()
                    st.success("Registration Successful! Please Sign In below.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Choose another one.")

        with t1:
            u_in = st.text_input("Username", key="log_u")
            p_in = st.text_input("Password", type="password", key="log_p")
            if st.button("Uplink to Dashboard"):
                cursor = db_conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (u_in, p_in))
                user_row = cursor.fetchone()
                if user_row:
                    login_success(user_row)
                else:
                    st.error("Access Denied: Invalid Credentials")
    st.stop()

# --- 5. TOP NAVIGATION & MUDRA WALLET ---
u = st.session_state.user
PrakritUI.wallet_widget(u.get('wallet', 0))

# Logout Button
st.markdown('<div style="position: fixed; top: 15px; right: 20px; z-index: 1001;">', unsafe_allow_html=True)
if st.button("Secure Logout 🚪"):
    logout()
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. AUTO-ROUTING ENGINE ---
role_map = {
    "NGO Auditor": "portals/auditor/verify.py",
    "Event Organizer": "portals/organizer/dashboard.py",
    "Customer": "portals/marketplace/browse.py"
}

path = role_map.get(u['role'])
if path and os.path.exists(path):
    with open(path, "r") as f:
        # Pass the SQLite connection and user dictionary to portals
        exec(f.read(), globals(), {"db": db_conn, "u": u})
else:
    st.error(f"Portal path '{path}' not found. Verify your file structure.")