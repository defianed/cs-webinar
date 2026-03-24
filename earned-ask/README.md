# Earned Ask

Detects whether a customer has genuinely earned a review request, then drafts the email for a CSM to send.

## What it does

This intelligent text-processing workflow analyses recent interaction context, milestones achieved, and sentiment signals to decide if the timing is right to ask for a review. If yes, it drafts the review request email.

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

That's it! You'll see output immediately — even without API keys (sample output is provided). To run with live AI:

```bash
python3 test.py --live
```

## What you get

- `should_ask` — yes or no with reasoning
- `subject_line` — ready-to-use email subject
- `email_body` — draft email for the CSM to review and send
- `csm_notes` — context for the CSM

## Note

This workflow processes text inputs to generate a recommendation and email draft. The CSM always reviews the output before sending. No automated emails are sent.

## Environment variables

See `.env.example`. Only `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`) is required for live results.
