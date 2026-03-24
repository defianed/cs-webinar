# Expansion Signal Detector

## Quick Start
1. Clone this repo
2. `cd expansion-signal-detector`
3. `python3 test.py` — see it work instantly (no setup needed)
4. Copy `.env.example` to `.env`, add your API key, run again with real AI

---

An intelligent text processor for expansion signals. You paste a transcript or post-call notes as text — the AI identifies buying signals and blockers and surfaces the upsell opportunity. Optionally alerts the CSM via Slack.

> **How it works:** You provide the call context. The AI reads it and identifies expansion signals. No live Gong or CRM connection required — connect real integrations once the output quality is proven.

## What it does
- Reads transcript text or post-call notes you provide
- Identifies buying signals and expansion blockers
- Summarises why the account may be ready to expand
- Optionally sends the CSM a Slack alert with a suggested next action

## Providers supported
- LLM: Anthropic (Claude) or OpenAI (GPT)
- Notifications: Slack (optional)
- CRM: Salesforce or HubSpot (optional — for live data pull once integrated)
- Transcript: Gong or Fireflies (optional — or pass raw text directly)

---


## Prerequisites

- Python 3.8+, pip, and Modal CLI installed — see the [main README](../README.md) for setup
- A Modal account (free tier works): [modal.com](https://modal.com)
- An LLM API key: Anthropic ([console.anthropic.com](https://console.anthropic.com)) or OpenAI ([platform.openai.com](https://platform.openai.com))
- A Slack bot token with permission to send DMs: [api.slack.com/apps](https://api.slack.com/apps)


## Setup

### 1. Configure your environment

```bash
cp .env.example .env
# Fill in your credentials
```

### 2. Create a Modal secret

```bash
modal secret create expansion-signal-detector-secrets \
  LLM_PROVIDER=anthropic \
  ANTHROPIC_API_KEY=sk-ant-... \
  SLACK_BOT_TOKEN=xoxb-...
```

### 3. Deploy

```bash
modal deploy execution/main.py
```

### 4. Trigger the workflow

Send a POST to your Modal webhook after a call or note is logged:

```json
{
  "account_id": "0015g00000AbCdEf",
  "account_name": "Acme Corp",
  "csm_slack_user_id": "U012AB3CD",
  "transcript_text": "Customer mentioned they're rolling out to the EMEA team next quarter and asked if we have multi-region support...",
  "post_call_notes": "Sarah asked about API rate limits for higher volume. Team is growing fast."
}
```

**Minimum required:** `account_id` or `account_name` + either `transcript_text` or `post_call_notes`.

---

## Test locally

```bash
# No setup needed — shows mock output immediately
python3 test.py

# With a real API key
ANTHROPIC_API_KEY=sk-ant-... python3 test.py
```

---

## Example output

```json
{
  "status": "ok",
  "workflow": "expansion-signal-detector",
  "account_name": "Acme Corp",
  "result": {
    "ready_for_expansion": true,
    "confidence": "high",
    "buying_signals": [
      "Explicitly asked about enterprise tier pricing",
      "Mentioned EMEA rollout starting next quarter",
      "Asked about API rate limits suggesting higher volume",
      "Referenced bringing in 2 additional teams"
    ],
    "blockers": [
      "Budget approval needed from CFO",
      "IT security review not started"
    ],
    "recommended_next_action": "Schedule a discovery call focused on enterprise tier — customer is signalling intent. Come prepared with volume pricing and multi-region specs.",
    "summary": "Acme is showing strong expansion signals. They're planning a 3-region rollout and proactively asked about enterprise features and limits. Budget and IT are the only blockers. This is a high-confidence expansion opportunity — act within 2 weeks."
  }
}
```

---

## Required env vars

| Var | Required | Description |
|-----|----------|-------------|
| `LLM_PROVIDER` | Yes | `anthropic` or `openai` |
| `ANTHROPIC_API_KEY` | If anthropic | Claude API key |
| `OPENAI_API_KEY` | If openai | OpenAI API key |
| `SLACK_BOT_TOKEN` | Yes | Bot token for CSM notifications |
| `CRM_PROVIDER` | Optional | `salesforce` or `hubspot` |
