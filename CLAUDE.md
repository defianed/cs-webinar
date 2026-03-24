# CLAUDE.md — CS Workflow Templates

## What This Repo Is

5 plug-and-play agentic CS workflows. Each automates a high-friction moment in the CS lifecycle.

| Workflow | What it does |
|----------|-------------|
| **invisible-handoff** | Turns a Closed Won deal into a structured CSM handoff brief — so your first call isn't the first time you've heard of the account |
| **trust-radar** | Reads a win-back or escalation call transcript and tells you: is this customer genuinely leaving, or are they negotiating? |
| **expansion-signal-detector** | Scans call transcripts for buying signals that a customer is ready to expand — before the moment passes |
| **churn-risk-summarizer** | Turns recent account activity into a plain-language churn risk story — tells you *why* the health score is declining, not just the number |
| **earned-ask** | Detects when a customer has earned a review request and drafts the email — gets the timing and message right |

---

## Three Ways to Run Each Workflow

### 1. `python3 test.py` — Zero setup, see output in 30 seconds

```bash
cd churn-risk-summarizer
python3 test.py
```

- No API key needed — prints realistic mock output
- If `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` is set in your environment: calls the real LLM with `sample_data/` fixtures
- Always exits 0

### 2. `python3 local.py` — Local run with your config

```bash
cd churn-risk-summarizer
cp .env.example .env
# edit .env — add your API key
python3 local.py
```

- Reads `config.yaml` for account name, CSM name, provider settings
- Loads data from `sample_data/` when `provider=manual` (the default)
- Calls real LLM if API key is set in `.env`

### 3. `modal deploy execution/main.py` — Production cloud deployment

```bash
pip install modal
modal token new
modal secret create churn-risk-summarizer-secrets ANTHROPIC_API_KEY=sk-ant-...
modal deploy execution/main.py
```

You get a webhook URL. Point your CRM, Gong, or Zapier at it and the workflow runs automatically.

---

## How `config.yaml` Works

Each workflow has a `config.yaml` in its root:

```yaml
# Who you are
account_name: Acme Corp
csm_name: Sarah Johnson
slack_channel: "#cs-alerts"

# What tools you use (provider=manual means use sample_data/ files)
crm_provider: manual        # manual | salesforce | hubspot
transcript_provider: manual # manual | gong | fireflies | fathom | zoom
support_provider: manual    # manual | zendesk | intercom

# Workflow-specific settings (varies per workflow)
min_confidence: 0.7
```

**`provider=manual`** means: load data from the `sample_data/` folder in that workflow. No external API needed.

**To connect a real provider**, change the value (e.g., `crm_provider: hubspot`) and add the credentials to `.env`. The `.env.example` file shows which variables you need.

**The LLM is auto-detected from your API key** — no LLM provider setting needed. If `ANTHROPIC_API_KEY` is set, it uses claude-opus-4-6. If `OPENAI_API_KEY` is set, it uses gpt-4o.

---

## How `sample_data/` Works

Every workflow ships with realistic fixture files you can run against immediately:

| File | What's in it |
|------|-------------|
| `account.json` | Fake Acme Corp account — ARR, health score, tier, CSM name, contract end date |
| `transcript.json` | ~400-word realistic CS conversation relevant to the workflow |
| `tickets.json` | 3 fake support tickets with title, status, priority, body |

These are the defaults when `provider=manual`. They work with both `test.py` (mock mode) and `local.py` (live LLM mode).

To use your own data without connecting a real provider: edit the files in `sample_data/` directly, or paste your transcript text into `transcript.json`.

See `examples/sample_output.md` in each workflow for what good output looks like.

---

## How to Add a New Provider (e.g., Fathom)

1. In `config.yaml`, set `transcript_provider: fathom`
2. In `execution/main.py`, find the `get_transcript_text()` function — it has a conditional block for each provider
3. Add an `elif provider == "fathom":` block that calls the Fathom API and returns the transcript as a string
4. Add `FATHOM_API_KEY` to `.env.example` and your real `.env`

All workflows follow the same pattern. The `manual` path (loading from `sample_data/transcript.json`) is the reference implementation — it shows exactly what format the transcript needs to be in.

---

## Common Errors

**`ModuleNotFoundError: No module named 'anthropic'`**
```bash
pip install anthropic openai slack-sdk requests pyyaml python-dotenv
```

**`AuthenticationError`**
Your API key in `.env` is wrong — no spaces, no quotes around the value. Anthropic keys start with `sk-ant-`. OpenAI keys start with `sk-`.

**`KeyError` or `IndexError` when parsing**
The LLM returned something unexpected. These workflows use `claude-opus-4-6` by default — don't downgrade it.

**Slack DM not arriving**
- `SLACK_BOT_TOKEN` must start with `xoxb-`
- `CSM_SLACK_USER_ID` must be a member ID like `U012AB3CD`, not `@username`
- The bot must be installed to the workspace

**Salesforce auth error**
`SALESFORCE_PASSWORD` must include the security token appended directly to the password (no space).

---

## Provider Cheat Sheet

| Category | Options | Default |
|----------|---------|---------|
| LLM | Anthropic, OpenAI | auto-detected from API key |
| CRM | Salesforce, HubSpot, manual | manual |
| Transcripts | Gong, Fireflies, Fathom, Zoom, manual | manual |
| Support tickets | Zendesk, Intercom, manual | manual |

Start with `manual` for everything. Connect real providers once you've validated the output quality.

---

## Need Help?

Built by [ExtensibleAgents](https://extensibleagents.com) — the agentic CS platform co-founded by Lincoln Murphy and Lewis Thompson.
