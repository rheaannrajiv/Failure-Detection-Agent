
import streamlit as st
import requests

# ==========================================
# FAILURE DETECTIVE AI
# Intelligent Mechanical Fault Diagnosis
# ==========================================

st.set_page_config(
    page_title="Failure Detective AI",
    page_icon="⚙️",
    layout="wide"
)

# ==========================================
# INDUSTRIAL DASHBOARD THEME
# ==========================================
st.markdown("""
<style>
:root {
    --navy: #071321;
    --panel: #10263b;
    --panel2: #15344c;
    --teal: #43d9c3;
    --text: #eaf2fb;
    --muted: #a8bbce;
    --line: rgba(100, 190, 205, .22);
}
.stApp {
    background:
        radial-gradient(ellipse at 12% 0%, rgba(24, 89, 115, .32), transparent 38%),
        radial-gradient(ellipse at 90% 18%, rgba(43, 70, 125, .20), transparent 35%),
        linear-gradient(135deg, #071321 0%, #0a1727 55%, #0c1b2d 100%);
    color: var(--text);
}
.stApp:before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background-image:
        linear-gradient(rgba(108, 166, 190, .045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(108, 166, 190, .045) 1px, transparent 1px);
    background-size: 32px 32px;
    mask-image: linear-gradient(to bottom, black, transparent 92%);
    animation: blueprint-drift 42s linear infinite;
}
/* Moving ambient light and layered technical atmosphere */
.stApp {
    background-size: 140% 140%, 130% 130%, 100% 100%;
    animation: ambient-shift 24s ease-in-out infinite alternate;
}
/* Decorative orbit rings behind the content */
.stApp:after {
    animation: orbit-breathe 10s ease-in-out infinite alternate;
}
@keyframes blueprint-drift {
    from { background-position: 0 0, 0 0; }
    to { background-position: 96px 64px, 64px 96px; }
}
@keyframes ambient-shift {
    0% { background-position: 0% 0%, 100% 0%, 0% 0%; }
    100% { background-position: 12% 10%, 85% 18%, 0% 0%; }
}
@keyframes orbit-breathe {
    from { transform: scale(.96) rotate(-5deg); opacity: .65; }
    to { transform: scale(1.04) rotate(5deg); opacity: 1; }
}
/* Soft ambient engineering glow */
.stApp:after {
    content: "";
    position: fixed;
    width: 440px;
    height: 440px;
    right: -170px;
    top: 180px;
    border-radius: 50%;
    border: 1px solid rgba(67, 217, 195, .08);
    box-shadow: 0 0 0 34px rgba(67, 217, 195, .018), 0 0 0 78px rgba(67, 217, 195, .014), 0 0 100px rgba(34, 137, 167, .07);
    pointer-events: none;
    z-index: 0;
}
.block-container {
    max-width: 1250px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}
header[data-testid="stHeader"] {
    background: rgba(7, 19, 33, .92) !important;
}
[data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: transparent !important;
}
[data-testid="stBottom"] {
    background: linear-gradient(180deg, rgba(7,19,33,0), rgba(7,19,33,.98) 22%) !important;
}
[data-testid="stChatInput"] > div, [data-testid="stChatInput"] textarea {
    background: #0b1c2d !important;
    color: #eaf2fb !important;
    -webkit-text-fill-color: #eaf2fb !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #8fa8bd !important;
    -webkit-text-fill-color: #8fa8bd !important;
}
h1, h2, h3, h4, p, label, .stMarkdown, .stCaption {
    color: var(--text);
}
h1, h2, h3 {
    letter-spacing: -.025em;
}
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}
[data-testid="stChatMessage"] {
    background: linear-gradient(145deg, rgba(16, 38, 59, .90), rgba(9, 27, 44, .92));
    border: 1px solid rgba(100, 165, 190, .20);
    border-radius: 16px;
    padding: 14px 16px;
    margin: 10px 0;
    box-shadow: 0 10px 24px rgba(0, 0, 0, .10);
}
[data-testid="stChatInput"] {
    border: 1px solid rgba(67, 217, 195, .42) !important;
    border-radius: 16px !important;
    background: rgba(8, 23, 38, .96) !important;
    box-shadow: 0 0 0 3px rgba(67, 217, 195, .035);
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    border: 0 !important;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1b2b, #071321);
    border-right: 1px solid rgba(100, 165, 190, .16);
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(100, 165, 190, .22) !important;
}
div[data-testid="stAlert"] {
    border: 1px solid rgba(67, 217, 195, .22);
    border-radius: 12px;
    background: rgba(17, 47, 70, .72);
}
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(18, 48, 71, .96), rgba(12, 30, 48, .96));
    border: 1px solid rgba(100, 165, 190, .26);
    border-radius: 16px;
    padding: 18px 18px 14px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, .14);
    min-height: 130px;
}
div[data-testid="stMetric"] label {
    color: var(--muted) !important;
}
div[data-testid="stMetricValue"] {
    color: #f2f8ff !important;
    font-size: 1.35rem;
}
div[data-testid="stForm"], div[data-testid="stExpander"] {
    border: 1px solid rgba(100, 165, 190, .24);
    border-radius: 16px;
    background: rgba(13, 33, 52, .78);
    padding: 16px;
}
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    border-radius: 10px;
    border: 1px solid rgba(67, 217, 195, .52);
    background: linear-gradient(110deg, #147f83, #176b91);
    color: #ffffff;
    font-weight: 650;
    transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
    color: #ffffff;
    border-color: #71f1dd;
    filter: brightness(1.12);
    transform: translateY(-1px);
    box-shadow: 0 8px 22px rgba(31, 190, 178, .18);
}
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background: rgba(8, 23, 38, .88);
    border-color: rgba(100, 165, 190, .36);
    border-radius: 10px;
}
input, textarea {
    color: var(--text) !important;
    background-color: #081726 !important;
    -webkit-text-fill-color: var(--text) !important;
    caret-color: var(--teal);
}
textarea {
    background: #081726 !important;
    border: 1px solid rgba(100, 165, 190, .36) !important;
    border-radius: 10px !important;
}
hr {
    border-color: rgba(119, 164, 190, .22);
}
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #1e9caa, #43d9c3);
}
@keyframes gear-turn { to { transform: rotate(360deg); } }
@keyframes gear-turn-reverse { to { transform: rotate(-360deg); } }
.gear {
    display: inline-block;
    transform-origin: center;
    color: #65e8d5;
    text-shadow: 0 0 22px rgba(67, 217, 195, .25);
}
.gear-main { animation: gear-turn 22s linear infinite; }
.gear-small { animation: gear-turn-reverse 14s linear infinite; }
/* Glass-like panels and a subtle luminous edge */
[data-testid="stChatMessage"] {
    background: linear-gradient(135deg, rgba(16,38,59,.82), rgba(10,26,42,.78)) !important;
    border: 1px solid rgba(91,170,195,.20) !important;
    border-radius: 16px !important;
    padding: 14px 16px !important;
    box-shadow: 0 10px 28px rgba(0,0,0,.12);
}
[data-testid="stChatInput"] > div {
    border: 1px solid rgba(67,217,195,.42) !important;
    border-radius: 16px !important;
    box-shadow: 0 0 0 1px rgba(67,217,195,.04), 0 12px 32px rgba(0,0,0,.20) !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #147f83, #176b91) !important;
    border-radius: 10px !important;
}
/* Decorative technical scan line */
@keyframes scan-glide {
    0% { transform: translateX(-110%); opacity: 0; }
    12% { opacity: .45; }
    88% { opacity: .45; }
    100% { transform: translateX(110%); opacity: 0; }
}
.hero-scan {
    position: absolute; left: 0; right: 0; top: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(67,217,195,.75), transparent);
    animation: scan-glide 8s ease-in-out infinite; pointer-events: none;
}
/* Chat-first workspace: keep the composer inside the page, not in Streamlit's fixed white footer */
[data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
    background: transparent !important;
    box-shadow: none !important;
    border-top: 0 !important;
}
[data-testid="stChatInput"] {
    position: static !important;
    background: rgba(8, 23, 38, .96) !important;
    border: 1px solid rgba(67, 217, 195, .55) !important;
    border-radius: 16px !important;
}
/* Layered visual atmosphere and stronger panels */
[data-testid="stMainBlockContainer"] { position: relative; z-index: 1; }
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-left: 3px solid rgba(67,217,195,.75) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-left: 3px solid rgba(74,155,225,.75) !important;
}
.suggestion-label {
    color: #43d9c3; font-size: 10px; font-weight: 800;
    letter-spacing: 2px; text-transform: uppercase; margin: 8px 0 10px;
}
/* Slow, subtle animated technical traces */
@keyframes trace-pulse { 0%,100% { opacity:.18; } 50% { opacity:.55; } }
@keyframes particle-float {
    0%,100% { transform: translate3d(0,0,0); opacity:.25; }
    50% { transform: translate3d(12px,-18px,0); opacity:.8; }
}
@keyframes orbit-spin { to { transform: rotate(360deg); } }
@keyframes core-pulse { 0%,100% { box-shadow:0 0 18px rgba(67,217,195,.10); } 50% { box-shadow:0 0 42px rgba(67,217,195,.28); } }
.stApp:before { animation: blueprint-drift 42s linear infinite, trace-pulse 7s ease-in-out infinite; }
.stApp:after { animation: orbit-breathe 10s ease-in-out infinite alternate; }
.hero-visual { position:relative; width:132px; height:132px; flex:0 0 132px; display:flex; align-items:center; justify-content:center; margin:0 10px; }
.hero-visual .orbit { position:absolute; inset:8px; border:1px solid rgba(67,217,195,.36); border-radius:50%; animation:orbit-spin 24s linear infinite; }
.hero-visual .orbit:before { content:''; position:absolute; width:8px; height:8px; top:8px; left:16px; border-radius:50%; background:#43d9c3; box-shadow:0 0 16px #43d9c3; }
.hero-visual .orbit-two { inset:-3px; border-style:dashed; opacity:.4; animation:orbit-spin 36s linear infinite reverse; }
.hero-visual .core { width:74px; height:74px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#eaf7ff; font-size:43px; background:radial-gradient(circle,rgba(67,217,195,.16),rgba(10,28,45,.4)); border:1px solid rgba(67,217,195,.32); animation:core-pulse 4s ease-in-out infinite; }
.hero-visual .spark { position:absolute; width:4px; height:4px; border-radius:50%; background:#b8fff3; box-shadow:0 0 12px #43d9c3; animation:particle-float 5s ease-in-out infinite; }
.hero-visual .spark-a { top:5px; right:20px; } .hero-visual .spark-b { bottom:14px; left:9px; animation-delay:1.5s; }
@media (max-width: 800px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 1rem; }
}
@media (prefers-reduced-motion: reduce) {
    .gear-main, .gear-small, .hero-visual .orbit, .hero-visual .core, .hero-visual .spark { animation: none; }
    .stApp, .stApp:before, .stApp:after, .hero-scan { animation: none !important; }
    * { scroll-behavior: auto !important; transition: none !important; }
}

/* FULL-PAGE BACKGROUND FIX: keep the animated technical backdrop behind every section */
html, body, [data-testid="stApp"], .stApp,
[data-testid="stAppViewContainer"], [data-testid="stMain"],
section.main, [data-testid="stMainBlockContainer"] {
    background-color: #071321 !important;
}
[data-testid="stAppViewContainer"], [data-testid="stMain"], section.main {
    background: transparent !important;
}
.stApp {
    min-height: 100vh !important;
    isolation: isolate;
    background-image:
        radial-gradient(ellipse at 10% 12%, rgba(18, 102, 125, .28), transparent 42%),
        radial-gradient(ellipse at 92% 34%, rgba(48, 68, 135, .23), transparent 38%),
        radial-gradient(ellipse at 54% 100%, rgba(12, 83, 96, .16), transparent 48%),
        linear-gradient(135deg, #061321 0%, #0a1b2c 52%, #091526 100%) !important;
    background-size: 150% 150%, 145% 145%, 130% 130%, 100% 100% !important;
    animation: ambient-shift 24s ease-in-out infinite alternate;
}
.stApp:before {
    content: "" !important;
    position: fixed !important;
    inset: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    pointer-events: none !important;
    z-index: -1 !important;
    opacity: .62 !important;
    background-image:
        linear-gradient(rgba(108, 190, 210, .065) 1px, transparent 1px),
        linear-gradient(90deg, rgba(108, 190, 210, .065) 1px, transparent 1px),
        radial-gradient(circle at 18% 24%, rgba(67,217,195,.13) 0 1px, transparent 2px),
        radial-gradient(circle at 78% 62%, rgba(67,217,195,.11) 0 1px, transparent 2px) !important;
    background-size: 34px 34px, 34px 34px, 180px 180px, 230px 230px !important;
    mask-image: none !important;
    animation: blueprint-drift 42s linear infinite, trace-pulse 7s ease-in-out infinite !important;
}
.stApp:after {
    content: "" !important;
    position: fixed !important;
    width: min(46vw, 560px) !important;
    height: min(46vw, 560px) !important;
    right: -190px !important;
    top: 24vh !important;
    border-radius: 50% !important;
    border: 1px solid rgba(67,217,195,.10) !important;
    box-shadow: 0 0 0 38px rgba(67,217,195,.025), 0 0 0 92px rgba(67,217,195,.018), inset 0 0 80px rgba(34,137,167,.035) !important;
    pointer-events: none !important;
    z-index: -1 !important;
    animation: orbit-breathe 12s ease-in-out infinite alternate !important;
}
[data-testid="stHeader"] {
    background: rgba(6, 19, 33, .88) !important;
}
[data-testid="stBottom"] {
    background: linear-gradient(180deg, rgba(7,19,33,0), rgba(7,19,33,.94) 30%) !important;
}
@media (prefers-reduced-motion: reduce) {
    .stApp, .stApp:before, .stApp:after { animation: none !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:26px 30px;border-radius:22px;border:1px solid rgba(91,170,195,.42);background:linear-gradient(115deg,rgba(13,35,54,.98),rgba(21,57,80,.96));box-shadow:0 22px 58px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.04);margin:0 0 18px 0;position:relative;overflow:hidden;">
<div class="hero-scan"></div>
<div style="height:3px;background:linear-gradient(90deg,#43d9c3,#2589a7,transparent);position:absolute;top:0;left:0;right:0;"></div>
<div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;">
<div style="font-size:54px;line-height:1;white-space:nowrap;"><span class="gear gear-main">⚙</span><span class="gear gear-small" style="font-size:30px;vertical-align:top;margin-left:-8px;">⚙</span></div>
<div style="min-width:240px;flex:1;">
<div style="font-size:12px;letter-spacing:3px;font-weight:800;color:#43d9c3;margin-bottom:10px;">MECHANICAL ENGINEERING&nbsp; · &nbsp;AI DIAGNOSTICS</div>
<h1 style="color:#f0f6ff;font-size:clamp(28px,4vw,42px);font-weight:800;line-height:1.12;margin:0;">Failure Detective AI</h1>
<p style="color:#b6c9dc;font-size:17px;margin:10px 0 0 0;">Intelligent Mechanical Fault Diagnosis Agent</p>
</div>
<div class="hero-visual" aria-hidden="true"><div class="orbit"></div><div class="orbit orbit-two"></div><div class="core">⚙</div><span class="spark spark-a"></span><span class="spark spark-b"></span></div>
<div style="border:1px solid rgba(67,217,195,.32);background:rgba(67,217,195,.07);border-radius:12px;padding:12px 15px;color:#bfeee7;font-size:11px;letter-spacing:1.2px;font-weight:700;">LOCAL AI<br>DIAGNOSTIC COPILOT</div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex;gap:10px;flex-wrap:wrap;margin:0 0 18px 2px;">
  <span style="font-size:11px;letter-spacing:1.4px;color:#8de8dc;border:1px solid rgba(67,217,195,.24);background:rgba(67,217,195,.06);padding:7px 10px;border-radius:999px;">● LOCAL AI · OLLAMA</span>
  <span style="font-size:11px;letter-spacing:1.4px;color:#b7cde0;border:1px solid rgba(120,170,195,.22);background:rgba(120,170,195,.05);padding:7px 10px;border-radius:999px;">18 FAILURE MODES</span>
  <span style="font-size:11px;letter-spacing:1.4px;color:#b7cde0;border:1px solid rgba(120,170,195,.22);background:rgba(120,170,195,.05);padding:7px 10px;border-radius:999px;">EVIDENCE-LED DIAGNOSIS</span>
</div>
""", unsafe_allow_html=True)


# Each failure has known symptoms and inspection checks.
FAILURES = {
    "Shaft Misalignment": {
        "symptoms": [
            "axial vibration",
            "coupling problems",
            "excessive vibration"
        ],
        "checks": [
            "Check shaft alignment",
            "Inspect coupling condition"
        ]
    },
    "Bearing Damage": {
        "symptoms": [
            "abnormal noise",
            "excessive vibration",
            "high bearing temperature"
        ],
        "checks": [
            "Inspect bearing condition",
            "Check vibration measurements"
        ]
    },
    "Rotor Imbalance": {
        "symptoms": [
            "speed-dependent vibration",
            "excessive vibration"
        ],
        "checks": [
            "Measure vibration at different speeds",
            "Inspect rotor balance"
        ]
    },
    "Inadequate Lubrication": {
        "symptoms": [
            "high bearing temperature",
            "lubrication problems",
            "abnormal noise"
        ],
        "checks": [
            "Check lubricant level and condition",
            "Inspect lubrication system"
        ]
    },
    "Mechanical Looseness": {
        "symptoms": [
            "excessive vibration",
            "loose mounting",
            "abnormal noise"
        ],
        "checks": [
            "Inspect mounting bolts",
            "Check foundation and fasteners"
        ]
    },
    "Cooling Problems": {
        "symptoms": [
            "motor overheating",
            "restricted airflow",
            "high operating temperature"
        ],
        "checks": [
            "Inspect cooling passages",
            "Check fan operation and airflow"
        ]
    },
    "Gear Tooth Damage": {
        "symptoms": [
            "gearbox noise",
            "abnormal vibration",
            "metal particles in lubricant"
        ],
        "checks": [
            "Inspect gear teeth",
            "Check gearbox lubricant for metal particles"
        ]
    },
    "Belt Slippage": {
        "symptoms": [
            "belt squealing",
            "reduced driven speed",
            "belt overheating"
        ],
        "checks": [
            "Inspect belt tension",
            "Inspect belt wear and pulley alignment"
        ]
    },
    "Chain Wear": {
        "symptoms": [
            "chain noise",
            "chain elongation",
            "irregular chain movement"
        ],
        "checks": [
            "Measure chain elongation",
            "Inspect chain links and sprockets"
        ]
    },
    "Pump Cavitation": {
        "symptoms": [
            "crackling pump noise",
            "fluctuating flow",
            "pump vibration"
        ],
        "checks": [
            "Check pump suction pressure",
            "Inspect impeller for cavitation damage"
        ]
    },
    "Pump Blockage": {
        "symptoms": [
            "low flow rate",
            "high discharge pressure",
            "reduced pump output"
        ],
        "checks": [
            "Inspect suction strainer and inlet",
            "Check discharge line for blockage"
        ]
    },
    "Seal Failure": {
        "symptoms": [
            "fluid leakage",
            "pressure loss",
            "seal overheating"
        ],
        "checks": [
            "Inspect mechanical seal",
            "Check seal flushing and operating conditions"
        ]
    },
    "Motor Electrical Fault": {
        "symptoms": [
            "unbalanced motor current",
            "motor electrical noise",
            "motor overheating"
        ],
        "checks": [
            "Measure current in each motor phase",
            "Inspect motor winding insulation"
        ]
    },
    "Motor Overload": {
        "symptoms": [
            "high motor current",
            "motor overheating",
            "reduced motor speed"
        ],
        "checks": [
            "Measure motor current under load",
            "Check driven equipment for excessive load"
        ]
    },
    "Fan or Impeller Damage": {
        "symptoms": [
            "reduced airflow",
            "fan vibration",
            "abnormal fan noise"
        ],
        "checks": [
            "Inspect fan blades or impeller",
            "Measure airflow and check rotation"
        ]
    },
    "Foundation Failure": {
        "symptoms": [
            "foundation cracks",
            "loose anchor bolts",
            "structural vibration"
        ],
        "checks": [
            "Inspect foundation and grout",
            "Check anchor bolts and mounting"
        ]
    },
    "Lubricant Contamination": {
        "symptoms": [
            "cloudy lubricant",
            "lubricant particles",
            "abnormal bearing wear"
        ],
        "checks": [
            "Inspect a lubricant sample",
            "Check lubricant filtration and ingress"
        ]
    },
    "Corrosion or Material Degradation": {
        "symptoms": [
            "visible corrosion",
            "surface pitting",
            "material cracking"
        ],
        "checks": [
            "Inspect the affected surface",
            "Assess material thickness and crack indications"
        ]
    }
}

# A check's outcome adds evidence for or against its
# associated failure. These are simplified prototype rules.
CHECK_TARGETS = {
    "Check shaft alignment": "Shaft Misalignment",
    "Inspect coupling condition": "Shaft Misalignment",
    "Inspect bearing condition": "Bearing Damage",
    "Check vibration measurements": "Bearing Damage",
    "Measure vibration at different speeds": "Rotor Imbalance",
    "Inspect rotor balance": "Rotor Imbalance",
    "Check lubricant level and condition": "Inadequate Lubrication",
    "Inspect lubrication system": "Inadequate Lubrication",
    "Inspect mounting bolts": "Mechanical Looseness",
    "Check foundation and fasteners": "Mechanical Looseness",
    "Inspect cooling passages": "Cooling Problems",
    "Check fan operation and airflow": "Cooling Problems",
    "Inspect gear teeth": "Gear Tooth Damage",
    "Check gearbox lubricant for metal particles": "Gear Tooth Damage",
    "Inspect belt tension": "Belt Slippage",
    "Inspect belt wear and pulley alignment": "Belt Slippage",
    "Measure chain elongation": "Chain Wear",
    "Inspect chain links and sprockets": "Chain Wear",
    "Check pump suction pressure": "Pump Cavitation",
    "Inspect impeller for cavitation damage": "Pump Cavitation",
    "Inspect suction strainer and inlet": "Pump Blockage",
    "Check discharge line for blockage": "Pump Blockage",
    "Inspect mechanical seal": "Seal Failure",
    "Check seal flushing and operating conditions": "Seal Failure",
    "Measure current in each motor phase": "Motor Electrical Fault",
    "Inspect motor winding insulation": "Motor Electrical Fault",
    "Measure motor current under load": "Motor Overload",
    "Check driven equipment for excessive load": "Motor Overload",
    "Inspect fan blades or impeller": "Fan or Impeller Damage",
    "Measure airflow and check rotation": "Fan or Impeller Damage",
    "Inspect foundation and grout": "Foundation Failure",
    "Check anchor bolts and mounting": "Foundation Failure",
    "Inspect a lubricant sample": "Lubricant Contamination",
    "Check lubricant filtration and ingress": "Lubricant Contamination",
    "Inspect the affected surface": "Corrosion or Material Degradation",
    "Assess material thickness and crack indications": "Corrosion or Material Degradation"
}

ALL_SYMPTOMS = sorted({
    symptom
    for failure in FAILURES.values()
    for symptom in failure["symptoms"]
})


# Translate common natural-language descriptions into the symptom labels
# used by the rule-based diagnostic engine. This is intentionally transparent
# and conservative: it identifies possible symptoms, not confirmed faults.
SYMPTOM_KEYWORDS = {
    "axial vibration": ["axial vibration", "vibrating along the shaft", "axial movement"],
    "coupling problems": ["coupling problem", "coupling issue", "coupling", "misaligned coupling"],
    "excessive vibration": ["excessive vibration", "too much vibration", "strong vibration", "vibrating excessively", "heavy vibration"],
    "abnormal noise": ["abnormal noise", "unusual noise", "strange noise", "loud noise", "grinding noise", "noise"],
    "high bearing temperature": ["high bearing temperature", "hot bearing", "bearing overheating"],
    "speed-dependent vibration": ["speed-dependent vibration", "vibration changes with speed", "vibrates at certain speeds"],
    "lubrication problems": ["lubrication problem", "lubrication issue", "poor lubrication", "low lubrication"],
    "loose mounting": ["loose mounting", "loose mount", "loose bolts", "loose mounting bolts"],
    "motor overheating": ["motor overheating", "motor is overheating", "motor gets hot", "motor too hot"],
    "restricted airflow": ["restricted airflow", "blocked airflow", "poor airflow", "airflow restriction"],
    "high operating temperature": ["high operating temperature", "running too hot", "high temperature", "overheating"],
    "gearbox noise": ["gearbox noise", "gear noise", "noisy gearbox", "gearbox is noisy"],
    "abnormal vibration": ["abnormal vibration", "unusual vibration"],
    "metal particles in lubricant": ["metal particles in lubricant", "metal in oil", "metal particles in oil", "metal flakes in lubricant"],
    "belt squealing": ["belt squealing", "squealing belt", "belt squeaks", "belt squeal"],
    "reduced driven speed": ["reduced driven speed", "driven speed is low", "output speed dropped", "speed has dropped"],
    "belt overheating": ["belt overheating", "hot belt", "belt is hot"],
    "chain noise": ["chain noise", "noisy chain", "chain is noisy"],
    "chain elongation": ["chain elongation", "stretched chain", "elongated chain"],
    "irregular chain movement": ["irregular chain movement", "chain jumps", "jerky chain movement"],
    "crackling pump noise": ["crackling pump noise", "pump crackling", "gravel sound in pump", "sounds like gravel", "crackling noise"],
    "fluctuating flow": ["fluctuating flow", "flow fluctuates", "flow is unstable", "inconsistent flow"],
    "pump vibration": ["pump vibration", "pump is vibrating", "pump vibrates"],
    "low flow rate": ["low flow rate", "low flow", "reduced flow", "less water", "flow rate has dropped", "delivering less water", "reduced water delivery"],
    "high discharge pressure": ["high discharge pressure", "discharge pressure is high"],
    "reduced pump output": ["reduced pump output", "pump output is low", "pump output dropped"],
    "fluid leakage": ["fluid leakage", "fluid leak", "leaking fluid", "oil leak", "water leak", "leakage"],
    "pressure loss": ["pressure loss", "pressure dropped", "loss of pressure", "low pressure"],
    "seal overheating": ["seal overheating", "hot seal", "mechanical seal is hot"],
    "unbalanced motor current": ["unbalanced motor current", "current imbalance", "unequal phase current"],
    "motor electrical noise": ["motor electrical noise", "electrical humming", "electrical buzzing"],
    "high motor current": ["high motor current", "motor draws high current", "overcurrent"],
    "reduced motor speed": ["reduced motor speed", "motor speed dropped", "motor running slowly"],
    "reduced airflow": ["reduced airflow", "low airflow", "fan airflow is low"],
    "fan vibration": ["fan vibration", "fan is vibrating", "fan vibrates"],
    "abnormal fan noise": ["abnormal fan noise", "fan noise", "noisy fan"],
    "foundation cracks": ["foundation cracks", "cracked foundation", "cracks in foundation"],
    "loose anchor bolts": ["loose anchor bolts", "anchor bolts are loose"],
    "structural vibration": ["structural vibration", "structure vibrates", "vibration in the frame"],
    "cloudy lubricant": ["cloudy lubricant", "milky oil", "cloudy oil"],
    "lubricant particles": ["lubricant particles", "particles in lubricant", "debris in oil"],
    "abnormal bearing wear": ["abnormal bearing wear", "bearing wear"],
    "visible corrosion": ["visible corrosion", "rust", "corrosion"],
    "surface pitting": ["surface pitting", "pitting on the surface", "pitted surface"],
    "material cracking": ["material cracking", "crack in the material", "cracked component", "material crack"],
}


def extract_symptoms_from_text(text):
    """Return known symptom labels suggested by a free-text description."""
    lowered = text.lower()
    found = []
    for symptom in ALL_SYMPTOMS:
        phrases = SYMPTOM_KEYWORDS.get(symptom, [symptom])
        if any(phrase in lowered for phrase in phrases):
            found.append(symptom)
    return found

# ------------------------------------------
# Agent reasoning engine
# ------------------------------------------


def rank_failures(symptoms, inspection_results):
    results = []

    for name, details in FAILURES.items():
        known = set(details["symptoms"])
        matches = set(symptoms) & known

        # Each matching symptom contributes evidence.
        # These are heuristic weights, not probabilities.
        score = sum(
            2 for symptom in matches
        )

        reasons = []

        if matches:
            reasons.append(
                "Matching symptoms: " + ", ".join(sorted(matches))
            )

        # Inspection evidence is interpreted separately.
        for check, outcome in inspection_results.items():
            if CHECK_TARGETS.get(check) != name:
                continue

            if outcome == "Finding observed":
                score += 3
                reasons.append(
                    f"Supporting evidence: {check}"
                )

            elif outcome == "Finding not observed":
                score -= 3
                reasons.append(
                    f"Expected finding not observed: {check}"
                )

            else:
                reasons.append(
                    f"Inconclusive inspection: {check}"
                )

        results.append({
            "failure": name,
            "score": max(0, score),
            "matches": sorted(matches),
            "checks": details["checks"],
            "reasons": reasons
        })

    # Higher evidence scores appear first.
    results.sort(
        key=lambda item: (
            item["score"],
            len(item["matches"])
        ),
        reverse=True
    )

    return results


def select_next_check(ranked, inspection_results):
    # Prefer an uncompleted check for the highest-ranked
    # candidate. If none remain, consider other candidates.
    for candidate in ranked:
        # Do not recommend checks for candidates with no supporting evidence.
        if candidate["score"] <= 0:
            continue
        for check in candidate["checks"]:
            if check not in inspection_results:
                return check

    return None


# ------------------------------------------
# Session state
# ------------------------------------------

if "inspection_results" not in st.session_state:
    st.session_state.inspection_results = {}

if "reported_symptoms" not in st.session_state:
    st.session_state.reported_symptoms = []

if "diagnosis_started" not in st.session_state:
    st.session_state.diagnosis_started = False


# ------------------------------------------
# Application interface
# ------------------------------------------


# ==========================================
# ANIMATED APPLICATION HEADER
# ==========================================


st.markdown(
    "<div style='color:#7fe7d8;font-size:11px;font-weight:800;"
    "letter-spacing:2px;margin:6px 0 14px 0;'>"
    "● DIAGNOSTIC WORKSPACE / RULE-BASED REASONING ENGINE</div>",
    unsafe_allow_html=True
)


st.info(
    "This educational prototype ranks potential causes "
    "using a rule-based knowledge base. It does not "
    "confirm real machine failures."
)

# Chat is the primary feature; structured tools follow beneath it.
# ------------------------------------------
# Local AI chat assistant (Ollama; no paid API)
# ------------------------------------------
st.divider()
st.markdown("""
<div style="display:flex;align-items:flex-start;gap:14px;margin:8px 0 6px 0;">
  <div style="width:46px;height:46px;display:flex;align-items:center;justify-content:center;border-radius:14px;background:linear-gradient(135deg,rgba(67,217,195,.18),rgba(23,107,145,.28));border:1px solid rgba(67,217,195,.34);font-size:24px;">✦</div>
  <div>
    <div style="font-size:11px;letter-spacing:2px;font-weight:800;color:#43d9c3;margin-bottom:5px;">YOUR DIAGNOSTIC COPILOT</div>
    <div style="font-size:27px;font-weight:800;line-height:1.2;color:#f0f6ff;">Tell me what the machine is doing.</div>
    <div style="font-size:14px;color:#a8bbce;margin-top:7px;">Describe the equipment, symptoms, noises, temperatures, or changes in performance.</div>
  </div>
</div>
""", unsafe_allow_html=True)
st.caption(
    "Local AI · No paid API · Symptoms from your message update the rule-based assessment; inspection findings are only recorded when you submit them below."
)

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! Describe the machine, what changed, and any symptoms "
                "you have observed. I can suggest possible causes and useful "
                "follow-up checks. I cannot confirm a fault from a description alone."
            ),
        }
    ]

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Starter prompts are shown only before the user begins the conversation.
# After any starter prompt or typed message, chat_messages contains a user turn
# and these buttons disappear on the next Streamlit rerun.
show_starter_prompts = (
    len(st.session_state.chat_messages) == 1
    and not st.session_state.get("conversation_started", False)
)
if show_starter_prompts:
    st.markdown('<div class="suggestion-label">START WITH A COMMON ISSUE</div>', unsafe_allow_html=True)
    _s1, _s2, _s3 = st.columns(3)
    if "suggested_chat_prompt" not in st.session_state:
        st.session_state.suggested_chat_prompt = ""
    if _s1.button("⚙️  Excessive vibration", use_container_width=True, key="suggest_vibration"):
        st.session_state.suggested_chat_prompt = "My machine is experiencing excessive vibration. What could cause it and what should I check first?"
    if _s2.button("💧  Pump flow problem", use_container_width=True, key="suggest_pump"):
        st.session_state.suggested_chat_prompt = "My industrial pump has low flow and unusual noise. Help me investigate possible causes."
    if _s3.button("🌡️  Motor overheating", use_container_width=True, key="suggest_heat"):
        st.session_state.suggested_chat_prompt = "My motor is overheating during operation. What are the possible causes and safe checks?"
else:
    st.session_state.suggested_chat_prompt = ""

with st.form("chat_composer_form", clear_on_submit=True, border=False):
    _chat_col, _send_col = st.columns([12, 1])
    with _chat_col:
        typed_prompt = st.text_input(
            "Message Failure Detective AI",
            placeholder="Describe the machine, symptoms, noise, temperature, or performance change...",
            label_visibility="collapsed",
            key="chat_composer_text",
        )
    with _send_col:
        send_chat = st.form_submit_button("➤", use_container_width=True)

user_prompt = st.session_state.suggested_chat_prompt.strip()
if user_prompt:
    st.session_state.suggested_chat_prompt = ""
elif send_chat and typed_prompt.strip():
    user_prompt = typed_prompt.strip()
else:
    user_prompt = ""

if user_prompt:
    st.session_state.conversation_started = True
    st.session_state.chat_messages.append(
        {"role": "user", "content": user_prompt}
    )
    with st.chat_message("user"):
        st.markdown(user_prompt)

    knowledge_lines = []
    for failure_name, details in FAILURES.items():
        knowledge_lines.append(
            f"- {failure_name}: symptoms={', '.join(details['symptoms'])}; "
            f"checks={'; '.join(details['checks'])}"
        )
    knowledge_context = "\n".join(knowledge_lines)

    # Connect the conversation to the existing diagnostic engine. Only symptoms
    # detected from the user's own description are added; inspection findings
    # are never inferred from chat text.
    newly_detected = extract_symptoms_from_text(user_prompt)
    combined_symptoms = sorted(set(st.session_state.reported_symptoms) | set(newly_detected))
    if newly_detected:
        st.session_state.reported_symptoms = combined_symptoms
        st.session_state.diagnosis_started = True

    current_ranked = rank_failures(
        st.session_state.reported_symptoms,
        st.session_state.inspection_results,
    )
    diagnosis_lines = []
    if st.session_state.reported_symptoms:
        diagnosis_lines.append("Symptoms currently recorded by the rule-based engine: " + ", ".join(st.session_state.reported_symptoms))
        positive_candidates = [item for item in current_ranked if item["score"] > 0]
        if positive_candidates:
            diagnosis_lines.append("Current ranked candidates with supporting evidence (heuristic scores, not probabilities):")
        else:
            diagnosis_lines.append("No candidate currently has a positive evidence score. Ask for more detail instead of listing zero-score candidates.")
        for item in positive_candidates[:5]:
            diagnosis_lines.append(
                f"- {item['failure']} (score {item['score']}); matching symptoms: "
                + (", ".join(item["matches"]) if item["matches"] else "none")
                + "; suggested checks: " + "; ".join(item["checks"])
            )
    else:
        diagnosis_lines.append("No known symptom has yet been confidently matched from the conversation. Ask clarifying questions instead of pretending the rule engine has a ranking.")
    if st.session_state.inspection_results:
        diagnosis_lines.append("Recorded inspection outcomes (only these are verified user inputs):")
        for check, outcome in st.session_state.inspection_results.items():
            diagnosis_lines.append(f"- {check}: {outcome}")
    diagnosis_context = "\n".join(diagnosis_lines)

    system_prompt = f"""You are Failure Detective AI, a cautious mechanical fault troubleshooting assistant.
Use clear, concise explanations suitable for a mechanical engineering student or machine operator.
Use the knowledge base below as a reference, not as proof. You may mention other plausible causes, but clearly label them as possibilities outside the listed knowledge base.
Never claim a fault is confirmed from symptoms alone. Do not invent inspection measurements or results. Ask one or two useful follow-up questions when important information is missing. Recommend safe, non-invasive checks first. For inspection of rotating, electrical, pressurized, or hot equipment, remind the user to follow lockout/tagout and relevant site safety procedures and use qualified personnel. If the description suggests immediate danger, advise stopping the equipment safely and seeking qualified help.
When helpful, explain which symptoms support or weaken each candidate and suggest the next check. The app's numeric evidence scores are heuristic rankings, not probabilities.

Current mechanical failure knowledge base:
{knowledge_context}

Current output from the app's rule-based diagnostic engine:
{diagnosis_context}

Integration rules:
- Treat the ranked candidates and scores above as the app's current rule-based assessment.
- Explain the leading candidates using only the recorded symptoms and inspection outcomes.
- If known symptoms were matched, explicitly summarize the top two or three candidates and their relevant checks in your response.
- Do not change scores yourself and do not treat symptom keyword matches as confirmation.
- If no known symptom was matched, ask a concise clarifying question and explain that the user can describe the machine and symptoms in more detail.
- Never claim that an inspection was performed unless its outcome appears in the recorded inspection outcomes above.
"""

    chat_payload = [{"role": "system", "content": system_prompt}]
    # Send recent turns to keep requests bounded while preserving context.
    chat_payload.extend(st.session_state.chat_messages[-12:])

    with st.chat_message("assistant"):
        with st.spinner("Analysing the description with your local model..."):
            try:
                response = requests.post(
                    "http://localhost:11434/api/chat",
                    json={
                        "model": "llama3.2:3b",
                        "messages": chat_payload,
                        "stream": False,
                        "options": {"temperature": 0.2},
                    },
                    timeout=180,
                )
                response.raise_for_status()
                answer = response.json().get("message", {}).get("content", "").strip()
                if not answer:
                    answer = "The local model returned an empty response. Please try again."
            except requests.exceptions.ConnectionError:
                answer = (
                    "I couldn't connect to Ollama. Make sure Ollama is installed and running, "
                    "then check Command Prompt with `ollama list`."
                )
            except requests.exceptions.Timeout:
                answer = (
                    "The local model took too long to respond. Try a shorter question or "
                    "close other demanding applications and try again."
                )
            except requests.exceptions.RequestException as exc:
                answer = (
                    f"Ollama returned an error: {exc}. Check that `llama3.2:3b` is installed "
                    "by running `ollama list` in Command Prompt."
                )
            except (ValueError, KeyError, TypeError):
                answer = "I couldn't read the response from Ollama. Please try again."
        st.markdown(answer)

    st.session_state.chat_messages.append(
        {"role": "assistant", "content": answer}
    )

    # Refresh the page so the diagnostic ranking above the chat reflects
    # any new symptoms extracted from this user message.
    st.rerun()

if st.button("Clear Chat Conversation"):
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! Describe the machine, what changed, and any symptoms "
                "you have observed. I can suggest possible causes and useful "
                "follow-up checks. I cannot confirm a fault from a description alone."
            ),
        }
    ]
    st.session_state.conversation_started = False
    st.session_state.suggested_chat_prompt = ""
    st.rerun()


st.divider()
st.markdown("""
<div style="font-size:11px;letter-spacing:2px;font-weight:800;color:#43d9c3;margin:6px 0 8px 0;">ENGINEERING WORKBENCH</div>
<div style="font-size:25px;font-weight:800;color:#f0f6ff;margin-bottom:4px;">Diagnostic tools</div>
<div style="font-size:14px;color:#a8bbce;margin-bottom:14px;">Review the evidence, record inspection findings, and export a report.</div>
""", unsafe_allow_html=True)

st.header("Confirm observed symptoms")

with st.form("symptom_form"):
    symptoms = st.multiselect(
        "Select all observed symptoms",
        options=ALL_SYMPTOMS,
        default=st.session_state.reported_symptoms,
        help="Choose every symptom that has actually been observed."
    )

    submitted = st.form_submit_button(
    "⚡ Analyse Symptoms",
    type="primary",
    use_container_width=True
    )

    if submitted:
        st.session_state.reported_symptoms = symptoms
        st.session_state.inspection_results = {}
        st.session_state.diagnosis_started = True

if st.session_state.diagnosis_started:

    symptoms = st.session_state.reported_symptoms
    inspection_results = st.session_state.inspection_results
    ranked = rank_failures(symptoms, inspection_results)

    st.divider()
    st.header("Fault assessment")

    if not symptoms:
        st.warning(
            "Select at least one symptom to begin the investigation."
        )
    else:
        st.write(
            "The agent has compared the reported symptoms with "
            "its mechanical failure knowledge base."
        )

        positive_ranked = [candidate for candidate in ranked if candidate["score"] > 0]

        if positive_ranked:
            cols = st.columns(min(3, len(positive_ranked)))
            for index, candidate in enumerate(positive_ranked[:3]):
                with cols[index]:
                    st.metric(
                        label=f"Candidate {index + 1}",
                        value=candidate["failure"],
                        delta=f"Evidence score: {candidate['score']}"
                    )
                    st.caption(
                        "Matching symptoms: " + ", ".join(candidate["matches"])
                        if candidate["matches"]
                        else "Supported by recorded inspection evidence."
                    )
            st.caption(
                "Only candidates with a positive evidence score are shown. Scores are heuristic rankings, not probabilities."
            )
        else:
            st.info(
                "No fault currently has supporting evidence in the knowledge base. "
                "Describe more symptoms or add an inspection finding to narrow the possibilities."
            )

        st.divider()
        st.header("Recommended inspection")

        next_check = select_next_check(
            ranked,
            inspection_results
        )

        if next_check:
            target = CHECK_TARGETS[next_check]

            st.write(
                f"**Next suggested check:** {next_check}"
            )
            st.write(
                f"This check investigates: **{target}**"
            )

            with st.form("inspection_form"):
                outcome = st.radio(
                    "What did the inspection reveal?",
                    [
                        "Finding observed",
                        "Finding not observed",
                        "Inconclusive"
                    ],
                    help=(
                        "'Finding observed' means the relevant "
                        "abnormal finding was present. 'Finding not "
                        "observed' means it was not found. Choose "
                        "'Inconclusive' if the check was uncertain "
                        "or could not be completed."
                    )
                )

                record = st.form_submit_button(
                    "Record Finding and Reassess",
                    type="primary"
                )

                if record:
                    st.session_state.inspection_results[
                        next_check
                    ] = outcome

                    st.rerun()

        else:
            st.success(
                "All available checks in this knowledge base "
                "have been recorded."
            )

        if inspection_results:
            st.divider()
            st.header("Inspection history")

            for check, outcome in inspection_results.items():
                st.write(f"- **{check}:** {outcome}")

        st.divider()
        st.header("Diagnostic report")

        ranked = rank_failures(symptoms, inspection_results)

        report = [
            "FAILURE DETECTIVE AI — DIAGNOSTIC REPORT",
            "=" * 45,
            "",
            "Reported symptoms:",
            *[f"- {item}" for item in symptoms],
            "",
            "Inspection findings:"
        ]

        if inspection_results:
            report.extend(
                f"- {check}: {outcome}"
                for check, outcome in inspection_results.items()
            )
        else:
            report.append("- No inspection results recorded.")

        report.extend(["", "Ranked potential causes:"])

        positive_report_candidates = [candidate for candidate in ranked if candidate["score"] > 0]
        if not positive_report_candidates:
            report.append("No candidates currently have a positive evidence score.")

        for index, candidate in enumerate(positive_report_candidates, start=1):
            report.extend([
                "",
                f"{index}. {candidate['failure']}",
                f"   Evidence score: {candidate['score']}",
                "   Matching symptoms: "
                + (
                    ", ".join(candidate["matches"])
                    if candidate["matches"]
                    else "None"
                ),
                "   Suggested checks: "
+ "; ".join(candidate["checks"]),
"   Reasoning: "
+ (
    "; ".join(candidate["reasons"])
    if candidate["reasons"]
    else "No supporting symptom evidence"
)
            ])

        report.extend([
            "",
            "LIMITATION:",
            "This is a preliminary rule-based assessment. "
            "Scores are not probabilities. Findings must be "
            "verified by a qualified person using appropriate "
            "measurements and safety procedures."
        ])

        report_text = "\n".join(report)
        # Use a themed code panel instead of a text area: Streamlit's
        # textarea styling can be overridden by browser/theme defaults,
        # making light text nearly invisible on a light background.
        st.markdown("**Report preview**")
        st.code(report_text, language=None, wrap_lines=True)

        st.download_button(
            label="Download Diagnostic Report",
            data=report_text,
            file_name="failure_diagnostic_report.txt",
            mime="text/plain"
        )



st.divider()

if st.button("Reset Investigation"):
    st.session_state.inspection_results = {}
    st.session_state.reported_symptoms = []
    st.session_state.diagnosis_started = False
    st.rerun()

st.caption(
    "Failure Detective AI | Mechanical Engineering "
    "Diagnostic Decision-Support Prototype"
)
