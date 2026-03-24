# Invisible Handoff

Turns the context from a Closed Won sales call into a structured CSM handoff brief — so the customer never has to repeat themselves.

## What it does

When a deal closes, the CSM shouldn't be going into their first call blind. This workflow takes sales call notes and context, then generates a structured handoff brief covering: what the customer cares about, what was promised, key stakeholders, watchouts, and a suggested first-call agenda.

When connected to live CRM and call transcript providers (Gong, Fireflies), it pulls the data automatically. Without live connections, it works from the text summaries you provide.

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

- Account overview
- Customer goals and pain points
- Commitments and objections handled in sales
- Key stakeholder map
- Watchouts for the CSM
- Suggested first-call agenda

## Environment variables

See `.env.example`. Only `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`) is required for the text-processing path. CRM and transcript provider credentials are optional — only needed if connecting live data sources.

## Note on live integrations

CRM and transcript integrations (Salesforce, HubSpot, Gong, Fireflies) are provided as placeholder adapters. You can connect them by setting the relevant env vars and extending the adapter classes in `execution/main.py`.
