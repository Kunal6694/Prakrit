import streamlit as st
from streamlit_lottie import st_lottie
import requests
from fpdf import FPDF

class PrakritUI:
    @staticmethod
    def inject_pro_css():
        """The Billion Dollar Theme: Glassmorphism, Persistent Layouts, and Luxury UI."""
        st.markdown("""
            <style>
            /* 1. Hiding standard Streamlit clutter & Top Bar */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0px;}
            [data-testid="stSidebar"] { display: none; }

            /* 2. Global Professional Dark Aesthetic */
            .stApp {
                background: radial-gradient(circle at 10% 20%, #111827 0%, #000000 100%);
                color: #f3f4f6;
                font-family: 'Inter', sans-serif;
            }

            /* 3. High-End Glass Cards */
            .glass-card {
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 24px;
                padding: 30px;
                margin-bottom: 25px;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            .glass-card:hover {
                border-color: #10b981;
                transform: translateY(-8px);
                box-shadow: 0 25px 50px -12px rgba(16, 185, 129, 0.2);
            }

            /* 4. Luxury Wallet & Top Navigation Bar */
            .top-nav {
                position: fixed;
                top: 0; right: 0; left: 0;
                height: 70px;
                background: rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(15px);
                display: flex;
                justify-content: flex-end;
                align-items: center;
                padding: 0 40px;
                z-index: 1000;
                border-bottom: 1px solid rgba(255,255,255,0.05);
            }

            .wallet-badge {
                background: rgba(16, 185, 129, 0.15);
                border: 1px solid #10b981;
                border-radius: 50px;
                padding: 8px 20px;
                color: #10b981;
                font-weight: 800;
                font-size: 0.9rem;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            /* 5. Animated Neon Buttons */
            .stButton>button {
                width: 100%;
                border-radius: 14px;
                background: #ffffff;
                color: #000000;
                font-weight: 800;
                border: none;
                padding: 14px 28px;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1.2px;
            }
            .stButton>button:hover {
                background: #10b981;
                color: #ffffff;
                box-shadow: 0 0 25px rgba(16, 185, 129, 0.5);
            }

            /* 6. Search Bar & Filter Containers */
            .filter-container {
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 20px;
                padding: 20px;
                margin-bottom: 35px;
            }

            /* 7. Category Tags */
            .tag {
                background: rgba(59, 130, 246, 0.1);
                color: #3b82f6;
                padding: 4px 12px;
                border-radius: 6px;
                font-size: 0.75rem;
                font-weight: 600;
                margin-right: 8px;
            }
            </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def load_lottie(url: str):
        try:
            r = requests.get(url)
            return r.json() if r.status_code == 200 else None
        except: return None

    @staticmethod
    def wallet_widget(amount):
        """Persistent Wallet UI component."""
        st.markdown(f"""
            <div style="position: fixed; top: 15px; right: 120px; z-index: 1001;">
                <div class="wallet-badge">
                    🪙 {amount} PrakritMudra
                </div>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def live_ticker(text):
        """A professional rolling ticker for live AI & booking activity."""
        st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 50px; padding: 10px 25px; margin-bottom: 30px; display: flex; align-items: center; gap: 15px;">
                <span style="color:#10b981; font-weight:bold; white-space: nowrap;">● LIVE ACTIVITY:</span>
                <marquee scrollamount="6" style="color:#94a3b8; font-size: 0.9rem;">{text}</marquee>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def venue_card(name, organizer, score, desc, price, location="Jaipur", category="Premium"):
        """Enhanced Modular Card with Category Tags and refined spacing."""
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <span class="tag">{category}</span>
                    <h2 style="margin:8px 0 0 0; font-size:1.7rem; letter-spacing:-0.8px; color:#ffffff;">{name}</h2>
                    <p style="color:#6b7280; margin:4px 0; font-weight:500;">
                        Partnered with <span style="color:#10b981;">{organizer}</span>
                    </p>
                </div>
                <div style="background: linear-gradient(135deg, #064e3b 0%, #10b981 100%); color:#ffffff; padding:8px 20px; border-radius:100px; font-weight:bold; font-size:0.85rem; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);">
                    ECO-INDEX: {score}
                </div>
            </div>
            <p style="color:#9ca3af; font-size:1rem; line-height:1.7; margin:20px 0;">{desc}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top:20px; margin-top: 10px;">
                <div style="color:#6b7280; font-size:0.9rem; display: flex; align-items: center; gap: 10px;">
                    <span>📍 {location}</span>
                    <span>•</span>
                    <span style="color:#facc15;">⭐ 4.9 Premium</span>
                </div>
                <div style="font-size:1.3rem; font-weight:800; color:#ffffff;">
                    ₹{price}<span style="font-size:0.8rem; color:#6b7280; font-weight:400; margin-left:4px;">/event</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def green_certificate_ui(org_name, score):
        """Visual placeholder/style for the Green Certificate download."""
        st.markdown(f"""
            <div style="border: 2px dashed #10b981; border-radius: 20px; padding: 40px; text-align: center; background: rgba(16, 185, 129, 0.05);">
                <h1 style="color: #10b981; margin-bottom: 10px;">🍃 Green Certification</h1>
                <p style="color: #f3f4f6; font-size: 1.2rem;">This certifies that <b>{org_name}</b> has passed the AI Sustainability Audit.</p>
                <div style="font-size: 3rem; font-weight: 900; color: #ffffff; margin: 20px 0;">Score: {score}/10</div>
                <p style="color: #94a3b8;">Verified by Prakrit NGO Authority</p>
            </div>
        """, unsafe_allow_html=True)
        # Install fpdf: pip install fpdf


        class CertificateGenerator:
            @staticmethod
            def create_pdf(org_name, score, date):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_fill_color(15, 23, 42)  # Dark theme matching Prakrit
                pdf.rect(0, 0, 210, 297, 'F')

                pdf.set_text_color(16, 185, 129)  # Green
                pdf.set_font("Arial", 'B', 30)
                pdf.cell(200, 40, "PRAKRIT GREEN BADGE", ln=True, align='C')

                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", '', 16)
                pdf.cell(200, 20, f"This is to certify that", ln=True, align='C')
                pdf.set_font("Arial", 'B', 24)
                pdf.cell(200, 20, f"{org_name}", ln=True, align='C')

                pdf.set_font("Arial", '', 16)
                pdf.cell(200, 20, f"Has achieved an AI Sustainability Score of", ln=True, align='C')
                pdf.set_font("Arial", 'B', 40)
                pdf.cell(200, 40, f"{score}/10", ln=True, align='C')

                pdf.set_font("Arial", 'I', 12)
                pdf.cell(200, 10, f"Verified on: {date}", ln=True, align='C')
                return pdf.output(dest='S').encode('latin-1')