# Invisible Handoff

## Quick Start
1. Clone this repo
2. `cd invisible-handoff`
3. `python3 test.py` — see it work instantly (no setup needed)
4. Copy `.env.example` to `.env`, add your API key, run again with real AI

---

Turns a Closed Won event into a CSM-ready customer brief — before the first call.

## What it does
- Pulls CRM context (opportunity, account)
- Reads the final sales call transcript
- Extracts what Sales promised and what the customer cares about
- Writes a brief to Notion (optional)
- Sends the CSM a Slack summary before their first call

## Providers supported
- CRM: Salesforce or HubSpot
- Transcript: Gong or Fireflies (or pass raw text directly)
- Output: Notion (optional) + Slack
- LLM: Anthropic (Claude) or OpenAI (GPT)

---


## Prerequisites

- Python 3.8+, pip, and Modal CLI installed — see the [main README](../README.md) for setup
- A Modal account (free tier works): [modal.com](https://modal.com)
- An LLM API key: Anthropic ([console.anthropic.com](https://console.anthropic.com)) or OpenAI ([platform.openai.com](https://platform.openai.com))
- A Slack bot token with permission to send DMs: [api.slack.com/apps](https://api.slack.com/apps)


## Setup

### 1. Configure your environment

Copy `.env.example` and fill in your credentials:

```bash
cp .env.example .env
# Edit .env with your values
```

Pick one provider per category. You don't need all of them — only the ones you use.

### 2. Create a Modal secret

```bash
modal secret create invisible-handoff-secrets \
  LLM_PROVIDER=anthropic \
  ANTHROPIC_API_KEY=sk-ant-... \
  SLACK_BOT_TOKEN=xoxb-... \
  CRM_PROVIDER=salesforce \
  SALESFORCE_INSTANCE_URL=https://yourorg.salesforce.com \
  SALESFORCE_ACCESS_TOKEN=...
```

### 3. Deploy

```bash
modal deploy execution/main.py
```

### 4. Set up your trigger

Send a POST request to the Modal webhook URL when a deal closes:

**Example payload:**
```json
{
  "account_id": "0015g00000AbCdEf",
  "opportunity_id": "0065g00000XyZaBc",
  "call_id": "gong-call-id-123",
  "account_name": "Acme Corp",
  "csm_slack_user_id": "U012AB3CD",
  "transcript_text": "Optional: paste raw transcript here if not using Gong/Fireflies"
}
```

**Minimum required fields:** `account_id` + either `call_id` (for provider pull) or `transcript_text` (for direct input).

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
  "workflow": "invisible-handoff",
  "account_name": "Acme Corp",
  "processed_at": "2026-03-20T12:00:00",
  "brief": {
    "customer_goals": ["Reduce onboarding time by 50%", "Replace manual CSV exports"],
    "pain_points": ["Current tool requires 3 manual steps per account"],
    "commitments_made": ["Sales promised API access in month 1", "Custom onboarding doc within 2 weeks"],
    "objections_raised": ["Price was a concern — resolved with annual discount"],
    "stakeholder_map": ["Sarah (Champion)", "Mark (Economic buyer)", "IT team (blockers)"],
    "communication_style": "Detail-oriented, prefers written summaries over verbal updates",
    "onboarding_risks": ["IT approval required for API integration — not yet started"],
    "first_call_agenda": ["Confirm onboarding timeline", "Intro to CSM process", "Set success metrics"],
    "top_3_watchouts": [
      "IT approval not secured — flag this in first call",
      "Sales promised custom doc — coordinate with solutions team",
      "Champion Sarah is leaving in 6 weeks — build relationship with backup"
    ],
    "brief_summary": "Acme is focused on reducing manual ops work. Sales committed to API access and a custom onboarding doc. IT approval is the main risk. Champion Sarah is engaged but leaving soon — prioritise getting a second contact."
  }
}
```

The CSM receives the `brief_summary` and `top_3_watchouts` in Slack before their first call.

---

## Required env vars

| Var | Required | Description |
|-----|----------|-------------|
| `LLM_PROVIDER` | Yes | `anthropic` or `openai` |
| `ANTHROPIC_API_KEY` | If anthropic | Claude API key |
| `OPENAI_API_KEY` | If openai | OpenAI API key |
| `SLACK_BOT_TOKEN` | Yes | Bot token for CSM notifications |
| `CRM_PROVIDER` | Optional | `salesforce` or `hubspot` |
| `CALL_TRANSCRIPT_PROVIDER` | Optional | `gong` or `fireflies` |
| `NOTION_API_KEY` | Optional | For Notion brief output |
