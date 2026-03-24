# Invisible Handoff

Turns the context from a Closed Won sales call into a structured CSM handoff brief — so the customer never has to repeat themselves.

## What it does

This workflow takes the sales context you already have — transcript snippets, close notes, implementation context, or a written sales summary — and turns it into a structured CSM handoff brief covering what the customer cares about, what was promised, key stakeholders, watchouts, and a suggested first-call agenda.

It's designed to be useful immediately: paste in your sales notes, run the test, and see the kind of brief a CSM would receive.

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

See `.env.example`. Only `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`) and `SLACK_BOT_TOKEN` are required to run the full webhook path.

`NOTION_API_KEY` and `NOTION_PARENT_PAGE_ID` are optional if you want the brief written to Notion.

## How to use it in practice

You can use this workflow in two ways:

1. **Beginner / manual-input mode** — paste transcript text, close notes, or a written sales summary into the payload or test file.
2. **Connected mode** — wire your own CRM / transcript source upstream and pass the resulting text into this workflow.

That keeps the workflow tool-agnostic without pretending it ships with live provider adapters out of the box.
