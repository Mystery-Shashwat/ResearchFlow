import streamlit as st
import markdown
from pipeline import run_research_pipeline

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchFlow AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background: #08080f;
    color: #ddd9ce;
}
.stApp { background: #08080f; }

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ═══════════════════════════════════════════
   HERO — input zone
═══════════════════════════════════════════ */
.hero {
    width: 100%;
    padding: 5rem 2rem 1.5rem;
    text-align: center;
    background:
        radial-gradient(ellipse 70% 55% at 50% -10%, rgba(180,140,70,0.13) 0%, transparent 70%),
        #08080f;
    border-bottom: 1px solid #1c1b22;
}

.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #c8a96e;
    margin-bottom: 1.2rem;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.08;
    background: linear-gradient(135deg, #f5edda 0%, #c8a96e 55%, #e8d090 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.8rem;
}

.hero-sub {
    font-size: 0.82rem;
    color: #5a5750;
    margin-bottom: 2.5rem;
    letter-spacing: 0.02em;
}

/* ── input wrapper ── */
.stTextInput > div > div > input {
    background: #111019 !important;
    border: 1.5px solid #2a2830 !important;
    border-radius: 10px !important;
    color: #f0ece0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1rem !important;
    padding: 1rem 1.3rem !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
    caret-color: #c8a96e !important;
}
.stTextInput > div > div > input::placeholder { color: #3e3c48 !important; }
.stTextInput > div > div > input:focus {
    border-color: #c8a96e !important;
    box-shadow: 0 0 0 4px rgba(200,169,110,0.10) !important;
    outline: none !important;
}
.stTextInput label { display: none !important; }

.stButton > button {
    background: linear-gradient(135deg, #c8a96e 0%, #9e7a38 100%) !important;
    color: #08080f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.85rem 0 !important;
    width: 100% !important;
    margin-top: 0.6rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover  { opacity: 0.85 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ═══════════════════════════════════════════
   PIPELINE TRACKER — horizontal steps
═══════════════════════════════════════════ */
.pipeline-bar {
    width: 100%;
    padding: 2.2rem 6rem;
    background: #0c0b13;
    border-bottom: 1px solid #1c1b22;
    display: flex;
    align-items: flex-start;
    justify-content: center;
}

.step-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    flex: 1;
    max-width: 200px;
}

.step-node:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 19px;
    left: calc(50% + 22px);
    width: calc(100% - 44px);
    height: 1px;
    background: #1e1c26;
}
.step-node.done:not(:last-child)::after   { background: #4a7c59; }
.step-node.active:not(:last-child)::after { background: linear-gradient(90deg, #c8a96e44, #1e1c26); }

.step-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 1.5px solid #2a2830;
    background: #111019;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    color: #3e3c48;
    margin-bottom: 0.65rem;
    position: relative;
    z-index: 1;
}
.step-node.active .step-circle {
    border-color: #c8a96e;
    background: rgba(200,169,110,0.12);
    color: #c8a96e;
    box-shadow: 0 0 18px rgba(200,169,110,0.28);
}
.step-node.done .step-circle {
    border-color: #4a7c59;
    background: rgba(74,124,89,0.15);
    color: #6ab07a;
}

.step-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    color: #3e3c48;
    text-align: center;
}
.step-node.active .step-label { color: #f0ece0; }
.step-node.done  .step-label  { color: #6ab07a; }

.step-status {
    font-size: 0.60rem;
    margin-top: 0.22rem;
    color: #2e2c38;
    text-transform: uppercase;
    letter-spacing: 0.14em;
}
.step-node.active .step-status { color: #c8a96e; }
.step-node.done   .step-status { color: #4a7c59; }

/* ═══════════════════════════════════════════
   OUTPUT AREA
═══════════════════════════════════════════ */
.sec-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.26em;
    text-transform: uppercase;
    color: #c8a96e;
    margin-bottom: 0.85rem;
}

.output-box {
    background: #0e0d16;
    border: 1px solid #1c1b22;
    border-radius: 10px;
    padding: 1.3rem 1.5rem;
    font-size: 0.78rem;
    line-height: 1.75;
    color: #7a7870;
    max-height: 220px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
    margin-bottom: 2.8rem;
}

.report-card {
    background: #0e0d16;
    border: 1px solid #1c1b22;
    border-radius: 12px;
    padding: 2.2rem 2.6rem;
    margin-bottom: 2.8rem;
    line-height: 1.85;
}

.sec-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e1c26 20%, #1e1c26 80%, transparent);
    margin: 0.5rem 0 2.8rem;
}

.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    color: #2a2830;
}
.empty-icon  { font-size: 2.8rem; margin-bottom: 1rem; }
.empty-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #383642;
    margin-bottom: 0.45rem;
}
.empty-sub { font-size: 0.76rem; color: #2e2c38; line-height: 1.65; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #08080f; }
::-webkit-scrollbar-thumb { background: #2e2c38; border-radius: 2px; }

.stSpinner > div { border-top-color: #c8a96e !important; }
.stAlert { border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
if "results"  not in st.session_state: st.session_state.results  = None
if "running"  not in st.session_state: st.session_state.running  = False
if "cur_step" not in st.session_state: st.session_state.cur_step = -1

results  = st.session_state.results
running  = st.session_state.running
cur_step = st.session_state.cur_step

STEPS = [
    ("Search",  "🔍", "Finding sources"),
    ("Reader",  "🌐", "Scraping pages"),
    ("Writer",  "✍️",  "Drafting report"),
    ("Critic",  "✅", "Reviewing report"),
]


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <div class="hero-title">ResearchFlow</div>
    <div class="hero-sub">
        Enter any topic — four specialised agents search, read, write and critique a full research report.
    </div>
</div>
""", unsafe_allow_html=True)

# Centred input row beneath the hero banner
gap1, inp_col, gap2 = st.columns([1, 2.2, 1])
with inp_col:
    st.markdown("<div style='padding: 2rem 0 0;'></div>", unsafe_allow_html=True)
    topic   = st.text_input("topic", placeholder="e.g.  Quantum computing breakthroughs in 2025",
                             label_visibility="collapsed")
    run_btn = st.button("⟶  Run Research Pipeline")
    st.markdown("<div style='padding-bottom: 2.5rem;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — PIPELINE TRACKER
# ══════════════════════════════════════════════════════════════════════════════
def node_class(i):
    if results:                       return "done"
    if running and i == cur_step:     return "active"
    return ""

nodes_html = ""
for i, (label, icon, sub) in enumerate(STEPS):
    cls    = node_class(i)
    circle = "✓" if cls == "done" else (icon if cls == "active" else str(i + 1))
    status = "Done" if cls == "done" else ("Running…" if cls == "active" else "Waiting")
    nodes_html += f"""
    <div class="step-node {cls}">
        <div class="step-circle">{circle}</div>
        <div class="step-label">{label} Agent</div>
        <div class="step-status">{status}</div>
    </div>"""

st.markdown(f'<div class="pipeline-bar">{nodes_html}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════
_, content_col, _ = st.columns([0.12, 0.76, 0.12])

with content_col:
    st.markdown("<div style='padding-top: 2.8rem;'></div>", unsafe_allow_html=True)

    out_ph      = st.empty()
    report_ph   = st.empty()
    feedback_ph = st.empty()

    if not results and not running:
        out_ph.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🔬</div>
            <div class="empty-title">No research run yet</div>
            <div class="empty-sub">
                Enter a topic above and click <strong style="color:#c8a96e">Run Research Pipeline</strong><br>
                to kick off the four-agent workflow.
            </div>
        </div>
        """, unsafe_allow_html=True)

    if results:
        with out_ph.container():
            st.markdown('<div class="sec-label">🔍 Search Agent — Sources Found</div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{results.get("search_results","—")}</div>',
                        unsafe_allow_html=True)
            st.markdown('<div class="sec-label">🌐 Reader Agent — Scraped Content</div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{results.get("scraped_content","—")}</div>',
                        unsafe_allow_html=True)

        with report_ph.container():
            st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-label">✍️ Writer Agent — Final Report</div>',
                        unsafe_allow_html=True)
            report_html = markdown.markdown(results.get("report", ""))
            st.markdown(f'<div class="report-card">{report_html}</div>', unsafe_allow_html=True)

        with feedback_ph.container():
            st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-label">✅ Critic Agent — Review & Feedback</div>',
                        unsafe_allow_html=True)
            feedback_html = markdown.markdown(results.get("feedback", ""))
            st.markdown(f'<div class="report-card">{feedback_html}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RUN PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results  = None
        st.session_state.running  = True
        st.session_state.cur_step = 0

        with st.spinner("Pipeline running — this may take a minute…"):
            try:
                result = run_research_pipeline(topic.strip())
                st.session_state.results  = result
                st.session_state.cur_step = 4
            except Exception as e:
                st.error(f"Pipeline error: {e}")
            finally:
                st.session_state.running = False

        st.rerun()