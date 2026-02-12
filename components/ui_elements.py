import streamlit as st
from streamlit_lottie import st_lottie
import requests
from fpdf import FPDF


class PrakritUI:
    @staticmethod
    def inject_pro_css():
        """Lauki-Glass Theme: Pale Bottle-Gourd Transparency, Neon Accents, and Floating Leaves."""
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Outfit:wght@300;600;900&display=swap');

            /* 1. HIDE DEFAULT UI */
            header, footer, #MainMenu {visibility: hidden; height: 0;}
            [data-testid="stHeader"] {display: none;}
            [data-testid="stSidebar"] {display: none;}

            /* 2. BASE: DEEP FOREST BACKGROUND (Nature Eye-Care) */
            .stApp {
                background: linear-gradient(135deg, #040d0a 0%, #081a14 100%);
                color: #FFFFFF;
                font-family: 'Outfit', sans-serif;
            }

            /* 3. BOTTLE GOURD GLASS CARDS (Pale Lauki Green) */
            .glass-card, [data-testid="stVerticalBlock"] > div:has(div.stTabs) {
                background: rgba(216, 239, 211, 0.12); /* Soft Lauki Green */
                backdrop-filter: blur(15px);
                -webkit-backdrop-filter: blur(15px);
                border: 1px solid rgba(188, 226, 158, 0.25);
                border-radius: 24px;
                padding: 30px;
                margin-bottom: 25px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            }

            /* Transparent Tabs for Login/Registration */
            .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
            .stTabs [data-baseweb="tab"] {
                background-color: rgba(216, 239, 211, 0.08);
                border-radius: 12px 12px 0 0;
                color: #FFFFFF;
            }

            /* 4. HIGH-CONTRAST NEON BUTTONS */
            .stButton>button {
                width: 100%;
                border-radius: 12px;
                background: #39FF14; /* Neon Lime */
                color: #040d0a !important; /* Deep Black for visibility */
                font-family: 'Syncopate', sans-serif;
                font-weight: 700;
                border: none;
                padding: 16px;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            .stButton>button:hover {
                background: #FFFFFF;
                box-shadow: 0 0 30px #FFFFFF;
                transform: scale(1.02);
            }

            /* 5. NATURE ANIMATION: FLOATING LEAVES */
            @keyframes float {
                0% { transform: translateY(0px) rotate(0deg); opacity: 0; }
                20% { opacity: 0.4; }
                80% { opacity: 0.4; }
                100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
            }
            .particle {
                position: fixed; bottom: -10%; z-index: 0;
                color: #39FF14; font-size: 20px;
                animation: float 12s linear infinite;
                pointer-events: none;
            }

            /* 6. WALLET WIDGET */
            .wallet-badge {
                background: rgba(216, 239, 211, 0.1);
                border: 2px solid #39FF14;
                border-radius: 50px;
                padding: 10px 25px;
                color: #FFFFFF;
                font-family: 'Syncopate', sans-serif;
                font-weight: 700;
            }
            </style>

            <div class="particle" style="left: 10%; animation-delay: 0s;">🍃</div>
            <div class="particle" style="left: 40%; animation-delay: 4s;">🌿</div>
            <div class="particle" style="left: 70%; animation-delay: 8s;">🍃</div>
            <div class="particle" style="left: 90%; animation-delay: 2s;">🌱</div>
        """, unsafe_allow_html=True)

    @staticmethod
    def load_lottie(url: str):
        try:
            r = requests.get(url)
            return r.json() if r.status_code == 200 else None
        except:
            return None

    @staticmethod
    def wallet_widget(amount):
        """High-Contrast Mudra Widget."""
        st.markdown(f"""
            <div style="position: fixed; top: 15px; right: 120px; z-index: 1001;">
                <div class="wallet-badge">
                    MUDRA // {amount}
                </div>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def live_ticker(text):
        """Lauki-Glass Activity Ticker."""
        st.markdown(f"""
            <div style="background: rgba(216, 239, 211, 0.05); border-left: 5px solid #39FF14; border-right: 5px solid #39FF14; padding: 12px; margin-bottom: 35px; border-radius: 50px;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="color:#39FF14; font-family:'Syncopate'; font-weight:900; font-size: 0.7rem; margin-left:15px;">PULSE</span>
                    <marquee scrollamount="6" style="color:#FFFFFF; font-weight: 600;">{text.upper()}</marquee>
                </div>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def venue_card(name, organizer, score, desc, price, location="JAIPUR", category="PREMIUM", auditor=None):
        """Lauki-Glass Modular Card."""
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span style="background: rgba(57, 255, 20, 0.2); color:#39FF14; padding:3px 10px; border-radius:5px; font-size:0.6rem; font-family:'Syncopate';">{category}</span>
                    <h2 style="margin:10px 0 2px 0; font-size:1.8rem; font-weight:900; color:#FFFFFF;">{name.upper()}</h2>
                    <p style="color:#39FF14; opacity:0.8; margin:0; font-size:0.9rem;">BY @{organizer.upper()}</p>
                </div>
                <div style="text-align: right;">
                    <div style="color: #39FF14; font-size: 1.8rem; font-weight: 700; font-family: 'Syncopate';">{score}</div>
                    <div style="color: #FFFFFF; font-size: 0.6rem; opacity:0.6;">ECO INDEX</div>
                </div>
            </div>
            <p style="color:#FFFFFF; opacity:0.7; margin:20px 0; font-size:1rem;">{desc}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(216, 239, 211, 0.2); padding-top:15px;">
                <div style="color:#FFFFFF; font-size:0.8rem;">
                    📍 {location.upper()} <br>
                    <span style="color:#39FF14;">VERIFIED: {auditor if auditor else 'PENDING'}</span>
                </div>
                <div style="font-size:1.6rem; font-weight:900; color:#FFFFFF;">₹{price}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def green_certificate_ui(org_name, score):
        """Visual Certificate Style."""
        st.markdown(f"""
            <div style="border: 2px dashed #39FF14; border-radius: 24px; padding: 40px; text-align: center; background: rgba(216, 239, 211, 0.05);">
                <h1 style="color: #39FF14; margin-bottom: 10px; font-family:'Syncopate';">CERTIFIED</h1>
                <p style="color: #f3f4f6; font-size: 1.2rem;"><b>{org_name.upper()}</b> has passed the AI Sustainability Audit.</p>
                <div style="font-size: 4rem; font-weight: 900; color: #ffffff; margin: 20px 0;">{score}/10</div>
                <p style="color: #39FF14;">Verified by Prakrit NGO Authority</p>
            </div>
        """, unsafe_allow_html=True)

        class CertificateGenerator:
            @staticmethod
            def create_pdf(org_name, score, date):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_fill_color(4, 13, 10)
                pdf.rect(0, 0, 210, 297, 'F')
                pdf.set_text_color(57, 255, 20)
                pdf.set_font("Arial", 'B', 30)
                pdf.cell(200, 40, "PRAKRIT GREEN BADGE", ln=True, align='C')
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", '', 16)
                pdf.cell(200, 20, f"This is to certify that", ln=True, align='C')
                pdf.set_font("Arial", 'B', 24)
                pdf.cell(200, 20, f"{org_name}", ln=True, align='C')
                pdf.set_font("Arial", 'B', 40)
                pdf.cell(200, 40, f"{score}/10", ln=True, align='C')
                pdf.set_font("Arial", 'I', 12)
                pdf.cell(200, 10, f"Verified on: {date}", ln=True, align='C')
                return pdf.output(dest='S').encode('latin-1')