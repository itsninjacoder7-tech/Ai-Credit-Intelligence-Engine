import streamlit as st
import os
import pandas as pd
import pickle
import numpy as np
import hashlib
import re
import time
import io

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="LoanSahayak — Smart Loan Intelligence",
    page_icon="🏦",
    layout="wide"
)

# -----------------------------------
# USER DATABASE FUNCTIONS
# -----------------------------------
USER_FILE = "users.csv"

def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    else:
        return pd.DataFrame(columns=["username", "password"])

def save_user(username, password):
    df = load_users()
    new_user = pd.DataFrame([[username, password]], columns=["username", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_username(username):
    return re.match(r"^[a-zA-Z0-9_.]{4,20}$", username)

def is_valid_password(password):
    return (
        len(password) >= 6 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password)
    )

# -----------------------------------
# SESSION STATE
# -----------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# -----------------------------------
# PREMIUM UI STYLING
# -----------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --gold: #C9A84C;
    --gold-light: #E8C97A;
    --gold-dim: rgba(201,168,76,0.12);
    --bg-deep: #070B14;
    --bg-card: rgba(255,255,255,0.035);
    --border: rgba(201,168,76,0.2);
    --border-bright: rgba(201,168,76,0.5);
    --text-primary: #EDE8DC;
    --text-secondary: #9A9080;
    --text-muted: #5A5448;
    --success: #2ECC71;
    --danger: #E74C3C;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none; z-index: 0; opacity: 0.4;
}

.main .block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1200px !important;
}

/* ── Hero ── */
.hero-wrap {
    position: relative; text-align: center;
    padding: 72px 40px 60px;
    border-radius: 24px; border: 1px solid var(--border);
    background:
        radial-gradient(ellipse 80% 60% at 50% 0%, rgba(201,168,76,0.08) 0%, transparent 70%),
        linear-gradient(180deg, #0C1525 0%, #070B14 100%);
    overflow: hidden; margin-bottom: 8px;
}
.hero-wrap::after {
    content: ''; position: absolute; top: 0; left: 50%;
    transform: translateX(-50%); width: 60%; height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.hero-badge {
    display: inline-block; padding: 6px 18px;
    border: 1px solid var(--border-bright); border-radius: 100px;
    font-size: 11px; letter-spacing: 2.5px; text-transform: uppercase;
    color: var(--gold); background: var(--gold-dim);
    margin-bottom: 24px; font-weight: 600;
}
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 56px !important; font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin: 0 0 16px !important; line-height: 1.1 !important;
}
.hero-title span { color: var(--gold); }
.hero-sub {
    font-size: 17px; color: var(--text-secondary);
    font-weight: 300; max-width: 520px; margin: 0 auto 28px; line-height: 1.7;
}
.hero-stats {
    display: flex; justify-content: center; gap: 48px;
    margin-top: 36px; padding-top: 28px; border-top: 1px solid var(--border);
}
.hero-stat-val {
    font-family: 'Playfair Display', serif;
    font-size: 28px; font-weight: 600; color: var(--gold-light);
}
.hero-stat-label {
    font-size: 11px; letter-spacing: 1.5px;
    text-transform: uppercase; color: var(--text-muted); margin-top: 4px;
}

/* ── Section headers ── */
.section-header {
    display: flex; align-items: center; gap: 12px;
    margin: 36px 0 18px; padding-bottom: 14px; border-bottom: 1px solid var(--border);
}
.section-icon {
    width: 36px; height: 36px; border-radius: 10px;
    background: var(--gold-dim); border: 1px solid rgba(201,168,76,0.3);
    display: flex; align-items: center; justify-content: center; font-size: 16px;
}
.section-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 20px !important; font-weight: 600 !important;
    color: var(--text-primary) !important; margin: 0 !important;
}
.section-desc {
    font-size: 12px; color: var(--text-muted);
    letter-spacing: 1px; text-transform: uppercase; margin-left: auto;
}

/* ── Labels ── */
label, .stSelectbox label, .stNumberInput label,
.stSlider label, [data-testid="stWidgetLabel"] {
    color: var(--text-secondary) !important;
    font-size: 12px !important; letter-spacing: 1px !important;
    text-transform: uppercase !important; font-weight: 500 !important;
    margin-bottom: 6px !important;
}

/* ── Inputs ── */
input[type="number"], .stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important; border-radius: 10px !important;
    color: var(--text-primary) !important; padding: 10px 14px !important;
    font-size: 15px !important; font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s !important;
}
input[type="number"]:focus { border-color: var(--gold) !important; box-shadow: 0 0 0 3px var(--gold-dim) !important; outline: none !important; }
input[type="password"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important; border-radius: 10px !important;
    color: var(--text-primary) !important; padding: 10px 14px !important;
    font-size: 15px !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important; border-radius: 10px !important;
    color: var(--text-primary) !important;
}
.stSelectbox > div > div:focus-within { border-color: var(--gold) !important; box-shadow: 0 0 0 3px var(--gold-dim) !important; }

/* ── Sliders ── */
.stSlider > div > div > div { background: var(--gold) !important; }
.stSlider > div > div > div > div { background: var(--gold) !important; border: 2px solid var(--bg-deep) !important; box-shadow: 0 0 0 2px var(--gold) !important; }
[data-testid="stSlider"] > div > div { background: rgba(255,255,255,0.07) !important; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #C9A84C 0%, #8B6914 100%) !important;
    color: #070B14 !important; border: none !important; border-radius: 12px !important;
    height: 54px !important; font-size: 14px !important; font-weight: 700 !important;
    letter-spacing: 1.5px !important; text-transform: uppercase !important;
    width: 100% !important; font-family: 'DM Sans', sans-serif !important;
    transition: all 0.25s ease !important; box-shadow: 0 4px 24px rgba(201,168,76,0.25) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(201,168,76,0.4) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Radio (Login/Signup tabs) ── */
.stRadio > div { flex-direction: row !important; gap: 12px !important; }
.stRadio > div > label {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important; border-radius: 10px !important;
    padding: 8px 20px !important; cursor: pointer !important;
    color: var(--text-secondary) !important; font-size: 13px !important;
    letter-spacing: 0.5px !important; transition: all 0.2s !important;
    text-transform: none !important;
}
.stRadio > div > label:has(input:checked) {
    background: var(--gold-dim) !important; border-color: rgba(201,168,76,0.5) !important;
    color: var(--gold-light) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important; border: 1px solid var(--border) !important;
    border-radius: 16px !important; padding: 20px 22px !important;
    backdrop-filter: blur(12px) !important; transition: border-color 0.2s !important;
}
[data-testid="metric-container"]:hover { border-color: var(--border-bright) !important; }
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 11px !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { color: var(--text-primary) !important; font-family: 'Playfair Display', serif !important; font-size: 26px !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important; border: 1px solid var(--border) !important;
    border-radius: 12px !important; color: var(--text-secondary) !important;
    font-size: 13px !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.02) !important; border: 1px solid var(--border) !important;
    border-top: none !important; border-radius: 0 0 12px 12px !important;
}

/* ── Alerts ── */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 14px !important; border-left-width: 3px !important;
    font-size: 15px !important; padding: 16px 20px !important;
}

/* ── Progress ── */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--gold), var(--gold-light)) !important; border-radius: 100px !important;
}
.stProgress > div { background: rgba(255,255,255,0.07) !important; border-radius: 100px !important; height: 8px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #070B14 !important; border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown li,
[data-testid="stSidebar"] label { color: var(--text-secondary) !important; font-size: 13px !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: var(--text-primary) !important; font-family: 'Playfair Display', serif !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 28px 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* ── Result cards ── */
.result-approved {
    padding: 32px 36px; border-radius: 20px;
    border: 1px solid rgba(46,204,113,0.3);
    background: radial-gradient(ellipse at top, rgba(46,204,113,0.06) 0%, transparent 70%), rgba(255,255,255,0.025);
    text-align: center;
}
.result-rejected {
    padding: 32px 36px; border-radius: 20px;
    border: 1px solid rgba(231,76,60,0.3);
    background: radial-gradient(ellipse at top, rgba(231,76,60,0.06) 0%, transparent 70%), rgba(255,255,255,0.025);
    text-align: center;
}
.result-icon { font-size: 48px; margin-bottom: 12px; }
.result-label { font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 700; margin: 0 0 8px; }
.result-sub { font-size: 14px; color: var(--text-secondary); letter-spacing: 0.5px; }
.result-conf { display: inline-block; margin-top: 14px; padding: 6px 20px; border-radius: 100px; font-size: 13px; font-weight: 600; letter-spacing: 1px; }
.conf-approved { background: rgba(46,204,113,0.15); color: #2ECC71; border: 1px solid rgba(46,204,113,0.3); }
.conf-rejected { background: rgba(231,76,60,0.15); color: #E74C3C; border: 1px solid rgba(231,76,60,0.3); }
</style>
""", unsafe_allow_html=True)


# -----------------------------------
# PREMIUM AUTH UI
# -----------------------------------
def show_auth():
    # Premium heading
    st.markdown("""
    <div style="
        position: relative;
        text-align: center;
        padding: 44px 40px 36px;
        border-radius: 20px;
        border: 1px solid rgba(201,168,76,0.22);
        background:
            radial-gradient(ellipse 80% 50% at 50% 0%, rgba(201,168,76,0.1) 0%, transparent 65%),
            linear-gradient(180deg, #0C1525 0%, #080C18 100%);
        overflow: hidden;
        margin-bottom: 28px;
    ">
        <!-- Top gold line -->
        <div style="
            position: absolute; top: 0; left: 50%; transform: translateX(-50%);
            width: 60%; height: 1px;
            background: linear-gradient(90deg, transparent, #C9A84C, transparent);
        "></div>

        <!-- Icon ring -->
        <div style="
            width: 66px; height: 66px; border-radius: 50%;
            background: rgba(201,168,76,0.08);
            border: 1px solid rgba(201,168,76,0.38);
            display: flex; align-items: center; justify-content: center;
            margin: 0 auto 20px;
            box-shadow: 0 0 0 6px rgba(201,168,76,0.05);
            font-size: 28px; line-height: 1;
        ">🏦</div>

        <!-- Badge -->
        <div style="
            display: inline-block;
            padding: 4px 16px;
            border: 1px solid rgba(201,168,76,0.42);
            border-radius: 100px;
            font-size: 10px; letter-spacing: 3px;
            text-transform: uppercase;
            color: #C9A84C;
            background: rgba(201,168,76,0.08);
            margin-bottom: 18px;
            font-family: 'DM Sans', sans-serif;
            font-weight: 600;
        ">✦ Smart Loan Intelligence</div>

        <!-- Title -->
        <div style="
            font-family: 'Playfair Display', serif;
            font-size: 48px; font-weight: 700;
            color: #EDE8DC;
            line-height: 1.05; letter-spacing: -0.5px;
            margin-bottom: 4px;
        ">Loan<em style="color: #C9A84C; font-weight: 400; font-style: italic;">Sahayak</em></div>

        <!-- Gold rule -->
        <div style="
            width: 52px; height: 1px;
            background: linear-gradient(90deg, transparent, #C9A84C, transparent);
            margin: 14px auto;
        "></div>

        <!-- Subtitle -->
        <div style="
            font-family: 'DM Sans', sans-serif;
            font-size: 12px; letter-spacing: 2.5px;
            text-transform: uppercase; color: #6A6058;
            margin-bottom: 6px;
        ">AI-Powered Credit Analysis</div>

        <div style="font-family:'DM Sans',sans-serif; font-size:14px; color:#7A7060; font-weight:300;">
            Sophisticated lending decisions, engineered for modern finance.
        </div>

        <!-- Decorative dots -->
        <div style="display:flex; justify-content:center; gap:6px; margin-top:18px;">
            <div style="width:4px;height:4px;border-radius:50%;background:#C9A84C;"></div>
            <div style="width:4px;height:4px;border-radius:50%;background:rgba(201,168,76,0.35);"></div>
            <div style="width:4px;height:4px;border-radius:50%;background:rgba(201,168,76,0.15);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    choice = st.radio("", ["Login", "Signup"], horizontal=True, label_visibility="collapsed")
    users = load_users()

    if choice == "Login":
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        if st.button("Login →"):
            if not username or not password:
                st.warning("Please enter both fields.")
            else:
                user = users[
                    (users["username"] == username) &
                    (users["password"] == hash_password(password))
                ]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    else:
        new_user    = st.text_input("Create Username", placeholder="4–20 chars (letters, numbers, _ .)")
        new_pass    = st.text_input("Create Password", type="password", placeholder="Uppercase + lowercase + number")
        confirm_pass = st.text_input("Confirm Password", type="password", placeholder="Repeat your password")

        if st.button("Create Account →"):
            if not new_user or not new_pass:
                st.warning("Fields cannot be empty.")
            elif not is_valid_username(new_user):
                st.error("Username must be 4–20 chars (letters, numbers, _ . only).")
            elif not is_valid_password(new_pass):
                st.error("Password must have uppercase, lowercase & a number.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            elif new_user.lower() in users["username"].str.lower().values:
                st.warning("Username already exists.")
            else:
                save_user(new_user, hash_password(new_pass))
                st.success("Account created! Please login.")


# -----------------------------------
# LOGIN GATE
# -----------------------------------
if not st.session_state.logged_in:
    col_auth_l, col_auth_m, col_auth_r = st.columns([1, 1.4, 1])
    with col_auth_m:
        show_auth()
    st.stop()


# -----------------------------------
# WELCOME BANNER (post-login)
# -----------------------------------
st.markdown(f"""
<div style="
    padding: 14px 20px; border-radius: 12px;
    background: rgba(201,168,76,0.08); border: 1px solid rgba(201,168,76,0.28);
    color: #E8C97A; font-size: 16px; margin-bottom: 18px;
">
    👋 Welcome!! <b>{st.session_state.username}</b> — System status: Active.
    LoanSahayak is ready to transform your data into definitive financial insights.
</div>
""", unsafe_allow_html=True)


# -----------------------------------
# HERO
# -----------------------------------
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">✦ AI-Powered Lending Intelligence</div>
    <div class="hero-title">Loan<span>Sahayak</span></div>
    <div class="hero-sub">
        Sophisticated credit analysis and risk assessment — engineered for modern lending decisions.
    </div>
    <div class="hero-stats">
        <div><div class="hero-stat-val">83.4%</div><div class="hero-stat-label">Accuracy</div></div>
        <div><div class="hero-stat-val">&lt; 2s</div><div class="hero-stat-label">Decision Time</div></div>
        <div><div class="hero-stat-val">16+</div><div class="hero-stat-label">Risk Factors</div></div>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.markdown("""
<div style="padding:8px 0 20px; border-bottom:1px solid rgba(201,168,76,0.2); margin-bottom:20px;">
    <div style="font-family:'Playfair Display',serif; font-size:22px; color:#F0EBE0; font-weight:700;">LoanSahayak</div>
    <div style="font-size:11px; letter-spacing:2px; text-transform:uppercase; color:#9A9080; margin-top:4px;">Smart Loan Intelligence</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="padding:16px; border-radius:14px; background:rgba(59,130,246,0.08);
    border:1px solid rgba(59,130,246,0.2); color:#9CCBFF; font-size:14px; line-height:1.6;">
AI-powered system that evaluates loan applications using:<br>
• Financial indicators<br>
• Credit score analysis<br>
• Multi-factor risk assessment
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="font-size:12px; color:#9A9080; letter-spacing:1px; text-transform:uppercase; margin-bottom:6px;">System Stats</div>
<div style="font-size:14px; color:#F0EBE0; line-height:1.8;">
✔ Accuracy: <span style="color:#C9A84C;">83.4%</span><br>
✔ Decision Time: <span style="color:#C9A84C;">&lt; 2s</span><br>
✔ Risk Factors: <span style="color:#C9A84C;">16+</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<hr style='border-color:rgba(201,168,76,0.2); margin:18px 0;'>", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="font-family:'Playfair Display',serif; font-size:20px; color:#F0EBE0; font-weight:600;">👤 Project Author</div>
<div style="margin-top:10px; font-size:16px; color:#F0EBE0; font-weight:500;">Arnav Singh</div>
<div style="font-size:13px; color:#9A9080; margin-top:4px;">Machine Learning Enthusiast | Aspiring Data Scientist</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

sb1, sb2, sb3 = st.sidebar.columns(3, gap="small")
with sb1:
    st.markdown("""<div style="display:flex;justify-content:center;">
        <a href="https://www.linkedin.com/in/arnav-singh-a87847351" target="_blank">
        <div style="display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;
            background:rgba(78,161,255,0.08);border:1px solid rgba(78,161,255,0.2);">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="#4EA1FF">
        <path d="M4.98 3.5C4.98 4.88 3.87 6 2.49 6S0 4.88 0 3.5 1.11 1 2.49 1 4.98 2.12 4.98 3.5zM.22 8.98H4.75V24H.22V8.98zm7.76 0h4.34v2.06h.06c.66-1.18 2.28-2.41 4.66-2.41 5.04 0 5.96 3.25 5.96 7.5V24h-4.53v-6.79c0-1.75-.03-4.01-2.45-4.01-2.46 0-2.84 1.86-2.84 3.88V24H7.98V8.98z"/>
        </svg></div></a></div>""", unsafe_allow_html=True)
with sb2:
    st.markdown("""<div style="display:flex;justify-content:center;">
        <a href="mailto:itsarnav.singh80@gmail.com">
        <div style="display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;
            background:rgba(0,255,150,0.08);border:1px solid rgba(0,255,150,0.25);">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="#00FFAA">
        <path d="M2 4a2 2 0 012-2h16a2 2 0 012 2v16a2 2 0 01-2 2H4a2 2 0 01-2-2V4zm2 0v2l8 7 8-7V4L12 11 4 4zm16 4l-8 7-8-7v12h16V8z"/>
        </svg></div></a></div>""", unsafe_allow_html=True)
with sb3:
    st.markdown("""<div style="display:flex;justify-content:center;">
        <a href="https://github.com/Arnav-Singh-5080" target="_blank">
        <div style="display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;
            background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.15);">
        <svg height="18" width="18" viewBox="0 0 16 16" fill="#4EA1FF">
        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.6.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-.46-1.34-.46-1.34-.1-.26-.5-1.02-.5-1.02-.4-.28.03-.27.03-.27.44.03.68.45.68.45.4.69.98.52.22.38-.09-.29-.12-.56-.04-.79C6.88 11 5 10.13 5 7.13c0-.86.31-1.56.82-2.11-.08-.2-.36-1 .08-2.08 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.03 2.2-.82 2.2-.82.44 1.08.16 1.88.08 2.08.51.55.82 1.25.82 2.11 0 3.01-1.88 3.67-3.67 3.89.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
        </svg></div></a></div>""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="font-size:12px; color:#5A5448; text-align:center;">⭐ Star this project on GitHub</div>
""", unsafe_allow_html=True)


# -----------------------------------
# LOAD MODEL
# -----------------------------------
model_path = os.path.join(os.path.dirname(__file__), 'models', 'loan_model.pkl')
model = pickle.load(open(model_path, "rb"))

scaler_path = os.path.join(os.path.dirname(__file__), 'models', 'scaler.pkl')
scaler = pickle.load(open(scaler_path, "rb"))

try:
    model  = pickle.load(open(model_path, "rb"))
    scaler = pickle.load(open(scaler_path, "rb"))
except FileNotFoundError:
    st.error("### ⚠️ Model Files Not Found")
    st.info("""
    The required AI models (**loan_model.pkl** and **scaler.pkl**) are missing from the `models/` directory.

    **How to fix:**
    1. Place the `.pkl` files in the `models/` folder.
    2. Refer to `docs/setup.md` for detailed instructions.
    """)
    st.stop()


# -----------------------------------
# EMI CALCULATOR
# -----------------------------------
def calculate_emi(principal, tenure_months, annual_rate=10):
    if principal == 0 or tenure_months == 0:
        return 0
    mr = annual_rate / 12 / 100
    return (principal * mr * (1 + mr)**tenure_months) / ((1 + mr)**tenure_months - 1)


# -----------------------------------
# SECTION: FINANCIAL PROFILE
# -----------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-icon">💼</div>
    <div class="section-title">Financial Profile</div>
    <div class="section-desc">Income & Loan Details</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")
with col1:
    applicant_income   = st.number_input("Applicant Income (₹)",   min_value=0, step=1000)
    coapplicant_income = st.number_input("Coapplicant Income (₹)", min_value=0, step=1000)
    loan_amount        = st.number_input("Loan Amount (₹)",        min_value=0, step=1000)
    savings            = st.number_input("Savings (₹)",            min_value=0, step=1000)
with col2:
    collateral_value = st.number_input("Collateral Value (₹)", min_value=0, step=1000)
    dependents       = st.number_input("Number of Dependents",  min_value=0)
    existing_loans   = st.number_input("Existing Active Loans", min_value=0)

col3, col4 = st.columns(2, gap="large")
with col3:
    credit_score = st.slider("Credit Score",        300, 900, 650)
with col4:
    loan_term    = st.slider("Loan Term (Months)",   6, 360,  60)

col5, _ = st.columns([1, 1], gap="large")
with col5:
    age = st.slider("Applicant Age", 18, 70, 30)


# -----------------------------------
# SECTION: APPLICANT BACKGROUND
# -----------------------------------
st.markdown("""
<div class="section-header" style="margin-top:44px;">
    <div class="section-icon">👤</div>
    <div class="section-title">Applicant Background</div>
    <div class="section-desc">Demographic & Employment</div>
</div>
""", unsafe_allow_html=True)

col6, col7 = st.columns(2, gap="large")
with col6:
    employment_dict   = {"Unemployed": 0, "Salaried": 1, "Self-Employed": 2}
    employment_status = employment_dict[st.selectbox("Employment Status", list(employment_dict.keys()))]

    property_dict = {"Rural": 0, "Semi-Urban": 1, "Urban": 2}
    property_area = property_dict[st.selectbox("Property Area", list(property_dict.keys()))]

    loan_purpose_dict = {"Home Loan": 0, "Car Loan": 1, "Education Loan": 2, "Personal Loan": 3}
    loan_purpose      = loan_purpose_dict[st.selectbox("Loan Purpose", list(loan_purpose_dict.keys()))]

with col7:
    education_dict  = {"Not Graduate": 0, "Graduate": 1}
    education_level = education_dict[st.selectbox("Education Level", list(education_dict.keys()))]

    gender_dict = {"Female": 0, "Male": 1}
    gender      = gender_dict[st.selectbox("Gender", list(gender_dict.keys()))]

    employer_dict     = {"Private Sector": 0, "Government": 1, "Business Owner": 2}
    employer_category = employer_dict[st.selectbox("Employer Category", list(employer_dict.keys()))]


# -----------------------------------
# ANALYSE BUTTON
# -----------------------------------
st.markdown("<div style='margin-top:36px;'></div>", unsafe_allow_html=True)
col_btn, _, _ = st.columns([1.2, 1, 1])
with col_btn:
    run = st.button("⬡  Analyse Loan Application")


# -----------------------------------
# PREDICTION
# -----------------------------------
if run:
    if applicant_income == 0 or loan_amount == 0:
        st.error("⚠ Income and Loan Amount must be greater than zero.")
        st.stop()

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.enums import TA_CENTER

    # Processing animation
    progress_bar = st.progress(0)
    status_text  = st.empty()

    steps = [
        "🔍 Collecting financial data...",
        "📊 Analyzing income & liabilities...",
        "🧠 Running ML model inference...",
        "⚖️ Evaluating risk parameters...",
        "✅ Finalizing decision...",
    ]
    for i, step in enumerate(steps):
        status_text.markdown(f"<span style='color:#C9A84C;font-family:DM Sans,sans-serif;'>{step}</span>", unsafe_allow_html=True)
        progress_bar.progress((i + 1) * 20)
        time.sleep(0.4)

    status_text.empty()
    progress_bar.empty()

    # ── Core calculations ──
    total_income = applicant_income + coapplicant_income
    emi          = calculate_emi(loan_amount, loan_term)
    emi_ratio    = emi / total_income if total_income > 0 else 0

    # ── Application summary expander ──
    with st.expander("📋 Application Summary"):
        s1, s2, s3 = st.columns(3)
        s1.metric("Total Household Income", f"₹{total_income:,}")
        s2.metric("Loan Amount Requested",  f"₹{loan_amount:,}")
        s3.metric("Credit Score",           credit_score)

    # ── Model prediction ──
    input_data = pd.DataFrame([[
        applicant_income, coapplicant_income, loan_amount, credit_score,
        age, dependents, existing_loans, savings, collateral_value,
        loan_term, employment_status, property_area, loan_purpose,
        education_level, gender, employer_category
    ]], columns=[
        'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount', 'Credit_Score',
        'Age', 'Dependents', 'Existing_Loans', 'Savings', 'Collateral_Value',
        'Loan_Term', 'Employment_Status', 'Property_Area', 'Loan_Purpose',
        'Education_Level', 'Gender', 'Employer_Category'
    ])

    scaled_data   = scaler.transform(input_data)
    prediction    = model.predict(scaled_data)
    probability   = model.predict_proba(scaled_data)
    approval_prob = probability[0][1] * 100

    st.markdown("---")

    # ── Financial analysis ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <div class="section-title">Financial Analysis</div>
    </div>
    """, unsafe_allow_html=True)

    mA, mB, mC = st.columns(3)
    mA.metric("Monthly EMI",         f"₹ {round(emi, 2):,}")
    mB.metric("Total Monthly Income", f"₹ {total_income:,}")
    mC.metric("EMI / Income Ratio",  f"{round(emi_ratio * 100, 2)} %")

    # ── Approval probability bar ──
    st.markdown("---")
    st.progress(int(approval_prob))
    st.markdown(f"**Approval Probability: {round(approval_prob, 1)}%**")
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Risk indicators ──
    if emi_ratio > 0.5:
        st.warning("⚠ High EMI ratio — exceeds 50% of monthly income")
    elif credit_score < 600:
        st.warning("⚠ Low credit score — below 600 threshold")
    else:
        st.info("✓ Stable profile — no major risk flags detected")

    # ── Decision ──
    decision_text = "APPROVED" if prediction[0] == 1 else "REJECTED"

    if prediction[0] == 1:
        st.markdown(f"""
        <div class="result-approved">
            <div class="result-icon">✅</div>
            <div class="result-label" style="color:#2ECC71;">{decision_text}</div>
            <div class="result-sub">Your application meets our lending criteria</div>
            <div class="result-conf conf-approved">Confidence: {round(approval_prob, 2)}%</div>
        </div>
        """, unsafe_allow_html=True)
        reasons = []
    else:
        st.markdown(f"""
        <div class="result-rejected">
            <div class="result-icon">❌</div>
            <div class="result-label" style="color:#E74C3C;">{decision_text}</div>
            <div class="result-sub">This application does not meet current lending criteria</div>
            <div class="result-conf conf-rejected">Confidence: {round(100 - approval_prob, 2)}%</div>
        </div>
        """, unsafe_allow_html=True)

        # Build rejection reasons
        reasons = []
        if total_income < 25000:
            reasons.append("Total household income is below the recommended threshold (₹25,000).")
        if emi_ratio > 0.5:
            reasons.append("EMI to income ratio is too high (greater than 50%).")
        if credit_score < 600:
            reasons.append("Credit score is below the acceptable limit (600).")
        if existing_loans > 3:
            reasons.append("Too many active loans already.")
        if collateral_value < loan_amount * 0.5:
            reasons.append("Collateral value is insufficient for the requested loan.")

        if reasons:
            st.markdown("""
            <div class="section-header">
                <div class="section-icon">⚠️</div>
                <div class="section-title">Possible Reasons for Rejection</div>
                <div class="section-desc">Key Risk Factors</div>
            </div>
            """, unsafe_allow_html=True)
            for reason in reasons:
                st.write(f"• {reason}")
        else:
            st.write("The application does not meet the bank approval criteria.")

    # ── PDF Report ──
    pdf_buffer = io.BytesIO()
    doc    = SimpleDocTemplate(pdf_buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                  alignment=TA_CENTER, textColor=colors.HexColor("#C9A84C"))
    section_style = ParagraphStyle('Heading', parent=styles['Heading2'],
                                    textColor=colors.HexColor("#3B82F6"))

    content = []
    content.append(Paragraph("LoanSahayak", title_style))
    content.append(Spacer(1, 6))
    content.append(Paragraph("AI Loan Analysis Report", styles["Italic"]))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Financial Summary", section_style))
    content.append(Spacer(1, 10))
    table = Table([
        ["Metric", "Value"],
        ["Total Income",  f"Rs. {total_income:,}"],
        ["Loan Amount",   f"Rs. {loan_amount:,}"],
        ["Loan Term",     f"{loan_term} months"],
        ["EMI",           f"Rs. {round(emi, 2)}"],
    ])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#C9A84C")),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    content.append(table)
    content.append(Spacer(1, 20))

    content.append(Paragraph("Credit Profile", section_style))
    content.append(Spacer(1, 10))
    table2 = Table([
        ["Credit Score",   credit_score],
        ["Dependents",     dependents],
        ["Existing Loans", existing_loans],
    ])
    table2.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.grey)]))
    content.append(table2)
    content.append(Spacer(1, 20))

    decision_color = colors.green if prediction[0] == 1 else colors.red
    decision_style = ParagraphStyle('Decision', parent=styles['Heading1'],
                                     alignment=TA_CENTER, textColor=decision_color)
    content.append(Paragraph(decision_text, decision_style))
    content.append(Spacer(1, 10))

    confidence = round(approval_prob, 2) if prediction[0] == 1 else round(100 - approval_prob, 2)
    label      = "Approval Confidence" if prediction[0] == 1 else "Rejection Confidence"
    content.append(Paragraph(f"{label}: {confidence}%", styles["Normal"]))
    content.append(Spacer(1, 20))

    if prediction[0] == 0 and reasons:
        content.append(Paragraph("Reasons for Rejection", section_style))
        content.append(Spacer(1, 10))
        for r in reasons:
            content.append(Paragraph(f"• {r}", styles["Normal"]))
        content.append(Spacer(1, 20))

    content.append(Paragraph("Generated by LoanSahayak AI", styles["Italic"]))
    doc.build(content)
    pdf_buffer.seek(0)

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_buffer,
        file_name="LoanSahayak_Report.pdf",
        mime="application/pdf",
    )


# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("""
<div style="
    margin-top:100px; padding:28px 32px; border-radius:16px;
    border:1px solid rgba(201,168,76,0.12); background:rgba(255,255,255,0.02);
    display:flex; justify-content:space-between; align-items:center;
    font-size:12px; letter-spacing:1px; color:#5A5448;
">
    <div>© 2026 <span style="color:#C9A84C;">LoanSahayak</span> — All Rights Reserved</div>
    <div style="text-transform:uppercase; letter-spacing:2px;">AI · Credit · Intelligence</div>
</div>
""", unsafe_allow_html=True)
