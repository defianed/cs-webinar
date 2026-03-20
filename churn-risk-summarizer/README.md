# Churn Risk Summarizer

Pulls recent activity, support tickets, and engagement data and generates a plain-language risk narrative before a QBR or renewal call. Not a health score — an actual story.

## What it does
- Ingests recent activity, support summary, and engagement data
- Generates a plain-English narrative explaining the risk (not just a score)
- Highlights stabilising factors alongside threats
- Suggests what the CSM should focus on in their next call

## Providers supported
- CRM: Salesforce or HubSpot
- Support: Zendesk or Intercom
- Analytics: Mixpanel or Amplitude (or pass data directly)
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
modal secret create churn-risk-summarizer-secrets \
  LLM_PROVIDER=anthropic \
  ANTHROPIC_API_KEY=sk-ant-... \
  SLACK_BOT_TOKEN=xoxb-...
```

### 3. Deploy

```bash
modal deploy execution/main.py
```

### 4. Trigger the workflow

Trigger before a QBR, renewal call, or on a schedule:

```json
{
  "account_id": "0015g00000AbCdEf",
  "account_name": "Acme Corp",
  "csm_slack_user_id": "U012AB3CD",
  "recent_activity": "Login frequency dropped 40% over last 30 days. Core feature usage stable, but 2 previously active users haven't logged in since Feb.",
  "support_summary": "3 tickets in past 30 days: 2 resolved quickly, 1 open for 12 days (integration issue). Sentiment in tickets is frustrated.",
  "engagement_summary": "Skipped last 2 monthly check-ins. NPS dropped from 8 to 6 in last survey."
}
```

**Minimum required:** `account_id` + at least one of `recent_activity`, `support_summary`, `engagement_summary`.

---

## Test locally

```bash
ACCOUNT_NAME="Acme Corp" \
RECENT_ACTIVITY="Usage down 40%, 2 ghost users" \
SUPPORT_SUMMARY="Open ticket 12 days, frustrated tone" \
ENGAGEMENT_SUMMARY="Missed 2 check-ins, NPS dropped" \
modal run execution/main.py
```

---

## Example output

```json
{
  "status": "ok",
  "workflow": "churn-risk-summarizer",
  "account_name": "Acme Corp",
  "result": {
    "summary": "Acme is showing early churn indicators. Usage is declining and they've disengaged from check-ins, but the core workflow is still running. The open support ticket is the immediate risk.",
    "risk_story": "Acme started strong but has gone quiet over the last 6 weeks. Two users who were previously active have stopped logging in entirely — worth finding out why. The bigger signal is the missed check-ins: this account used to show up. When engaged customers stop showing up, it usually means something changed internally (new priorities, new stakeholder) or they've mentally started to move on. The open support ticket at 12 days is adding friction at exactly the wrong time. If that's not resolved this week, it becomes the reason they leave.",
    "primary_risks": [
      "12-day open support ticket creating active frustration",
      "2 ghost users — possible team restructure or disengagement",
      "Missed 2 check-ins suggests deprioritisation"
    ],
    "stabilizers": [
      "Core workflow still running — product is embedded",
      "Champion Sarah still responsive to direct messages",
      "Renewal is 90 days out — time to course-correct"
    ],
    "next_call_focus": [
      "Lead with the support ticket — acknowledge the delay, give timeline",
      "Ask about the 2 ghost users — is there a team change?",
      "Reframe the value of check-ins as time-saving, not reporting"
    ],
    "urgency": "high"
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
| `SUPPORT_PROVIDER` | Optional | `zendesk` or `intercom` |
| `ANALYTICS_PROVIDER` | Optional | `mixpanel` or `amplitude` |
