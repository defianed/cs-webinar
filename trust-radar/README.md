# Trust Radar

Analyses win-back and escalation call transcripts to determine whether a customer is showing genuine loss of trust or applying commercial negotiation pressure — then tells the CSM what to do.

## What it does

The Trust Radar classifies calls into one of four verdicts:
- `GENUINE_LOSS_OF_TRUST` — real relationship damage; repair trust before anything commercial
- `NEGOTIATING` — using frustration as leverage; hold the line or make a targeted concession
- `MIXED` — both signals present; nuanced response needed
- `UNCLEAR` — insufficient signal; listen more before acting

It provides evidence snippets from the transcript, a confidence score, and a concrete recommended response strategy.

## Quickstart (3 steps)

1. **Clone the repo** (if you haven't already)
2. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```
   Then add your `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`) to the `.env` file.
3. **Run the test:**
   ```bash
   python3 test.py
   ```

That's it! You'll see output immediately — even without API keys. To run with live AI:

```bash
python3 test.py --live
```

## What you get

- Classification verdict with confidence score
- Evidence snippets from the transcript with signal type
- Response strategy (specific, actionable)
- Urgency score (1-10)
- Recommended next actions

## Environment variables

See `.env.example`. Only `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`) and `SLACK_BOT_TOKEN` are required to run.

Live CRM integration (Salesforce, HubSpot), transcript providers (Gong, Fireflies, Zoom), and support systems (Zendesk, Intercom) are optional.

**Note on Salesforce:** Connecting live Salesforce data may require custom field mapping depending on your org's schema. Review `execution/main.py` adapter classes before enabling.

## Updated environment variable names

This workflow uses:
- `HUBSPOT_PRIVATE_APP_TOKEN` (not `HUBSPOT_API_KEY`)
- `ZOOM_OAUTH_TOKEN` (not `ZOOM_JWT_TOKEN`)

Ensure your `.env` uses these names.
