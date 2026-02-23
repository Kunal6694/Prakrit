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
PrakritUI.minimalist_leaf_animation()

# --- IMPROVED UNIVERSAL HOVER GLOW CSS ---

st.markdown("""
<style>
    /* 1. Targets every type of button in the Streamlit ecosystem */
    div.stButton > button, 
    div.stFormSubmitButton > button, 
    button[kind="secondary"], 
    button[kind="primary"] {
        transition: all 0.3s ease-in-out !important;
    }

    /* 2. Applies the glow and lift on hover for all of them */
    div.stButton > button:hover, 
    div.stFormSubmitButton > button:hover,
    button:hover {
        background-color: #7fa85d !important; 
        color: white !important;
        box-shadow: 0 0 20px rgba(46, 125, 50, 0.8) !important; 
        transform: translateY(-3px) !important;
        cursor: pointer !important;
    }
    
    /* 3. Adds a "click" feel (slight shrink) */
    button:active {
        transform: translateY(-1px) !important;
        box-shadow: 0 0 5px rgba(46, 125, 50, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)


# --- TOP-CORNER LEAFY BRANCHES & ECO-LUXURY SPARKLES ---
st.markdown("""
<div class="branch-top-left">
    🌿<span class="minimal-flower" style="top: 35px; left: 45px;">✨</span>
</div>
<div class="branch-top-right">
    🌿<span class="minimal-flower" style="top: 35px; left: 45px;">✨</span>
</div>

<style>
    /* Pinning the branches to the corners */
    .branch-top-left {
        position: fixed;
        top: -10px;
        left: -10px;
        font-size: 80px; 
        transform: rotate(45deg);
        opacity: 0.3; /* Keeps your original subtle background visibility */
        z-index: 9999;
        pointer-events: none;
        filter: drop-shadow(2px 2px 5px rgba(0,0,0,0.1));
    }

    .branch-top-right {
        position: fixed;
        top: -10px;
        right: -10px;
        font-size: 80px;
        transform: rotate(-45deg) scaleX(-1);
        opacity: 0.3; /* Keeps your original subtle background visibility */
        z-index: 9999;
        pointer-events: none;
        filter: drop-shadow(-2px 2px 5px rgba(0,0,0,0.1));
    }

    /* Positioning the sparkles right on the leaves */
    .minimal-flower {
        position: absolute;
        font-size: 30px; 
        transform: rotate(-20deg); 
    }
</style>
""", unsafe_allow_html=True)

#.........................................

st.markdown("""
<style>
    /* Reduce the massive default Streamlit top padding */
    .block-container {
        padding-top: 2rem !important; /* Change to 1rem if you want it even tighter */
        padding-bottom: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 2. DATABASE INITIALIZATION
# --------------------------------------------------

@st.cache_resource
def init_sqlite():
    import sqlite3
    conn = sqlite3.connect("prakrit_system.db", check_same_thread=False)
    cursor = conn.cursor()

        # --- MIGRATION BLOCK: INTEGRATING KUNAL'S LOGIC ---

    # 1. New Branding Columns for Organizers
    for col in [("about", "TEXT"), ("address", "TEXT"), ("map_link", "TEXT"), ("prakrit_id", "TEXT")]:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col[0]} {col[1]}")
        except:
            pass # Column already exists

    # 2. AI Audit Columns for Bookings
    for col in [("audit_score", "REAL"), ("audit_status", "TEXT"), ("auditor_name", "TEXT"), 
                ("demands", "TEXT"), ("items", "TEXT")]:
        try:
            cursor.execute(f"ALTER TABLE bookings ADD COLUMN {col[0]} {col[1]}")
        except:
            pass # Column already exists

    # 3. Transaction Details (Mudra History)
    try:
        cursor.execute("ALTER TABLE transactions ADD COLUMN reason TEXT")
    except:
        pass

    conn.commit()

        # Place this near your database connection logic in prakrit_app.py
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            category TEXT,
            organizer TEXT,
            status TEXT DEFAULT 'active'
        )
    """)
    

    # 1. Users table (Preserved)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE, password TEXT, role TEXT, 
            wallet INTEGER DEFAULT 0, prakrit_id TEXT UNIQUE
        )
    """)

    # 2. Transactions table (Preserved)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT, type TEXT, amount REAL, 
            timestamp TEXT, details TEXT
        )
    """)

    # 3. Bookings table (Preserved)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id TEXT, customer TEXT, organizer TEXT, 
            status TEXT, total_price REAL
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS packages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        organizer TEXT,
        score REAL DEFAULT 0.0,
        description TEXT,
        price REAL,
        location TEXT DEFAULT 'JAIPUR',
        category TEXT DEFAULT 'PREMIUM',
        auditor_name TEXT
    )
""")

    # --- RECTIFICATION BLOCK: ADD MISSING COLUMNS ---
    # This specifically fixes the "no such column: reason" error
    try:
        cursor.execute("ALTER TABLE transactions ADD COLUMN reason TEXT")
    except: pass

    try:
        cursor.execute("ALTER TABLE transactions ADD COLUMN status TEXT")
    except: pass

    conn.commit()
    return conn

db_conn = init_sqlite()
# Ensure db is in session state for portals to access via "db"
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
        # Map DB row to user dictionary exactly as expected by portals
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
    # Mapping the extended database row into the session dictionary
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
        # NEW: Adding Kunal's branding & identity fields
        "about": user_row[11] if len(user_row) > 11 else "",
        "address": user_row[12] if len(user_row) > 12 else "",
        "map_link": user_row[13] if len(user_row) > 13 else "",
        "prakrit_id": user_row[14] if len(user_row) > 14 else ""
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
    lottie_welcome = PrakritUI.load_lottie("https://lottie.host/8282361a-7e0e-473d-9d41-3b7c8441164a/H9m1m5WjN6.json")
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.title("🌿 Prakrit")
        st.subheader("Deciphering Nature with AI-Verified Integrity")
        if lottie_welcome:
            from streamlit_lottie import st_lottie
            st_lottie(lottie_welcome, height=350, key="welcome_anim")

    with col2:
        # --- SUCCESS SCREEN AFTER REGISTRATION ---
        if st.session_state.registered_id:
            st.success("✅ Account Created Successfully!")
            pid = st.session_state.registered_id
            
            st.divider()
            st.caption("OFFICIAL PRAKRIT ID")
            st.code(pid, language=None)
            st.divider()
            
            id_card_text = f"PRAKRIT ECOSYSTEM\nUnique ID: {pid}\nStatus: Verified User"
            st.download_button("📥 Download ID Credentials", id_card_text, file_name=f"Prakrit_ID_{pid}.txt", use_container_width=True)
            
            if st.button("PROCEED TO LOGIN", use_container_width=True, key="final_login_btn"):
                st.session_state.registered_id = None
                st.session_state.show_registration = False
                st.rerun()
            st.stop()

        if not st.session_state.get("show_registration"):
            t1, t2 = st.tabs(["Login to Dashboard", "Join the Ecosystem"])

            with t1:
                u_in = st.text_input("Username or Prakrit ID", key="log_u")
                p_in = st.text_input("Password", type="password", key="log_p")
                if st.button("Uplink to Dashboard"):
                    cursor = db_conn.cursor()
                    cursor.execute("""
                        SELECT * FROM users 
                        WHERE (username = ? OR prakrit_id = ?) AND password = ?
                    """, (u_in, u_in, p_in))
                    user_row = cursor.fetchone()
                    if user_row:
                        login_success(user_row)
                    else:
                        st.error("Access Denied: Invalid Credentials")

            with t2:
                st.markdown("## 🌿 Join the Ecosystem")
                selected_role = st.selectbox("Select your role:", ["Customer", "NGO Auditor", "Event Organizer"], key="reg_role_select")
                if st.button("PROCEED TO REGISTRATION", use_container_width=True):
                    st.session_state.show_registration = True
                    st.session_state.temp_role = selected_role
                    st.rerun()
        
        else:
            # --- REGISTRATION FORM ---
            current_role = st.session_state.get("temp_role", "User")
            PrakritUI.apply_glass_forms()

            # --- NEW: BACK BUTTON HEADER ---
            col_header, col_back = st.columns([5, 1])
            with col_header:
                st.markdown(f"### Register as {current_role}")
            with col_back:
                # This button resets the registration state and returns user to the login tabs
                if st.button("⬅️ Back", key="reg_back_btn", use_container_width=True):
                    st.session_state.show_registration = False
                    st.rerun()
            # -------------------------------
            
            location_data = {
                "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
                "Karnataka": ["Bengaluru", "Mysuru"],
                "Delhi": ["New Delhi", "North Delhi"],
                "Tamil Nadu": ["Chennai", "Coimbatore"]
            }

            v_loc = "General"
            if current_role == "Event Organizer":
                col_s, col_c = st.columns(2)
                with col_s:
                    state = st.selectbox("Select State*", [""] + sorted(list(location_data.keys())), key="dynamic_state")
                with col_c:
                    if state:
                        v_loc = st.selectbox("Select City*", sorted(location_data[state]), key="dynamic_city")
                    else:
                        v_loc = st.selectbox("Select City*", ["Select State first"], disabled=True)
                st.markdown("---")

            with st.form("detailed_reg"):
                st.write("Account Details")
                new_u = st.text_input("Choose Username*")
                new_p = st.text_input("Set Password*", type="password")

                company_val = ""
                phone_val = ""

                if current_role == "Customer":
                    company_val = st.text_input("Full Name*")
                    c_email = st.text_input("Email Address*")
                    phone_val = st.text_input("Contact Number*")
                elif current_role == "Event Organizer":
                    
                    company_val = st.text_input("Venue Name*")
                    phone_val = st.text_input("Phone Number*")
                    v_mail = st.text_input("E-mail address*")
                    v_capacity = st.number_input("Maximum Capacity*", min_value=1)
                    v_type = st.selectbox("Venue type", ["Indoor","Outdoor","Hybrid"])
                    t_and_c = st.checkbox("I accept the terms and conditions*")
                elif current_role == "NGO Auditor":
                    company_val = st.text_input("NGO Organization Name*")
                    org_mail = st.text_input("E-mail*")
                    phone_val = st.text_input("Phone Number*")
                    org_link = st.text_input("Official Portal")

                if st.form_submit_button("Complete Registration"):
                    if not new_u or not new_p or not company_val:
                        st.error("🚨 Please fill in all mandatory fields!")
                    else:
                        try:
                            cursor = db_conn.cursor()
                            cursor.execute("SELECT COUNT(*) FROM users")
                            user_count = cursor.fetchone()[0]
                            generated_id = f"PRK-{1000 + user_count + 1}"
                            
                            cursor.execute("""
                                INSERT INTO users (username, password, role, company, phone, location, prakrit_id, wallet, score, audited) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (new_u, new_p, current_role, company_val, phone_val, v_loc, generated_id, 0, 0.0, False))
                            
                            db_conn.commit()
                            st.session_state.registered_id = generated_id
                            st.rerun()
                        except Exception as e:
                            st.error(f"⚠️ Registration failed: {e}")

# --------------------------------------------------
# 6. ROLE ROUTING (FIXED LOGIC)
# --------------------------------------------------
u = st.session_state.get("user")

if u:
    # 1. NAVIGATION UI
    st.markdown('<div class="logout-container">', unsafe_allow_html=True)
    if st.button("Logout 🚪", key="global_logout"):
        logout()
    st.markdown('</div>', unsafe_allow_html=True)
    
    PrakritUI.wallet_widget(u.get("wallet", 0) if u else 0)

    # --- STEP 3: LIVE PATHWAY PULSE INTEGRATION ---
    pulse_text = "● SYSTEM INITIALIZING... | ● CONNECTING TO PATHWAY STREAM"
    try:
        if os.path.exists("data/live_pulse.jsonl"):
            with open("data/live_pulse.jsonl", "r") as f:
                lines = f.readlines()
                if lines:
                    import json
                    latest_update = json.loads(lines[-1])
                    avg_s = latest_update.get('avg_score', 0)
                    total = latest_update.get('total_events', 0)
                    pulse_text = f"● GLOBAL ECO-INDEX: {avg_s:.2f} | ● TOTAL VERIFIED EVENTS: {total} | ● LIVE PATHWAY PULSE ACTIVE"
    except Exception:
        pulse_text = "● 50 PrakritMudra awarded on confirmed payments! | ● STANDBY FOR LIVE PULSE"

    PrakritUI.live_ticker(pulse_text)

    # 2. ROLE MAP & PATH DEFINITION
    role_map = {
        "NGO Auditor": "portals/auditor/verify.py",
        "Event Organizer": "portals/organizer/dashboard.py",
        "Customer": "portals/marketplace/browse.py"
    }

    path = role_map.get(u.get("role"))

    # --- STEP 4: ENHANCED PORTAL EXECUTION ---
    # NOTE: This must be INDENTED inside the 'if u:' block!
    if path and os.path.exists(path):
        with open(path, "r") as f:
            code = f.read()
            
            # We inject 'PrakritUI' so Kunal's files use YOUR beige design
            portal_scope = {
                "db": db_conn, 
                "u": u, 
                "st": st, 
                "PrakritUI": PrakritUI
            }
            
            try:
                # Execute with your UI class in the namespace
                exec(code, globals(), portal_scope)
            except Exception as e:
                st.error(f"Error loading portal: {e}")
    else:
        st.warning(f"Dashboard file not found at: {path}")

        