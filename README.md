# AI Marketing Copilot

A lightweight AI marketing workflow prototype that turns a raw brief into an executable campaign plan, and analyzes competitor communication materials to identify white-space opportunities.

## What it does

### 1) Campaign Generator
Input brand/product, objective, audience, channels, budget, timeline and brief materials. The app generates:
- consumer insight
- Big Idea
- message architecture
- channel roles
- execution rhythm
- budget allocation
- KPI framework
- risks and assumptions
- one-page campaign summary

### 2) Competitor Analyzer
Paste competitor campaign / social / PR materials. The app extracts:
- communication themes
- audience and scenario differences
- channel/content tactics
- common patterns and homogeneity
- communication white space
- recommended actions

## Product principle

This tool is designed to automate repetitive first-pass work, not replace human judgment. It explicitly asks the model to mark unsupported assumptions as `待验证` instead of inventing market facts.

## Run locally

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\\Scripts\\Activate.ps1

pip install -r requirements.txt
streamlit run app.py
```

## Add your API key

You can paste your OpenAI API key into the app sidebar during a session, or create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your_key_here"
OPENAI_MODEL = "gpt-5.6"
```

Do **not** commit `secrets.toml` or your API key to GitHub.

## Deploy on Streamlit Community Cloud

1. Push this folder to a public or private GitHub repository.
2. In Streamlit Community Cloud, create a new app from the repo.
3. Set the entry point to `app.py`.
4. Add `OPENAI_API_KEY` and optionally `OPENAI_MODEL` in app Secrets.
5. Deploy and share the generated webpage URL.

## Suggested demo

Use the built-in **Demo** button in Campaign Generator. This lets reviewers see the product experience even without entering an API key.

## Tech stack

- Python
- Streamlit
- OpenAI Responses API

## Why this project

Marketing work often spends substantial time on brief structuring, competitor synthesis and first-pass strategy framing. This prototype turns those repetitive steps into an AI-assisted workflow so marketers can spend more time on judgment, creativity and execution.
