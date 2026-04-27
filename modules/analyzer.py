"""
analyzer.py — Sentiment analysis via Claude API
Returns a structured dict with scores, aspects, emotions, summary.
"""

import json
import re
import anthropic


# ── Anthropic client ────────────────────────────────────────────────────────────
_client = anthropic.Anthropic()

# ── System prompt ───────────────────────────────────────────────────────────────
_SYSTEM = """You are an expert sentiment analysis engine. Analyze the provided text and return ONLY a valid JSON object — no markdown fences, no preamble.

The JSON must follow this exact schema:
{
  "overall_sentiment": "Positive" | "Negative" | "Neutral" | "Mixed",
  "confidence": <float 0.0–1.0>,
  "scores": {
    "positive": <float 0.0–1.0>,
    "neutral": <float 0.0–1.0>,
    "negative": <float 0.0–1.0>
  },
  "emotions": [
    {"label": "<emotion>", "score": <float 0.0–1.0>, "emoji": "<single emoji>"}
  ],
  "aspects": [
    {"aspect": "<topic phrase>", "sentiment": "positive" | "negative" | "neutral", "emoji": "<single emoji>"}
  ],
  "key_phrases": ["<phrase>", ...],
  "summary": "<2-sentence human-readable summary of the sentiment>",
  "tone": "<one-word descriptor e.g. Appreciative / Critical / Ambivalent / Enthusiastic>"
}

Rules:
- Scores in `scores` must sum to exactly 1.0
- Include 3–6 emotions, sorted by score descending
- Include 3–8 aspect-level sentiments extracted from the text
- Use relevant emojis from Unicode (e.g. 😊 😡 😐 🏨 🚿 📍 etc.)
- Return ONLY the JSON object, nothing else
"""


def analyze_sentiment(text: str) -> dict:
    """
    Call Claude API and return parsed sentiment analysis dict.
    Falls back to a minimal error dict if parsing fails.
    """
    # Truncate very long texts to stay within token limits
    truncated = text[:8000] if len(text) > 8000 else text

    try:
        message = _client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=_SYSTEM,
            messages=[{"role": "user", "content": truncated}],
        )

        raw = message.content[0].text.strip()

        # Strip any accidental markdown fences
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        result = json.loads(raw)
        result["_raw_text"] = truncated
        return result

    except json.JSONDecodeError as exc:
        return _error_result(f"JSON parse error: {exc}", truncated)
    except Exception as exc:
        return _error_result(str(exc), truncated)


def _error_result(reason: str, text: str) -> dict:
    return {
        "overall_sentiment": "Unknown",
        "confidence": 0.0,
        "scores": {"positive": 0.33, "neutral": 0.34, "negative": 0.33},
        "emotions": [],
        "aspects": [],
        "key_phrases": [],
        "summary": f"Analysis failed: {reason}",
        "tone": "Unknown",
        "_raw_text": text,
        "_error": True,
    }
