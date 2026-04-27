"""
ui_config.py — Theme CSS injection, header, footer rendering
"""

import streamlit as st


# ── Color tokens ───────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "--bg-primary": "#0d0d0d",
        "--bg-secondary": "#161616",
        "--bg-card": "#1e1e1e",
        "--bg-input": "#141414",
        "--border": "#2a2a2a",
        "--text-primary": "#f0f0f0",
        "--text-secondary": "#9a9a9a",
        "--accent": "#f0a500",
        "--accent-hover": "#ffc040",
        "--accent-light": "rgba(240,165,0,0.12)",
        "--tag-bg": "#252525",
        "--shadow": "0 4px 24px rgba(0,0,0,0.5)",
        "--hero-overlay": "rgba(0,0,0,0.72)",
    },
    "light": {
        "--bg-primary": "#f5f5f0",
        "--bg-secondary": "#ffffff",
        "--bg-card": "#ffffff",
        "--bg-input": "#fafaf8",
        "--border": "#e0e0d8",
        "--text-primary": "#1a1a1a",
        "--text-secondary": "#666660",
        "--accent": "#d08000",
        "--accent-hover": "#f0a500",
        "--accent-light": "rgba(208,128,0,0.10)",
        "--tag-bg": "#f0f0e8",
        "--shadow": "0 4px 24px rgba(0,0,0,0.10)",
        "--hero-overlay": "rgba(255,255,255,0.18)",
    },
}


def apply_theme(theme: str = "dark") -> None:
    """Inject CSS variables and global styles."""
    tokens = THEMES[theme]
    css_vars = "\n".join(f"        {k}: {v};" for k, v in tokens.items())

    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

        :root {{
{css_vars}
        }}

        /* ── Reset & base ─────────────────────────────────────── */
        html, body, [class*="css"] {{
            font-family: 'DM Sans', sans-serif;
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }}

        .stApp {{
            background-color: var(--bg-primary) !important;
        }}

        /* Hide Streamlit chrome */
        #MainMenu, footer, header {{ visibility: hidden; }}
        .block-container {{
            padding: 0 2rem 3rem 2rem !important;
            max-width: 1400px !important;
        }}

        /* ── Hero banner ──────────────────────────────────────── */
        .hero-banner {{
            background: linear-gradient(135deg, #111 0%, #1a1400 50%, #111 100%);
            border-bottom: 1px solid var(--border);
            padding: 2.2rem 3rem;
            margin: -1rem -2rem 2rem -2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .hero-banner.light-hero {{
            background: linear-gradient(135deg, #f8f6ee 0%, #fff8e6 50%, #f8f6ee 100%);
            border-bottom: 1px solid var(--border);
        }}

        .hero-left {{
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }}

        .logo-mark {{
            font-family: 'Syne', sans-serif;
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--accent);
            letter-spacing: -0.03em;
        }}

        .hero-nav {{
            display: flex;
            gap: 2rem;
            align-items: center;
        }}

        .hero-nav a {{
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.2s;
        }}

        .hero-nav a:hover {{ color: var(--accent); }}
        .hero-nav a.active {{ color: var(--accent); }}

        .hero-title-block {{
            text-align: center;
            flex: 1;
        }}

        .hero-title {{
            font-family: 'Syne', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0;
            letter-spacing: -0.02em;
        }}

        .hero-sub {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 0.3rem;
        }}

        .hero-actions {{
            display: flex;
            gap: 0.8rem;
            align-items: center;
        }}

        .btn-outline {{
            border: 1.5px solid var(--accent);
            color: var(--accent);
            background: transparent;
            padding: 0.45rem 1.2rem;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            font-family: 'DM Sans', sans-serif;
            letter-spacing: 0.05em;
            transition: all 0.2s;
        }}

        .btn-solid {{
            background: var(--accent);
            color: #000;
            border: none;
            padding: 0.45rem 1.2rem;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: 700;
            cursor: pointer;
            font-family: 'DM Sans', sans-serif;
            letter-spacing: 0.05em;
        }}

        /* ── Info banner ──────────────────────────────────────── */
        .info-banner {{
            background: var(--accent-light);
            border-left: 3px solid var(--accent);
            border-radius: 4px;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.5rem;
            font-size: 0.88rem;
            color: var(--text-secondary);
            line-height: 1.6;
        }}

        .info-banner a {{ color: var(--accent); text-decoration: none; font-weight: 500; }}

        /* ── Section titles ───────────────────────────────────── */
        .section-label {{
            font-family: 'Syne', sans-serif;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 0.6rem;
        }}

        /* ── Cards ────────────────────────────────────────────── */
        .result-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.2rem 1.4rem;
            box-shadow: var(--shadow);
            margin-bottom: 1rem;
        }}

        .sentiment-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--accent-light);
            border: 1.5px solid var(--accent);
            border-radius: 30px;
            padding: 0.55rem 1.4rem;
            font-family: 'Syne', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--accent);
            margin-bottom: 1rem;
        }}

        .score-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.7rem;
            margin-bottom: 1rem;
        }}

        .score-item {{
            background: var(--tag-bg);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.8rem 0.6rem;
            text-align: center;
        }}

        .score-label {{
            font-size: 0.72rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 600;
            margin-bottom: 0.3rem;
        }}

        .score-value {{
            font-family: 'Syne', sans-serif;
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--text-primary);
        }}

        .score-emoji {{ font-size: 1.2rem; }}

        /* ── Aspect tags ──────────────────────────────────────── */
        .aspect-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }}

        .aspect-tag {{
            background: var(--tag-bg);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 0.3rem 0.75rem;
            font-size: 0.8rem;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .aspect-tag.pos {{ border-color: #2d6a2d; color: #6fcf6f; background: rgba(45,106,45,0.15); }}
        .aspect-tag.neg {{ border-color: #6a2d2d; color: #cf6f6f; background: rgba(106,45,45,0.15); }}
        .aspect-tag.neu {{ border-color: var(--border); }}

        /* ── Progress bar override ────────────────────────────── */
        .stProgress > div > div {{ background-color: var(--accent) !important; }}
        .stProgress > div {{ background-color: var(--border) !important; border-radius: 4px; }}

        /* ── Textarea & file uploader ─────────────────────────── */
        .stTextArea textarea {{
            background: var(--bg-input) !important;
            border: 1.5px solid var(--border) !important;
            color: var(--text-primary) !important;
            border-radius: 6px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 0.93rem !important;
            resize: vertical !important;
        }}

        .stTextArea textarea:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 2px var(--accent-light) !important;
        }}

        .stFileUploader {{
            background: var(--bg-input) !important;
            border: 1.5px dashed var(--border) !important;
            border-radius: 6px !important;
        }}

        /* ── Tabs ─────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {{
            background: var(--bg-card) !important;
            border-bottom: 1px solid var(--border) !important;
            border-radius: 6px 6px 0 0 !important;
            padding: 0 0.5rem !important;
            gap: 0 !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            color: var(--text-secondary) !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            padding: 0.75rem 1.2rem !important;
            border-bottom: 2px solid transparent !important;
        }}

        .stTabs [aria-selected="true"] {{
            color: var(--accent) !important;
            border-bottom: 2px solid var(--accent) !important;
            background: transparent !important;
        }}

        .stTabs [data-baseweb="tab-panel"] {{
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-top: none !important;
            border-radius: 0 0 6px 6px !important;
            padding: 1.2rem !important;
        }}

        /* ── Run button ───────────────────────────────────────── */
        .stButton > button {{
            background: var(--accent) !important;
            color: #000 !important;
            border: none !important;
            border-radius: 4px !important;
            font-family: 'Syne', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.88rem !important;
            letter-spacing: 0.08em !important;
            padding: 0.65rem 2rem !important;
            transition: all 0.2s !important;
        }}

        .stButton > button:hover {{
            background: var(--accent-hover) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(240,165,0,0.25) !important;
        }}

        /* ── Placeholder box ──────────────────────────────────── */
        .placeholder-box {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 4rem 2rem;
            border: 1.5px dashed var(--border);
            border-radius: 8px;
            height: 100%;
            min-height: 350px;
        }}

        .placeholder-icon {{ font-size: 3rem; margin-bottom: 1rem; opacity: 0.5; }}
        .placeholder-title {{
            font-family: 'Syne', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-secondary);
            margin: 0 0 0.5rem 0;
        }}
        .placeholder-sub {{ color: var(--text-secondary); font-size: 0.88rem; margin: 0; opacity: 0.7; }}

        /* ── Footer ───────────────────────────────────────────── */
        .app-footer {{
            border-top: 1px solid var(--border);
            padding: 1.2rem 0;
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.82rem;
            margin-top: 2rem;
        }}

        /* ── Spinner ──────────────────────────────────────────── */
        .stSpinner > div {{ border-top-color: var(--accent) !important; }}

        /* ── Radio buttons (theme toggle) ─────────────────────── */
        .stRadio > div {{ flex-direction: row !important; gap: 0.5rem !important; }}
        .stRadio label {{ font-size: 0.85rem !important; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_header() -> None:
    """Render the top hero banner."""
    theme = st.session_state.theme
    hero_class = "light-hero" if theme == "light" else ""
    nav_link = (
        '<a href="#" class="active">Demo</a>'
        '<a href="#">Products</a>'
        '<a href="#">Pricing</a>'
        '<a href="#">Blog</a>'
    )

    # Theme toggle lives inside the Streamlit column for reactivity
    col_logo, col_title, col_right = st.columns([1, 2, 1])
    with col_logo:
        st.markdown(
            f'<div class="logo-mark" style="padding-top:0.3rem">SentiScope</div>',
            unsafe_allow_html=True,
        )
    with col_title:
        st.markdown(
            '<div class="hero-title-block">'
            '<h1 class="hero-title">Free Sentiment Analysis</h1>'
            '<p class="hero-sub">AI-powered • Multi-format • Real-time</p>'
            "</div>",
            unsafe_allow_html=True,
        )
    with col_right:
        choice = st.radio(
            "Theme",
            ["🌙 Dark", "☀️ Light"],
            horizontal=True,
            label_visibility="collapsed",
            key="theme_radio",
        )
        new_theme = "dark" if choice == "🌙 Dark" else "light"
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()

    st.markdown(
        '<div class="info-banner">💡 This demo uses generic models trained on product reviews and user opinions. '
        "For domain-specific accuracy, consider fine-tuning your own sentiment model.</div>",
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        '<div class="app-footer">SentiScope © 2025 — Powered by Claude AI · '
        "Built for scale and precision</div>",
        unsafe_allow_html=True,
    )
