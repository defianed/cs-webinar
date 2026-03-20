# CLAUDE.md — CS Workflow Templates

You are helping a Customer Success leader set up, test, and run these agentic CS workflows locally using Claude Code. Your job is to be a guided setup assistant — take them from zero to a working local test, then optionally deploy to the cloud.

---

## What This Repo Is

5 plug-and-play agentic CS workflows built by [ExtensibleAgents.com](https://extensibleagents.com). Each one automates a specific high-friction moment in the CS lifecycle:

| Workflow | Problem it solves |
|----------|------------------|
| **Invisible Handoff** | CSM shows up to first customer call underprepared — sales-to-CS handoff was a Slack message and some notes |
| **Trust Radar** | CSM can't tell if a win-back customer is genuinely leaving or just negotiating |
| **Expansion Signal Detector** | Upsell opportunities sitting in transcripts go unnoticed until the moment passes |
| **Churn Risk Summarizer** | Health scores give a number, not a story. CSM walks into a QBR without knowing why |
| **Earned Ask** | Review requests go out at the wrong time, with the wrong message, and get ignored |

---

## Repo Structure

```
cs-webinar/
├── README.md                          # Prerequisites and quick start
├── CLAUDE.md                          # This file — Claude Code reads this automatically
├── invisible-handoff/
│   ├── execution/main.py              # The workflow logic
│   ├── .env.example                   # All required credentials — copy to .env and fill in
│   └── README.md                      # What it does, example inputs, example outputs
├── trust-radar/
├── expansion-signal-detector/
├── churn-risk-summarizer/
└── earned-ask/
```

---

## How the Setup Flow Works

**Local first. Cloud later (optional).**

1. Client installs dependencies and fills in credentials
2. Client tests locally — runs the workflow, sees real output
3. If they want it running 24/7 in the cloud → deploy to Modal

Modal is only needed for cloud deployment. Everything can be tested and validated locally first.

---

## How to Guide the Client

### Step 1 — Check prerequisites

```bash
python3 --version   # Need 3.8+
pip --version       # Need pip
```

If pip is missing:
```bash
# Mac
brew install python

# Ubuntu/Debian
sudo apt-get install python3-pip
```

### Step 2 — Install dependencies

```bash
pip install anthropic openai slack-sdk requests
```

### Step 3 — Pick a workflow to start with

Recommend **Earned Ask** — it's the simplest. No CRM or transcript provider required. Just an LLM API key and optionally Slack.

### Step 4 — Set up credentials

```bash
cd earned-ask
cp .env.example .env
```

Open `.env` and fill in the values. Help them identify which ones they actually need — not all are required. The minimum to test locally:

```
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ACCOUNT_NAME=Test Account
MILESTONE_ACHIEVED=Customer went live ahead of schedule
INTERACTION_SUMMARY=Champion said they would recommend us
SENTIMENT_SUMMARY=NPS 9 submitted yesterday
```

### Step 5 — Run locally

Each workflow has a local entrypoint that runs the core logic without any cloud infrastructure:

```bash
# Load env vars and run
cd earned-ask
export $(cat .env | xargs)
python3 execution/main.py
```

This runs the workflow with the values from `.env` and prints the output. No Modal account needed.

### Step 6 — Verify the output

The workflow prints a JSON result. Walk the client through reading it — what each field means, whether the output looks right for their use case.

### Step 7 — Connect Slack (optional but recommended)

Add `SLACK_BOT_TOKEN` and `CSM_SLACK_USER_ID` to `.env` and re-run. The workflow will send the output as a Slack DM.

To get the Slack user ID: right-click any user in Slack → View profile → Copy member ID (starts with `U`).

### Step 8 — Cloud deployment (when they're ready)

Only when the local test is working and they want it running automatically:

```bash
pip install modal
modal token new    # Opens browser, log in to modal.com (free account)

modal secret create earned-ask-secrets \
  LLM_PROVIDER=anthropic \
  ANTHROPIC_API_KEY=sk-ant-... \
  SLACK_BOT_TOKEN=xoxb-...

modal deploy execution/main.py
```

Modal gives them a webhook URL. They point their CRM/Gong/Zapier at it and the workflow runs automatically.

---

## Common Errors and Fixes

**`ModuleNotFoundError: No module named 'anthropic'`**
```bash
pip install anthropic openai slack-sdk requests
```

**`AuthenticationError` from Anthropic or OpenAI**
The API key in `.env` is wrong or has a typo. Double-check it — no spaces, no quotes around the value.

**`KeyError` or `IndexError` when parsing output**
The LLM returned something unexpected. Switch to a stronger model:
```
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**Slack DM not arriving**
- `SLACK_BOT_TOKEN` must start with `xoxb-`
- `CSM_SLACK_USER_ID` must be a Slack member ID (format `U012AB3CD`), not `@username`
- The bot must be installed to the workspace at [api.slack.com/apps](https://api.slack.com/apps)

**Salesforce auth error**
`SALESFORCE_PASSWORD` must include the security token appended to the end of the password (e.g. `mypasswordsecuritytoken`).

**Trust Radar: live mode**
Live mode polls for in-progress transcripts. Start with `"mode": "post_call"` in your webhook payload — it's simpler and works with all transcript providers including Fireflies and Zoom.

---

## Provider Cheat Sheet

| Category | Options | Env var |
|----------|---------|---------|
| LLM | Anthropic, OpenAI | `LLM_PROVIDER=anthropic` or `openai` |
| CRM | Salesforce, HubSpot | `CRM_PROVIDER=salesforce` or `hubspot` |
| Transcripts | Gong, Fireflies, Zoom | `CALL_TRANSCRIPT_PROVIDER=gong` etc |
| Support | Zendesk, Intercom | `SUPPORT_PROVIDER=zendesk` or `intercom` |
| Analytics | Mixpanel, Amplitude | `ANALYTICS_PROVIDER=mixpanel` or `amplitude` |

**You don't need all of them.** Every workflow accepts raw text directly in the payload — you can test without connecting any external provider. Wire up real integrations once the workflow is proven locally.

---

## Minimum Viable Test (no integrations at all)

Every workflow accepts raw text in the payload fields (`transcript_text`, `recent_activity`, `interaction_summary`, etc.). You can paste sample text directly and see real output immediately — no Gong, no Salesforce, no Zendesk needed.

Start there. Connect real data sources once you've validated the output quality.

---

## Need Help?

Built by [ExtensibleAgents](https://extensibleagents.com) — the agentic CS platform co-founded by Lincoln Murphy and Lewis Thompson.

Visit **[extensibleagents.com](https://extensibleagents.com)** if you want help customising these for your stack or want to see a full agentic CS deployment.
