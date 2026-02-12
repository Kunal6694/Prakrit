import streamlit as st
import sqlite3
import os
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
# 2. DATABASE INITIALIZATION
# --------------------------------------------------
@st.cache_resource
def init_sqlite():
    conn = sqlite3.connect("prakrit_system.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            company TEXT,
            wallet INTEGER,
            audited BOOLEAN,
            score REAL,
            location TEXT,
            category TEXT,
            phone TEXT,
            prakrit_id TEXT UNIQUE
        )
    """)

    conn.commit()
    return conn

db_conn = init_sqlite()
st.session_state.db = db_conn

# --------------------------------------------------
# 3. SESSION MANAGEMENT
# --------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "show_registration" not in st.session_state:
    st.session_state.show_registration = False

if "registered_id" not in st.session_state:
    st.session_state.registered_id = None


# Token login persistence
token = st.query_params.get("token")
if token and st.session_state.user is None:
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (token,))
    user_row = cursor.fetchone()
    if user_row:
        st.session_state.user = {
            "id": user_row[0],
            "username": user_row[1],
            "role": user_row[3],
            "company": user_row[4],
            "wallet": user_row[5],
            "audited": user_row[6],
            "score": user_row[7],
            "location": user_row[8],
            "category": user_row[9],
            "phone": user_row[10],
            "prakrit_id": user_row[11],
        }


def login_success(user_row):
    st.session_state.user = {
        "id": user_row[0],
        "username": user_row[1],
        "role": user_row[3],
        "company": user_row[4],
        "wallet": user_row[5],
        "audited": user_row[6],
        "score": user_row[7],
        "location": user_row[8],
        "category": user_row[9],
        "phone": user_row[10],
        "prakrit_id": user_row[11],
    }
    st.query_params["token"] = str(user_row[0])
    st.rerun()


def logout():
    st.query_params.clear()
    st.session_state.user = None
    st.rerun()


# --------------------------------------------------
# 4. AUTHENTICATION UI
# --------------------------------------------------
if st.session_state.user is None:

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.title("🌿 Prakrit")
        st.subheader("Deciphering Nature with AI-Verified Integrity")

    with col2:

        # -------------------------
        # SUCCESS SCREEN
        # -------------------------
        if st.session_state.registered_id:
            st.success("✅ Account Created Successfully!")

            pid = st.session_state.registered_id

            st.markdown(f"""
                <div style="border:2px solid #10b981;padding:20px;border-radius:15px;text-align:center;">
                    <p>OFFICIAL PRAKRIT ID</p>
                    <h2 style="font-family:monospace;">{pid}</h2>
                </div>
            """, unsafe_allow_html=True)

            if st.button("Proceed to Login", key="success_login_btn"):
                st.session_state.registered_id = None
                st.session_state.show_registration = False
                st.rerun()

            st.stop()

        # -------------------------
        # LOGIN & REGISTRATION
        # -------------------------
        if not st.session_state.show_registration:

            tabs = st.tabs(["Login to Dashboard", "Join the Ecosystem"])

            # ---------------- LOGIN TAB ----------------
            with tabs[0]:
                login_username = st.text_input(
                    "Username or Prakrit ID",
                    key="login_username"
                )

                login_password = st.text_input(
                    "Password",
                    type="password",
                    key="login_password"
                )

                if st.button("Uplink to Dashboard", key="login_btn"):
                    cursor = db_conn.cursor()
                    cursor.execute("""
                        SELECT * FROM users
                        WHERE (username = ? OR prakrit_id = ?) AND password = ?
                    """, (login_username, login_username, login_password))

                    user_row = cursor.fetchone()

                    if user_row:
                        login_success(user_row)
                    else:
                        st.error("Invalid Credentials")

            # ---------------- ROLE SELECTION TAB ----------------
            with tabs[1]:
                st.markdown("## 🌿 Join the Ecosystem as")

                role_select = st.selectbox(
                    "Select your role:",
                    ["Customer", "NGO Auditor", "Event Organizer"],
                    key="role_select_box"
                )

                if st.button("Proceed to Registration", key="role_proceed_btn"):
                    st.session_state.temp_role = role_select
                    st.session_state.show_registration = True
                    st.rerun()

        # -------------------------
        # REGISTRATION FORM
        # -------------------------
        else:

            role = st.session_state.get("temp_role", "Customer")

            st.markdown(f"### Register as {role}")

            with st.form("registration_form"):

                reg_username = st.text_input(
                    "Choose Username",
                    key="reg_username"
                )

                reg_password = st.text_input(
                    "Set Password",
                    type="password",
                    key="reg_password"
                )

                reg_company = st.text_input(
                    "Full Name / Organization",
                    key="reg_company"
                )

                reg_phone = st.text_input(
                    "Phone Number",
                    key="reg_phone"
                )

                submit_reg = st.form_submit_button("Complete Registration")

                if submit_reg:

                    if not reg_username or not reg_password or not reg_company:
                        st.error("Please fill all required fields.")
                    else:
                        try:
                            cursor = db_conn.cursor()

                            cursor.execute("SELECT COUNT(*) FROM users")
                            count = cursor.fetchone()[0]
                            generated_id = f"PRK-{1001 + count}"

                            cursor.execute("""
                                INSERT INTO users
                                (username, password, role, company, wallet,
                                 audited, score, location, category,
                                 phone, prakrit_id)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                reg_username,
                                reg_password,
                                role,
                                reg_company,
                                0,
                                False,
                                0.0,
                                "India",
                                "Standard",
                                reg_phone,
                                generated_id
                            ))

                            db_conn.commit()

                            st.session_state.registered_id = generated_id
                            st.rerun()

                        except sqlite3.IntegrityError:
                            st.error("Username already exists.")

    st.stop()

# --------------------------------------------------
# 5. LOGGED IN SECTION
# --------------------------------------------------

u = st.session_state.user

PrakritUI.wallet_widget(u.get("wallet", 0))

if st.button("Secure Logout 🚪", key="logout_btn"):
    logout()

# --------------------------------------------------
# 6. ROLE ROUTING (SAFE VERSION)
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
    st.info("Dashboard loaded successfully.")