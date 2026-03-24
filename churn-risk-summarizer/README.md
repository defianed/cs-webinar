# Churn Risk Summarizer

Turns recent customer activity into a plain-language churn risk narrative before a QBR or renewal call.

## What it does

This intelligent text-processing workflow analyses account activity, support friction, and engagement changes to build a narrative explaining what is driving current churn risk. It highlights stabilizers and the most important next-call focus areas.

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

That's it! You'll see output immediately — even without API keys (sample data is provided).

## Running locally

```bash
python3 test.py
```

The test works without any API credentials by showing realistic sample output. To see live LLM-generated results, add your API key to `.env`.

## Environment variables

See `.env.example` for all options. Only `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`) is required for live results.

## What you get

A structured risk assessment including:
- Plain-language risk story
- Primary risks (list)
- Stabilizers (positive factors)
- Next call focus areas
- Urgency level

## Deploying to production

This workflow is designed as an intelligent text processor. To connect live data sources:

1. Set up CRM, support, and analytics integrations in `.env`
2. Deploy with Modal: `modal deploy execution/main.py`
3. Trigger via webhook or schedule

## Providers supported

- LLM: Anthropic (Claude) or OpenAI (GPT-4)
- Optional integrations: Salesforce, HubSpot, Zendesk, Intercom, Mixpanel, Amplitude

## Note

This workflow processes text inputs to generate risk narratives. Live CRM/support integrations are optional — you can feed it data manually or via API.
