# SentiScope — Sentiment Analysis App

Professional, modular sentiment analysis application built with Streamlit and powered by Claude AI.

## Features

- **Dark / Light theme** toggle — matches the reference design
- **Two input modes**: paste text directly or upload a file (`.txt`, `.md`, `.csv`, `.pdf`, `.docx`)
- **Rich results grid**: overall sentiment pill, confidence, positive/neutral/negative scores, emotion breakdown with bars, aspect-level sentiment tags, key phrases
- **Emoji-annotated output** for instant visual communication
- Modular codebase — easy to extend

## Project Structure

```
sentiment_app/
├── app.py                  # Entry point
├── requirements.txt
└── modules/
    ├── __init__.py
    ├── ui_config.py        # Theme CSS, header, footer
    ├── input_handler.py    # Text paste + file upload tabs
    ├── analyzer.py         # Claude API call + JSON parsing
    └── results_display.py  # Results grid rendering
```

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Run
streamlit run app.py
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ | Your Anthropic API key |

## Customization

- **Colors / tokens** → `modules/ui_config.py` → `THEMES` dict
- **Supported file types** → `modules/input_handler.py` → `ACCEPTED_TYPES`
- **Analysis schema** → `modules/analyzer.py` → `_SYSTEM` prompt
- **Result layout** → `modules/results_display.py`

## Scaling Notes

- Text is truncated at 8,000 characters before sending to the API (configurable in `analyzer.py`)
- For batch processing, wrap `analyze_sentiment()` in an async queue
- Deploy with `streamlit run app.py --server.port 8080 --server.address 0.0.0.0`
