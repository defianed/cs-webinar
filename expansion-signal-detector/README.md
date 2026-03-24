# Expansion Signal Detector

Scans call transcripts and post-call notes for signals that a customer is ready to expand.

## What it does

This intelligent text-processing workflow analyses account context, transcript snippets, and usage notes to identify expansion buying signals, blockers, and optimal timing for an expansion conversation.

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

- `expansion_ready` — true/false with confidence score
- `buying_signals` — specific signals from the transcript/notes
- `blockers` — what might delay or prevent expansion
- `recommended_timing` — when to have the expansion conversation
- `next_steps` — concrete actions for the CSM

## Note

This workflow processes text inputs you supply (transcripts, notes, usage summaries). It does not connect directly to CRM or call recording systems.

## Environment variables

See `.env.example`. Only `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`) is required for live results.
