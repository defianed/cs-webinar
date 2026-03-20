# Expansion Signal Detector

Scans call transcripts and post-call notes for language that signals a customer is ready to expand. Surfaces the upsell opportunity before it passes.

## What it does
- Reads the latest customer conversation context (transcript or notes)
- Identifies buying signals and expansion blockers
- Summarises why the account may be ready to expand
- Sends the CSM a Slack alert with a suggested next action

## Providers supported
- CRM: Salesforce or HubSpot (context enrichment)
- Transcript: Gong or Fireflies (or pass raw text directly)
- LLM: Anthropic (Claude) or OpenAI (GPT)
- Notifications: Slack

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
ACCOUNT_NAME="Acme Corp" \
TRANSCRIPT_TEXT="We're expanding to 3 new regions next quarter and want to understand your enterprise tier..." \
modal run execution/main.py
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
