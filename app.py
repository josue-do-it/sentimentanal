"""
Sentiment Analysis App — Streamlit
Modular, production-grade, dark/light theme
"""

import sys
import os

# Ensure the app directory is on the path (required for Streamlit Cloud)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from modules.ui_config import apply_theme, render_header, render_footer
from modules.input_handler import render_input_section
from modules.analyzer import analyze_sentiment
from modules.results_display import render_results

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SentiScope — Sentiment Analysis",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state defaults ─────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "results" not in st.session_state:
    st.session_state.results = None
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# ── Apply CSS theme ────────────────────────────────────────────────────────────
apply_theme(st.session_state.theme)

# ── Header ─────────────────────────────────────────────────────────────────────
render_header()

# ── Main layout ────────────────────────────────────────────────────────────────
col_input, col_results = st.columns([1, 1], gap="large")

with col_input:
    text, submitted = render_input_section()

with col_results:
    if submitted and text:
        with st.spinner("Analyzing sentiment..."):
            results = analyze_sentiment(text)
            st.session_state.results = results
            st.session_state.text_input = text

    if st.session_state.results:
        render_results(st.session_state.results, st.session_state.text_input)
    else:
        st.markdown(
            """
            <div class="placeholder-box">
                <div class="placeholder-icon">🔍</div>
                <p class="placeholder-title">Results will appear here</p>
                <p class="placeholder-sub">Enter text or upload a file and click <strong>Run Analysis</strong></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Footer ─────────────────────────────────────────────────────────────────────
render_footer()
