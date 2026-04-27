"""
results_display.py — Render sentiment analysis results in the right column
"""

import streamlit as st


# ── Sentiment → emoji + color mapping ──────────────────────────────────────────
_SENTIMENT_META = {
    "Positive":  {"emoji": "😊", "color": "#6fcf6f", "bg": "rgba(45,106,45,0.18)"},
    "Negative":  {"emoji": "😞", "color": "#cf6f6f", "bg": "rgba(106,45,45,0.18)"},
    "Neutral":   {"emoji": "😐", "color": "#9a9a9a", "bg": "rgba(80,80,80,0.18)"},
    "Mixed":     {"emoji": "🤔", "color": "#f0c040", "bg": "rgba(140,100,0,0.18)"},
    "Unknown":   {"emoji": "❓", "color": "#9a9a9a", "bg": "rgba(80,80,80,0.18)"},
}

_ASPECT_CLASS = {"positive": "pos", "negative": "neg", "neutral": "neu"}
_ASPECT_EMOJI = {"positive": "✅", "negative": "❌", "neutral": "➖"}


def _pct(score: float) -> str:
    return f"{score * 100:.0f}%"


def _bar(score: float, color: str) -> None:
    """Render a custom progress bar."""
    filled = int(score * 100)
    st.markdown(
        f"""
        <div style="
            background: var(--border);
            border-radius: 4px;
            height: 6px;
            width: 100%;
            margin-top: 4px;
        ">
            <div style="
                background: {color};
                width: {filled}%;
                height: 100%;
                border-radius: 4px;
                transition: width 0.4s ease;
            "></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_results(results: dict, original_text: str) -> None:
    """Render the full results panel."""

    sentiment = results.get("overall_sentiment", "Unknown")
    meta = _SENTIMENT_META.get(sentiment, _SENTIMENT_META["Unknown"])
    confidence = results.get("confidence", 0)
    scores = results.get("scores", {})
    emotions = results.get("emotions", [])
    aspects = results.get("aspects", [])
    key_phrases = results.get("key_phrases", [])
    summary = results.get("summary", "")
    tone = results.get("tone", "")

    st.markdown('<p class="section-label">Results</p>', unsafe_allow_html=True)

    # ── Sentiment pill + confidence ────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="result-card" style="border-color: {meta['color']}44;">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;">
                <div class="sentiment-pill" style="color:{meta['color']}; border-color:{meta['color']}; background:{meta['bg']};">
                    {meta['emoji']}&nbsp;&nbsp;{sentiment}
                </div>
                <div style="text-align:right;">
                    <div class="score-label">CONFIDENCE</div>
                    <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800; color:{meta['color']};">
                        {_pct(confidence)}
                    </div>
                </div>
            </div>
            <div style="margin-top:0.7rem; font-size:0.88rem; color:var(--text-secondary); line-height:1.6;">
                {summary}
            </div>
            {"" if not tone else f'<div style="margin-top:0.6rem;"><span class="aspect-tag" style="font-size:0.78rem;">🎭 Tone: <strong>{tone}</strong></span></div>'}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Score grid ─────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="score-grid">
            <div class="score-item">
                <div class="score-label">Positive</div>
                <div class="score-value" style="color:#6fcf6f;">{_pct(scores.get('positive',0))}</div>
                <div class="score-emoji">😊</div>
            </div>
            <div class="score-item">
                <div class="score-label">Neutral</div>
                <div class="score-value" style="color:#9a9a9a;">{_pct(scores.get('neutral',0))}</div>
                <div class="score-emoji">😐</div>
            </div>
            <div class="score-item">
                <div class="score-label">Negative</div>
                <div class="score-value" style="color:#cf6f6f;">{_pct(scores.get('negative',0))}</div>
                <div class="score-emoji">😞</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Emotion bars ───────────────────────────────────────────────────────────
    if emotions:
        with st.expander("🎭 Emotion Breakdown", expanded=True):
            for emo in emotions[:6]:
                label = emo.get("label", "")
                score = emo.get("score", 0)
                emoji = emo.get("emoji", "")
                col_l, col_r = st.columns([3, 1])
                with col_l:
                    st.markdown(
                        f'<span style="font-size:0.88rem; color:var(--text-primary);">'
                        f'{emoji} {label}</span>',
                        unsafe_allow_html=True,
                    )
                    _bar(score, "var(--accent)")
                with col_r:
                    st.markdown(
                        f'<div style="text-align:right; padding-top:0.2rem; '
                        f'font-family:Syne,sans-serif; font-size:0.95rem; '
                        f'font-weight:700; color:var(--accent);">{_pct(score)}</div>',
                        unsafe_allow_html=True,
                    )

    # ── Aspect-level sentiments ────────────────────────────────────────────────
    if aspects:
        st.markdown('<p class="section-label" style="margin-top:0.8rem;">Aspect Sentiments</p>', unsafe_allow_html=True)
        tags_html = "".join(
            f'<span class="aspect-tag {_ASPECT_CLASS.get(a.get("sentiment","neu"), "neu")}">'
            f'{a.get("emoji", _ASPECT_EMOJI.get(a.get("sentiment","neutral"), "➖"))} '
            f'{a.get("aspect","")}</span>'
            for a in aspects
        )
        st.markdown(
            f'<div class="result-card"><div class="aspect-grid">{tags_html}</div></div>',
            unsafe_allow_html=True,
        )

    # ── Key phrases ────────────────────────────────────────────────────────────
    if key_phrases:
        st.markdown('<p class="section-label" style="margin-top:0.8rem;">Key Phrases</p>', unsafe_allow_html=True)
        phrases_html = "".join(
            f'<span class="aspect-tag">💬 {phrase}</span>'
            for phrase in key_phrases[:10]
        )
        st.markdown(
            f'<div class="result-card"><div class="aspect-grid">{phrases_html}</div></div>',
            unsafe_allow_html=True,
        )

    # ── Analysed text preview ─────────────────────────────────────────────────
    with st.expander("📄 Analyzed Text Preview"):
        preview = original_text[:600] + ("…" if len(original_text) > 600 else "")
        st.markdown(
            f'<div style="font-size:0.85rem; color:var(--text-secondary); '
            f'line-height:1.7; font-style:italic;">{preview}</div>',
            unsafe_allow_html=True,
        )

    # ── Error notice ───────────────────────────────────────────────────────────
    if results.get("_error"):
        st.error("⚠️ Analysis encountered an error. Results may be incomplete.")
