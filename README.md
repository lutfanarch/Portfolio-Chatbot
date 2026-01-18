# Interactive Portfolio Bot (Streamlit) — Lutfan Haziq

This is a beginner-friendly, evidence-first portfolio chatbot intended for DAE portfolio submission.

**Design principle:** no LLM is used in the MVP, so the bot does not hallucinate. It answers strictly from `profile.json`.

## What is included
- `app.py` — Streamlit app (chat UI + admissions pages)
- `profile.json` — your editable portfolio data
- `CHANGELOG.md` — optional notes (not shown in-app)
- `requirements.txt` — dependencies

## Run locally
### 1) Create and activate virtual environment
Windows:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Run
```bash
streamlit run app.py
```

## Customize content
Edit `profile.json`.
- Replace `TBD` with real links (GitHub repo links and Streamlit demo).
- Keep all claims honest and verifiable.

## Privacy
- This repo/app intentionally avoids publishing certificates or sensitive personal identifiers.
- If you add images under assets/, ensure they are redacted before committing.

## Suggested proof-of-work
- Commit daily to GitHub
- Add screenshots under `assets/screenshots/`

## Deployment (Streamlit Community Cloud)
1) Push this repo to GitHub
2) Deploy from Streamlit Community Cloud
3) Ensure `app.py`, `requirements.txt`, and `profile.json` are in the repo root
