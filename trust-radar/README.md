# Trust Radar

## Quick Start
1. Clone this repo
2. `cd trust-radar`
3. `python3 test.py` — see it work instantly (no setup needed)
4. Copy `.env.example` to `.env`, add your API key, run again with real AI

---

Analyses a win-back or escalation call and tells the CSM whether they're dealing with genuine loss of trust, negotiation pressure, mixed signals, or unclear evidence.

## What it does
- Pulls CRM context and support history
- Reads the call transcript (live or post-call)
- Classifies trust status with confidence score and evidence
- Sends the CSM a Slack alert with recommended strategy

## Providers supported
- CRM: Salesforce or HubSpot
- Transcript: Gong, Fireflies, or Zoom
- Support context: Zendesk or Intercom
- LLM: Anthropic (Claude) or OpenAI (GPT)


## Prerequisites

- Python 3.8+, pip, and Modal CLI installed — see the [main README](../README.md) for setup
- A Modal account (free tier works): [modal.com](https://modal.com)
- An LLM API key: Anthropic ([console.anthropic.com](https://console.anthropic.com)) or OpenAI ([platform.openai.com](https://platform.openai.com))
- A Slack bot token with permission to send DMs: [api.slack.com/apps](https://api.slack.com/apps)


## Classifications
- `GENUINE_LOSS_OF_TRUST` — Real relationship damage, needs repair before anything else
- `NEGOTIATING` — Customer is using dissatisfaction as leverage for concessions
- `MIXED` — Genuine frustration with openness to repair
- `UNCLEAR` — Not enough signal to classify confidently

---

## Setup

### 1. Configure your environment

```bash
cp .env.example .env
# Fill in your credentials
```

### 2. Create a Modal secret

```bash
modal secret create trust-radar-secrets \
  LLM_PROVIDER=anthropic \
  ANTHROPIC_API_KEY=sk-ant-... \
  SLACK_BOT_TOKEN=xoxb-... \
  CRM_PROVIDER=salesforce \
  CALL_TRANSCRIPT_PROVIDER=gong \
  SUPPORT_PROVIDER=zendesk
  # ... add provider credentials
```

### 3. Deploy

```bash
modal deploy execution/main.py
```

### 4. Trigger the workflow

**Post-call mode** — trigger after a call ends:
```json
{
  "call_id": "gong-call-id-456",
  "customer_id": "0015g00000AbCdEf",
  "mode": "post_call",
  "webhook_source": "gong"
}
```

**Live mode** — trigger when a call starts (monitors in real time):
```json
{
  "call_id": "gong-call-id-456",
  "customer_id": "0015g00000AbCdEf",
  "mode": "live",
  "webhook_source": "gong"
}
```

---

## Test locally

```bash
# No setup needed — shows mock output immediately
python3 test.py

# With a real API key
ANTHROPIC_API_KEY=sk-ant-... python3 test.py
```

---

## Example output (Slack DM to CSM)

```
🔴 Trust Radar Alert: GENUINE_LOSS_OF_TRUST

Customer: Acme Corp       Call ID: gong-456
Mode: 📼 POST-CALL        Confidence: 84%
Urgency: 8/10

Reasoning:
Customer referenced a broken commitment from 3 months ago ("you promised the integration would be ready") and used definitive leaving language twice. No price or concession requests — this is not a negotiation.

Recommended Strategy:
Do not offer discounts. Acknowledge the broken promise directly. Ask what would need to change for trust to be rebuilt. Escalate to your manager for a joint call.

Key Evidence:
• [14:23] Sarah: "You said this would be fixed by January. It's March."  (broken_promise)
• [22:01] Sarah: "We're actively evaluating other options at this point."  (churn_threat)
• [31:45] Sarah: "I don't know if there's a path back here honestly."  (genuine_loss_of_trust)

Recommended Actions:
• Acknowledge the broken promise before anything else
• Do not discuss pricing or concessions in this call
• Request a follow-up with executive sponsor
```

---

## Required env vars

| Var | Required | Description |
|-----|----------|-------------|
| `LLM_PROVIDER` | Yes | `anthropic` or `openai` |
| `ANTHROPIC_API_KEY` | If anthropic | Claude API key |
| `OPENAI_API_KEY` | If openai | OpenAI API key |
| `SLACK_BOT_TOKEN` | Yes | Bot token for CSM alerts |
| `CRM_PROVIDER` | Optional | `salesforce` or `hubspot` |
| `CALL_TRANSCRIPT_PROVIDER` | Optional | `gong`, `fireflies`, or `zoom` |
| `SUPPORT_PROVIDER` | Optional | `zendesk` or `intercom` |
| `TRUST_RADAR_MIN_CONFIDENCE` | Optional | Default `0.7` — below this, forces MIXED/UNCLEAR |

> **HubSpot note:** HubSpot deprecated API keys in 2022. Use a Private App token (`HUBSPOT_PRIVATE_APP_TOKEN`) instead.
>
> **Zoom note:** Zoom deprecated JWT tokens in 2023. Use OAuth tokens (`ZOOM_OAUTH_TOKEN`) instead.
