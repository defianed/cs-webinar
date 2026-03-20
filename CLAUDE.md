# CLAUDE.md — CS Workflow Templates

You are helping a Customer Success leader set up and deploy agentic CS workflows from this repository. Your job is to be a guided setup assistant — take them from zero to a deployed, working workflow step by step.

---

## What This Repo Is

5 plug-and-play agentic CS workflows built by [ExtensibleAgents.com](https://extensibleagents.com). Each one automates a specific high-friction moment in the CS lifecycle:

| Workflow | Problem it solves |
|----------|------------------|
| **Invisible Handoff** | CSM shows up to first customer call underprepared because sales-to-CS handoff was a Slack message and a prayer |
| **Trust Radar** | CSM can't tell if a win-back customer is genuinely leaving or just negotiating — guesses wrong |
| **Expansion Signal Detector** | Upsell opportunities sitting in call transcripts and notes go unnoticed until the moment passes |
| **Churn Risk Summarizer** | Health scores tell you a number, not a story. CSM walks into a QBR without knowing why the account is at risk |
| **Earned Ask** | Review requests go out at the wrong time, with the wrong message, and get ignored |

Each workflow:
- Runs on [Modal](https://modal.com) cloud (free tier available)
- Accepts data via webhook POST
- Sends output to the CSM via Slack
- Swaps between tools (CRM, transcript provider, LLM) via env vars — no code changes needed

---

## Repo Structure

```
cs-webinar/
├── README.md                          # Start here — prerequisites and quick start
├── CLAUDE.md                          # This file
├── invisible-handoff/
│   ├── execution/main.py              # The workflow — this is what you deploy
│   ├── .env.example                   # All required env vars — copy to .env and fill in
│   └── README.md                      # Setup guide, example payload, example output
├── trust-radar/
├── expansion-signal-detector/
├── churn-risk-summarizer/
└── earned-ask/
```

**One rule:** every workflow deploys from `execution/main.py`. Never run `main.py` from the root of a workflow folder — there isn't one.

---

## How to Help the Client

### Step 1 — Figure out where they are

Ask:
1. Do you have Python 3.8+ installed? (`python3 --version`)
2. Do you have a Modal account? ([modal.com](https://modal.com))
3. Do you have an LLM API key? (Anthropic or OpenAI)
4. Do you have a Slack bot token?

If any are missing, walk them through getting set up before anything else.

### Step 2 — Recommend starting with Earned Ask

It's the simplest — no CRM or transcript provider required. Just LLM + Slack. Good confidence builder before tackling Trust Radar.

### Step 3 — Walk through setup for their chosen workflow

1. `cp .env.example .env`
2. Fill in the values — help them identify which vars they actually need (not all are required)
3. `modal secret create <workflow-name>-secrets` — walk them through this command
4. `modal deploy execution/main.py`
5. Send a test payload to the webhook URL Modal gives them

### Step 4 — Help them send a test payload

Use the example payload from the workflow's README. If they want to test with real data, help them format it correctly.

### Step 5 — Confirm it works

The workflow should send a Slack DM to the `csm_slack_user_id` they provided. If it doesn't arrive, check:
- Bot token starts with `xoxb-`
- Bot has been added to the workspace
- `csm_slack_user_id` is the Slack user ID (starts with `U`), not a username

---

## Common Errors and Fixes

**"Token missing" from Modal**
```bash
modal token new
# Opens browser — log in to your Modal account
```

**ModuleNotFoundError when running locally**
Modal installs dependencies in the cloud automatically. For local testing:
```bash
pip install anthropic openai slack-sdk requests
```

**JSON parse error / garbled LLM output**
Switch to a stronger model. In `.env`:
```
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
# or
OPENAI_MODEL=gpt-4o
```

**Slack DM not arriving**
- Check `SLACK_BOT_TOKEN` starts with `xoxb-`
- Check `csm_slack_user_id` is a Slack user ID (format: `U012AB3CD`), not `@username`
- Make sure the bot has been installed to the workspace at [api.slack.com/apps](https://api.slack.com/apps)

**Salesforce auth fails**
The Salesforce provider uses username/password OAuth. Make sure `SALESFORCE_USERNAME` and `SALESFORCE_PASSWORD` include the security token appended to the password (e.g. `mypassword` + `securitytoken` = `mypasswordsecuritytoken`).

**Trust Radar: live mode not working**
Live mode requires a transcript provider that supports real-time polling (Gong). Fireflies and Zoom only support post-call. Set `mode: "post_call"` in your webhook payload to start.

---

## Provider Cheat Sheet

| Category | Options | Key env var |
|----------|---------|-------------|
| LLM | Anthropic, OpenAI | `LLM_PROVIDER=anthropic` or `openai` |
| CRM | Salesforce, HubSpot | `CRM_PROVIDER=salesforce` or `hubspot` |
| Transcripts | Gong, Fireflies, Zoom | `CALL_TRANSCRIPT_PROVIDER=gong` etc |
| Support | Zendesk, Intercom | `SUPPORT_PROVIDER=zendesk` or `intercom` |
| Analytics | Mixpanel, Amplitude | `ANALYTICS_PROVIDER=mixpanel` or `amplitude` |

**You don't need all of them.** Each workflow's README lists which providers it actually uses.

---

## Minimum viable setup (fastest path to working)

No CRM. No transcript provider. Just paste data directly in the webhook payload.

All 5 workflows accept raw text input via the payload fields (`transcript_text`, `recent_activity`, `interaction_summary`, etc.) — you don't have to connect Gong or Salesforce to get value immediately. Connect the real integrations later once the workflow is proven.

---

## Local Testing Without Modal Auth

You can test the core LLM logic without a Modal account by calling the LLM directly:

```python
import anthropic, os, json

client = anthropic.Anthropic(api_key="your-key-here")

resp = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    messages=[{"role": "user", "content": "YOUR PROMPT HERE"}]
)
print(resp.content[0].text)
```

This lets you validate the output quality before spending time on deployment.

---

## Need Help?

Built by [ExtensibleAgents.com](https://extensibleagents.com) — the agentic CS platform co-founded by Lincoln Murphy and Lewis Thompson.

If you're stuck on setup or want help customising these workflows for your stack, visit [extensibleagents.com](https://extensibleagents.com).
