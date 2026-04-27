"""
input_handler.py — Text input (paste) and file upload tabs
Returns (text: str, submitted: bool)
"""

import io
import streamlit as st

# Optional heavy imports — graceful fallback if not installed
try:
    import pdfplumber
    _PDF_OK = True
except ImportError:
    _PDF_OK = False

try:
    import docx as python_docx
    _DOCX_OK = True
except ImportError:
    _DOCX_OK = False


# ── Supported file types ────────────────────────────────────────────────────────
ACCEPTED_TYPES = ["txt", "md", "csv"]
if _PDF_OK:
    ACCEPTED_TYPES.append("pdf")
if _DOCX_OK:
    ACCEPTED_TYPES.append("docx")


# ── File parsers ────────────────────────────────────────────────────────────────

def _parse_txt(raw: bytes) -> str:
    return raw.decode("utf-8", errors="ignore")


def _parse_pdf(raw: bytes) -> str:
    if not _PDF_OK:
        return ""
    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        pages = [p.extract_text() or "" for p in pdf.pages]
    return "\n\n".join(pages).strip()


def _parse_docx(raw: bytes) -> str:
    if not _DOCX_OK:
        return ""
    doc = python_docx.Document(io.BytesIO(raw))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def _parse_csv(raw: bytes) -> str:
    """Return raw CSV as plain text (first 5000 chars)."""
    text = raw.decode("utf-8", errors="ignore")
    return text[:5000]


_PARSERS = {
    "txt": _parse_txt,
    "md": _parse_txt,
    "csv": _parse_csv,
    "pdf": _parse_pdf,
    "docx": _parse_docx,
}


def _extract_text(uploaded_file) -> str | None:
    """Extract text from an uploaded Streamlit file object."""
    ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
    parser = _PARSERS.get(ext)
    if parser is None:
        st.error(f"Unsupported file type: .{ext}")
        return None
    raw = uploaded_file.read()
    try:
        text = parser(raw)
        return text
    except Exception as exc:
        st.error(f"Could not parse file: {exc}")
        return None


# ── Public renderer ─────────────────────────────────────────────────────────────

def render_input_section() -> tuple[str, bool]:
    """
    Render the left-column input panel with two tabs:
    1. Paste Text
    2. Upload File

    Returns (text, submitted).
    """
    st.markdown('<p class="section-label">Input</p>', unsafe_allow_html=True)

    tab_text, tab_file = st.tabs(["✏️  Paste Text", "📂  Upload File"])

    text = ""
    submitted = False

    # ── Tab 1: Paste Text ──────────────────────────────────────────────────────
    with tab_text:
        pasted = st.text_area(
            label="text_area",
            label_visibility="collapsed",
            placeholder=(
                "Paste your review, comment, survey response, or any text here...\n\n"
                "Example: "Have stayed here off and on over several years. Great location…""
            ),
            height=260,
            key="paste_input",
        )

        col_opt, col_btn = st.columns([2, 1])
        with col_opt:
            twitter_mode = st.checkbox(
                "🐦 Twitter/social-media content",
                help="Enables handling of abbreviations, hashtags, and informal language.",
                key="twitter_mode_text",
            )
        with col_btn:
            run_text = st.button("▶ Run Analysis", key="run_text", use_container_width=True)

        if run_text:
            if pasted.strip():
                text = pasted.strip()
                submitted = True
            else:
                st.warning("Please enter some text before running analysis.")

    # ── Tab 2: Upload File ─────────────────────────────────────────────────────
    with tab_file:
        st.markdown(
            f'<p style="font-size:0.82rem; color:var(--text-secondary); margin-bottom:0.6rem">'
            f"Accepted formats: {', '.join(f'<strong>.{t}</strong>' for t in ACCEPTED_TYPES)}"
            f"</p>",
            unsafe_allow_html=True,
        )

        uploaded = st.file_uploader(
            label="file_uploader",
            label_visibility="collapsed",
            type=ACCEPTED_TYPES,
            accept_multiple_files=False,
            key="file_upload",
        )

        if uploaded:
            st.markdown(
                f'<p style="font-size:0.82rem; color:var(--accent)">📄 {uploaded.name}</p>',
                unsafe_allow_html=True,
            )

        col_opt2, col_btn2 = st.columns([2, 1])
        with col_opt2:
            twitter_mode_f = st.checkbox(
                "🐦 Twitter/social-media content",
                help="Enables handling of abbreviations, hashtags, and informal language.",
                key="twitter_mode_file",
            )
        with col_btn2:
            run_file = st.button("▶ Run Analysis", key="run_file", use_container_width=True)

        if run_file:
            if uploaded is None:
                st.warning("Please upload a file before running analysis.")
            else:
                extracted = _extract_text(uploaded)
                if extracted and extracted.strip():
                    text = extracted.strip()
                    submitted = True
                    st.success(f"Extracted {len(text):,} characters from {uploaded.name}")
                else:
                    st.error("Could not extract text from the uploaded file.")

    # Word / char counters for paste tab
    if text:
        word_count = len(text.split())
        st.markdown(
            f'<p style="font-size:0.78rem; color:var(--text-secondary); margin-top:0.4rem">'
            f"📊 {word_count:,} words · {len(text):,} characters"
            f"</p>",
            unsafe_allow_html=True,
        )

    return text, submitted
