# Agentic CS Workflows — Setup & Usage Guide

## If a user just cloned this repo and says "set me up" or "get me started"

Run the full setup flow conversationally. Ask questions one at a time, wait for answers, then move to the next. Do not dump all questions at once.

### Setup flow (ask in this order):

**Step 1 — LLM API key**
Ask: "First, we need an AI API key to power the workflows. Do you have an Anthropic key (starts with sk-ant-) or an OpenAI key (starts with sk-proj-)? If you don't have one yet, get it from https://console.anthropic.com — it takes 2 minutes."

Wait for them to paste their key. Write it to `.env` in the repo root:
```
ANTHROPIC_API_KEY=their_key
ANTHROPIC_MODEL=claude-opus-4-6
```
(or OPENAI_API_KEY if they gave you that instead)

**Step 2 — Run a test immediately**
Say: "Great — let me make sure that works before we go any further."

Run: `python3 churn-risk-summarizer/test.py`

If it works, show them the output and say: "That's the churn risk workflow running on a sample account. You just saw your first agentic CS workflow."
If it fails, diagnose and fix before continuing.

**Step 3 — Business info**
Ask these one at a time:
- "What's your company name?"
- "What's your name?"
- "What CS tool or CRM do you use? (e.g. Salesforce, HubSpot, or none)"
- "Do you record calls? If so, what tool? (e.g. Gong, Fireflies, Fathom, Zoom, or none)"
- "Do you use a support ticketing tool? (e.g. Zendesk, Intercom, or none)"

Write their answers into `config.yaml` in each workflow folder.

**Step 4 — Slack (output destination)**
Ask: "Where do you want workflow results delivered? The easiest option is Slack — it posts a message to a channel when a workflow runs. Do you want to set that up? (yes/no)"

If yes:
- "Paste your Slack bot token (starts with xoxb-). Create one at https://api.slack.com/apps if you don't have one."
- "Which Slack channel should results go to? (e.g. #cs-alerts)"

Write to `.env`:
```
SLACK_BOT_TOKEN=their_token
```
Write `slack_channel` to each config.yaml.

If no: "No problem — results will print to the terminal for now. You can add Slack any time by editing .env."

**Step 5 — Run a real workflow**
Say: "You're set up. Let's run a real workflow on the sample data so you can see the full output."

Run: `python3 churn-risk-summarizer/local.py`

Show them the output. Explain what they're seeing.

Then say: "You've got 5 workflows in this repo. Here's what each one does:
- **churn-risk-summarizer** — reads account data and flags churn risk with a recommended action
- **expansion-signal-detector** — reads a call transcript and identifies expansion opportunities
- **earned-ask** — tells you when the moment is right to ask for a referral, case study, or upsell
- **invisible-handoff** — creates a full account brief when a CSM handoff happens
- **trust-radar** — monitors for early signs of trust erosion across an account

To run any of them: `python3 <workflow-name>/local.py`
To connect your real tools (Salesforce, Gong, etc): edit the config.yaml in the workflow folder."

---

## If a user asks "how do I run a workflow on my own data"

Tell them:
1. Edit the `config.yaml` in the workflow folder — set `crm_provider`, `transcript_provider` etc to their tool (or `manual` to paste data directly)
2. If using manual: put their data in the `sample_data/` folder (replace the example files)
3. Run `python3 local.py` from inside the workflow folder

---

## If a user asks "how do I add a new provider" (e.g. Fathom)

The provider pattern is in `local.py`. To add Fathom:
1. Add `FATHOM_API_KEY` to `.env`
2. In `local.py`, add a `fetch_transcript_fathom()` function
3. In the provider routing block, add: `elif transcript_provider == "fathom": transcript = fetch_transcript_fathom(...)`
4. Add `fathom` as an option in `config.yaml` comment

---

## Workflow structure

Every workflow has the same structure:
```
<workflow-name>/
├── test.py          # Runs instantly, zero setup, uses sample data
├── local.py         # Full workflow, needs .env configured
├── config.yaml      # Non-secret settings (providers, account info)
├── sample_data/     # Realistic dummy data for testing
├── examples/        # Sample outputs so you know what to expect
├── execution/
│   └── main.py      # Modal deploy version (production cloud)
└── requirements.txt
```

## Three run modes

| Mode | Command | Needs |
|------|---------|-------|
| Demo | `python3 test.py` | Nothing — runs immediately |
| Local | `python3 local.py` | `.env` with API key + Slack token |
| Production | `modal deploy execution/main.py` | Modal account + secrets |

---

## .env reference (repo root, covers all workflows)

```
# Required
ANTHROPIC_API_KEY=          # or OPENAI_API_KEY
SLACK_BOT_TOKEN=            # xoxb-...

# Optional — only needed for live integrations
SALESFORCE_INSTANCE_URL=
SALESFORCE_ACCESS_TOKEN=
HUBSPOT_PRIVATE_APP_TOKEN=
GONG_ACCESS_KEY=
GONG_ACCESS_KEY_SECRET=
FIREFLIES_API_KEY=
ZENDESK_SUBDOMAIN=
ZENDESK_EMAIL=
ZENDESK_API_TOKEN=
NOTION_API_KEY=
```
