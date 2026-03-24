# The Earned Ask

## Quick Start
1. Clone this repo
2. `cd earned-ask`
3. `python3 test.py` — see it work instantly (no setup needed)
4. Copy `.env.example` to `.env`, add your API key, run again with real AI

---

An intelligent text processor for review timing. You describe a milestone and recent interactions as text — the AI decides if a review request is earned and drafts the email. Optionally delivers the draft to the CSM via Slack.

> **How it works:** You provide the milestone context. The AI writes the review request draft. No live CRM connection required — connect real integrations once the output quality is proven.

## What it does
- Reads milestone and interaction context you provide
- Decides whether a review ask is appropriate (and why)
- Drafts a personalised, non-generic review request email
- Optionally delivers the draft to the CSM via Slack for approval before sending

## Providers supported
- LLM: Anthropic (Claude) or OpenAI (GPT)
- Notifications: Slack (optional)
- CRM: Salesforce or HubSpot (optional — for live data pull once integrated)

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
modal secret create earned-ask-secrets \
  LLM_PROVIDER=anthropic \
  ANTHROPIC_API_KEY=sk-ant-... \
  SLACK_BOT_TOKEN=xoxb-...
```

### 3. Deploy

```bash
modal deploy execution/main.py
```

### 4. Trigger the workflow

Trigger from a milestone event — NPS survey response, support ticket resolved positively, renewal completed, QBR with positive outcome:

```json
{
  "account_id": "0015g00000AbCdEf",
  "account_name": "Acme Corp",
  "csm_slack_user_id": "U012AB3CD",
  "milestone_achieved": "Customer completed onboarding and went live ahead of schedule. First full month in production.",
  "interaction_summary": "QBR last week went well. Customer said the time savings have exceeded expectations. Champion Sarah specifically said she'd recommend to peers.",
  "sentiment_summary": "NPS score 9 submitted yesterday. Recent support tickets resolved same-day with positive follow-up."
}
```

**Minimum required:** `account_id` + `milestone_achieved` or `interaction_summary`.

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
  "workflow": "earned-ask",
  "account_name": "Acme Corp",
  "result": {
    "should_ask": true,
    "reason": "Customer just hit a major milestone (first month live, ahead of schedule), champion expressed intent to recommend, and NPS is 9. This is the ideal moment — positive sentiment is high and the value is fresh in their mind.",
    "subject_line": "Quick favour from one of our best customers?",
    "email_body": "Hi Sarah,\n\nReally glad to hear the first month went so well — going live ahead of schedule is no small thing, and it's a reflection of how seriously your team took the rollout.\n\nWe're building out our G2 profile and a review from you would mean a lot to us right now. It takes about 3 minutes and I can send you a direct link.\n\nOnly if you're happy to — no pressure at all.\n\n[Your name]",
    "csm_notes": "Sarah is warm and has already said she'd recommend. Send this week while the momentum is fresh. If she agrees, send the G2 link directly. Don't wait more than 5 days."
  }
}
```

The CSM receives the full draft in Slack, edits if needed, and sends it directly. The agent never contacts the customer.

---

## Required env vars

| Var | Required | Description |
|-----|----------|-------------|
| `LLM_PROVIDER` | Yes | `anthropic` or `openai` |
| `ANTHROPIC_API_KEY` | If anthropic | Claude API key |
| `OPENAI_API_KEY` | If openai | OpenAI API key |
| `SLACK_BOT_TOKEN` | Yes | Bot token for CSM notifications |
| `CRM_PROVIDER` | Optional | `salesforce` or `hubspot` |
