import streamlit as st
from streamlit_lottie import st_lottie
import requests
from fpdf import FPDF


class PrakritUI:

    

    

    @staticmethod
    def apply_glass_forms():
        """Specifically targets st.form containers for the Eco Luxury Glass look"""
        st.markdown("""
        <style>
        /* This targets the outer shell of any st.form */
        div[data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.45) !important;
            backdrop-filter: blur(18px) !important;
            -webkit-backdrop-filter: blur(18px) !important;
            border-radius: 24px !important;
            padding: 40px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
        }
        </style>
        """, unsafe_allow_html=True)
    def inject_pro_css():
        """Eco Luxury Glass Theme - Global Visibility & Font Fix"""
        

        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Alegreya:wght@600;700&family=Alegreya+Sans:wght@300;400;600&family=Syncopate:wght@400;700&display=swap');

               
        
        

        /* A. THE FOUNDATION: FORCE LIGHT THEME & FONT */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #F8ECD6 !important; /* Your Beige Base */
            color: #1F2937 !important;
            font-family: 'Alegreya Sans', sans-serif !important;
        }

        /* B. THE BLACK BOX KILLER: Target technical blocks specifically */
        code, pre, .stCodeBlock, div[data-testid="stCodeBlock"], .stMarkdown pre {
            background-color: transparent !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #1F2937 !important;
        }

        /* 1. GLOBAL FONT RESET */
        html, body, [class*="st-"], .stMarkdown, .stText, p, span, label, input, select, textarea {
            font-family: 'Alegreya Sans', sans-serif !important;
            color: #1F2937 !important;
        }

        h1 {
            font-family: 'Alegreya' !important;
            color: #000000 !important;
        }

        h2 {
            font-family: 'Alegreya', sans-serif;
            color: #000000;}
        
        h3 {
            font-family: 'Alegreya Sans' !important;
            color: #1F2937 !important;
        }

# /* 2. MAIN BACKGROUND WITH BRANCHES */
# [data-testid="stAppViewContainer"] {
#     background-image: 
#         url("https://www.svgrepo.com/show/475147/leaf-1.svg"), /* Left Branch */
#         url("https://www.svgrepo.com/show/475147/leaf-1.svg"), /* Right Branch */
#         linear-gradient(135deg, #F8ECD6 0%, #F3E2C3 100%) !important;
        
#     background-position: 
#         left 30px center, 
#         right 30px center, 
#         center center !important;
        
#     background-size: 
#         150px auto, 
#         150px auto, 
#         cover !important;
        
#     background-repeat: no-repeat !important;
#     background-attachment: fixed !important;
# }

# /* 2.1 MAKING THE BRANCHES MINIMAL (Subtle Opacity) */
# /* This ensures the SVGs aren't too bright and match the "Glass" aesthetic */
# [data-testid="stAppViewContainer"]::before {
#     content: "";
#     position: absolute;
#     top: 0; left: 0; right: 0; bottom: 0;
#     background: inherit;
#     opacity: 0.1; /* High transparency for a minimal look */
#     pointer-events: none;
# }

# /* 2.2 CLEARING OVERLAYS */
# /* Forces the actual content area to be transparent so the background shows through */
# [data-testid="stMainViewContainer"], [data-testid="stHeader"] {
#     background: transparent !important;
# }
        /* 3. INPUT FIELDS & COLUMNS VISIBILITY FIX */
        div[data-baseweb="input"], div[data-baseweb="input"] > div {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 12px !important;
            border: 1px solid #8BAE66 !important;
        }

        input {
            color: #1F2937 !important;
            background-color: transparent !important;
            -webkit-text-fill-color: #1F2937 !important;
        }


        /* --- THE ULTIMATE BLACK BOX KILLER --- */

        /* 1. FIX NUMBER INPUT BUTTONS (+ and -) */
        [data-testid="stNumberInputStepUp"], 
        [data-testid="stNumberInputStepDown"],
        [data-testid="stNumberInput"] button {
            background-color: #8BAE66 !important; /* Eco-Luxury Green */
            background: #8BAE66 !important;
            color: #1F2937 !important;
            border: none !important;
        }
        [data-testid="stNumberInputStepUp"] svg, 
        [data-testid="stNumberInputStepDown"] svg,
        [data-testid="stNumberInput"] button svg {
            fill: #1F2937 !important; /* Dark icons so they are visible */
            color: #1F2937 !important;
        }

        /* 2. FIX FILE UPLOADER (Drag & Drop Zone + Browse Button) */
        [data-testid="stFileUploaderDropzone"],
        [data-testid="stFileUploadDropzone"],
        section[data-testid="stFileUploaderDropzone"] {
            background-color: rgba(255, 255, 255, 0.7) !important;
            background: rgba(255, 255, 255, 0.7) !important;
            border: 2px dashed #8BAE66 !important; /* Green dashed border */
            border-radius: 12px !important;
        }
        /* Fix the text inside the dropzone */
        [data-testid="stFileUploaderDropzone"] *,
        [data-testid="stFileUploadDropzone"] * {
            color: #1F2937 !important;
        }
        /* Fix the Browse Button inside it */
        [data-testid="stFileUploaderDropzone"] button,
        [data-testid="stFileUploadDropzone"] button {
            background-color: #8BAE66 !important;
            color: #1F2937 !important;
            border: none !important;
            font-weight: bold !important;
        }

        /* 3. FIX TEXT AREAS (About Company, Descriptions) */
        [data-testid="stTextArea"] div[data-baseweb="textarea"], 
        [data-testid="stTextArea"] textarea {
            background-color: rgba(255, 255, 255, 0.9) !important;
            background: rgba(255, 255, 255, 0.9) !important;
            color: #1F2937 !important;
            -webkit-text-fill-color: #1F2937 !important;
            border-radius: 12px !important;
            border: none !important; 
        }



        /* 4. RECTIFIED SELECTBOX & DROPDOWN (Fixes the Black background) */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="popover"], 
        div[data-baseweb="popover"] ul {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            border: 1px solid #8BAE66 !important;
            border-radius: 12px !important;
        }

        /* Ensure text inside the black "portal" is visible */
        [data-baseweb="popover"] li, 
        [data-baseweb="popover"] div[role="option"] {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
        }

        /* Hover effect for dropdown items */
        [data-baseweb="popover"] li:hover {
            background-color: #A7C686 !important;
            color: #2F6F4E !important;
        }

        div[data-baseweb="select"] *, 
        [data-baseweb="popover"] * {
            color: #1F2937 !important;
            fill: #1F2937 !important;
            -webkit-text-fill-color: #1F2937 !important;
        }

        /* 5. FORM LABELS & SUBHEADERS */
        .stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label, .stPasswordInput label {
            color: #1F2937 !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
        }

        /* 6. BUTTONS */
        .stButton>button,
        div[data-testid="stFormSubmitButton"]>button {
            width: 100%;
            border-radius: 12px !important;
            background: #8BAE66 !important;
            color: #1F2937 !important;
            font-family: 'Syncopate', sans-serif !important;
            font-weight: 700 !important;
            border: none !important;
            padding: 16px !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
        }

        /* 7. GLASS CARD */
        .glass-card, 
        [data-testid="stVerticalBlock"] > div:has(div.stTabs) {
            background: rgba(255, 255, 255, 0.55);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(255, 255, 255, 0.8);
            border-radius: 24px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        }

        .stButton>button:hover {
            background: #739652 !important;
            transform: scale(1.02) !important;
            color: #FFFFFF !important;
        }

            div.stDownloadButton > button {
        background-color: #A7C686 !important; /* Lighter Green */
        color: #1F2937 !important;           /* Charcoal Text */
        border: none !important;
        width: 100% !important;
        padding: 12px !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        transition: transform 0.2s ease !important;
          }

          div.stDownloadButton > button:hover {
        background-color: #8BAE66 !important; /* Original Green on hover */
        transform: scale(1.01) !important;
         }

        /* F. PUNCH THROUGH HIDDEN LAYERS */
        [data-testid="stMainViewContainer"], [data-testid="stHeader"], .main {
            background-color: transparent !important;
        }

        /* 8. HIDE DEFAULT UI */
        header, footer, #MainMenu {visibility: hidden; height: 0;}
        [data-testid="stHeader"] {display: none;}

        
    .logout-container .stButton > button {
        position: fixed !important; /* Fixed keeps it in view even when scrolling */
        top: 20px !important;
        left: 20px !important;
        width: auto !important; 
        padding: 5px 15px !important;
        z-index: 1002;
        background-color: #f8f9fa !important; /* Optional: light color to stand out */
        border: 1px solid #ddd !important;
    }

    .wallet-badge-fixed {
    position: fixed !important;
    top: 20px !important;
    right: 20px !important;
    background: #8BAE66 !important; /* Matching your main green */
    color: #1F2937 !important;
    padding: 8px 18px !important;
    border-radius: 50px !important;
    font-family: 'Syncopate', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    z-index: 1002;
    box-shadow: 0 0 15px rgba(139, 174, 102, 0.6) !important; /* THE GLOW EFFECT */
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}
        </style>
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
        st.markdown(f"""
            <style>
                .wallet-badge {{
                    background: linear-gradient(135deg, #7fa85d, #739c4f);
                    color: white;
                    padding: 8px 20px;
                    border-radius: 25px;
                    font-weight: 600;
                    font-size: 14px;
                    letter-spacing: 0.5px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                    display: inline-block;
                }}
            </style>

            <div style="
                position: fixed;
                top: 18px;
                right: 120px;
                z-index: 1001;
            ">
                <div class="wallet-badge">
                    💰 MUDRA // {amount}
                </div>
            </div>
        """, unsafe_allow_html=True)


    @staticmethod
    def live_ticker(text):
        st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.6);
                border-left: 5px solid #2F6F4E;
                padding: 12px;
                margin-bottom: 35px;
                border-radius: 50px;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="color:#2F6F4E; font-family:'Syncopate'; font-weight:900; font-size: 0.7rem; margin-left:15px;">
                        PULSE
                    </span>
                    <marquee scrollamount="6" style="color:#1F2937; font-weight: 600;">
                        {text.upper()}
                    </marquee>
                </div>
            </div>
        """, unsafe_allow_html=True)

    

    
    @staticmethod
    def venue_card(name, organizer, score, desc, price, 
                   location="JAIPUR", category="PREMIUM", auditor=None):
        # We define the HTML block starting at the very edge of the screen
        # This prevents Streamlit from interpreting it as indented "code"
        html_string = f"""
<div class="glass-card" style="background-color: rgba(255, 255, 255, 0.55) !important;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <span style="background: rgba(47, 111, 78, 0.15); color:#2F6F4E; padding:3px 10px; border-radius:5px; font-size:0.6rem; font-family:'Syncopate';">
                {category}
            </span>
            <h2 style="margin:10px 0 2px 0; font-size:1.8rem; font-weight:900; color:#1F2937;">
                {name.upper()}
            </h2>
            <p style="color:#4B5563; margin:0; font-size:0.9rem;">
                BY @{organizer.upper()}
            </p>
        </div>
        <div style="text-align: right;">
            <div style="color: #2F6F4E; font-size: 1.8rem; font-weight: 700; font-family: 'Syncopate';">
                {score}
            </div>
            <div style="color: #4B5563; font-size: 0.6rem;">ECO INDEX</div>
        </div>
    </div>
    <div style="color:#1F2937; margin:20px 0; font-size:1rem; background: transparent !important;">
        {desc}
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(0,0,0,0.05); padding-top:15px;">
        <div style="font-size:0.8rem; color:#1F2937;">
            📍 {location.upper()} <br>
            <span style="color:#2F6F4E;">
                VERIFIED: {auditor if auditor else 'PENDING'}
            </span>
        </div>
        <div style="font-size:1.6rem; font-weight:900; color:#1F2937;">₹{price}</div>
    </div>
</div>
"""
        st.markdown(html_string, unsafe_allow_html=True)
    @staticmethod
    def green_certificate_ui(org_name, score):
        st.markdown(f"""
            <div style="
                border: 2px dashed #2F6F4E;
                border-radius: 24px;
                padding: 40px;
                text-align: center;
                background: rgba(255,255,255,0.6);">
                <h1 style="color: #2F6F4E; margin-bottom: 10px; font-family:'Syncopate';">
                    CERTIFIED
                </h1>
                <p style="font-size: 1.2rem;">
                    <b>{org_name.upper()}</b> has passed the AI Sustainability Audit.
                </p>
                <div style="font-size: 4rem; font-weight: 900; margin: 20px 0;">
                    {score}/10
                </div>
                <p style="color: #2F6F4E;">
                    Verified by Prakrit NGO Authority
                </p>
            </div>
        """, unsafe_allow_html=True)



    @staticmethod
    def minimalist_leaf_animation():
        """Injects a subtle, pure-CSS wireframe leaf animation for the Eco-Luxury theme."""
        leaf_html = """
        <style>
            .eco-leaf {
                position: fixed;
                width: 30px;
                height: 30px;
                background-color: transparent;
                /* This CSS trick creates a perfect, geometric leaf silhouette */
                border-radius: 0 25px 0 25px; 
                border: 1.5px solid rgba(139, 174, 102, 0.25); /* Subtle Sage Green */
                pointer-events: none; /* Clicks pass right through it */
                z-index: -1; /* Keeps it strictly in the deep background */
                animation: floatUp linear infinite;
                opacity: 0;
            }
            
            /* Varying positions, sizes, and slow speeds for an organic feel */
            .leaf1 { left: 12%; animation-duration: 25s; animation-delay: 0s; transform: scale(0.8); }
            .leaf2 { left: 45%; animation-duration: 32s; animation-delay: 5s; transform: scale(1.3); }
            .leaf3 { left: 82%; animation-duration: 28s; animation-delay: 12s; transform: scale(0.6); }
            .leaf4 { left: 28%; animation-duration: 35s; animation-delay: 18s; transform: scale(1.0); }
            .leaf5 { left: 65%; animation-duration: 22s; animation-delay: 8s; transform: scale(0.9); }
            
            @keyframes floatUp {
                0% { 
                    bottom: -10%; 
                    opacity: 0; 
                    transform: translateX(0px) rotate(0deg); 
                }
                15% { 
                    opacity: 1; /* Fade in gently */
                }
                85% { 
                    opacity: 1; 
                }
                100% { 
                    bottom: 110%; 
                    opacity: 0; 
                    transform: translateX(-40px) rotate(180deg); /* Gentle drift and spin */
                }
            }
        </style>
        
        <div class="eco-leaf leaf1"></div>
        <div class="eco-leaf leaf2"></div>
        <div class="eco-leaf leaf3"></div>
        <div class="eco-leaf leaf4"></div>
        <div class="eco-leaf leaf5"></div>
        """
        import streamlit as st
        st.markdown(leaf_html, unsafe_allow_html=True)


class CertificateGenerator:

    @staticmethod
    def create_pdf(org_name, score, date):
        pdf = FPDF()
        pdf.add_page()

        pdf.set_fill_color(248, 236, 214)  # Light beige background
        pdf.rect(0, 0, 210, 297, 'F')

        pdf.set_text_color(47, 111, 78)
        pdf.set_font("Arial", 'B', 30)
        pdf.cell(200, 40, "PRAKRIT GREEN BADGE", ln=True, align='C')

        pdf.set_text_color(31, 41, 55)
        pdf.set_font("Arial", '', 16)
        pdf.cell(200, 20, "This is to certify that", ln=True, align='C')

        pdf.set_font("Arial", 'B', 24)
        pdf.cell(200, 20, f"{org_name}", ln=True, align='C')

        pdf.set_font("Arial", 'B', 40)
        pdf.cell(200, 40, f"{score}/10", ln=True, align='C')

        pdf.set_font("Arial", 'I', 12)
        pdf.cell(200, 10, f"Verified on: {date}", ln=True, align='C')

        return pdf.output(dest='S').encode('latin-1')

    


    