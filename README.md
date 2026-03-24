# CS Workflow Templates

5 agentic CS workflows you can run today. Built by [ExtensibleAgents.com](https://extensibleagents.com).

---

## See It Work in 60 Seconds

```bash
git clone https://github.com/defianed/cs-webinar
cd cs-webinar/churn-risk-summarizer
python3 test.py
```

That's it. No API key, no setup. You'll see realistic output immediately.

Add your API key and it calls the real LLM with sample data:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python3 test.py
```

---

## The 5 Workflows

| Workflow | Problem it solves | What you get out |
|----------|------------------|-----------------|
| **invisible-handoff** | CSM shows up to first customer call underprepared — all they got was a Slack message | Structured handoff brief: goals, stakeholders, commitments, watchouts, suggested first call agenda |
| **trust-radar** | Can't tell if a win-back customer is genuinely leaving or just negotiating | Classification (NEGOTIATING / GENUINE_LOSS_OF_TRUST / MIXED), evidence snippets, specific response strategy |
| **expansion-signal-detector** | Upsell opportunities sit in transcripts unnoticed until the moment passes | Confidence score, buying signals, blockers, recommended timing, next steps |
| **churn-risk-summarizer** | Health scores give a number, not a story — CSM walks into QBR without knowing *why* | Plain-language risk narrative, primary risks, stabilizers, next call focus, urgency |
| **earned-ask** | Review requests go out at the wrong time, wrong message, and get ignored | Should-ask decision, reason, subject line, drafted email, CSM notes |

Each workflow has an `examples/sample_output.md` showing exactly what the output looks like.

---

## Three Ways to Run

### 1. `python3 test.py` — No setup required

```bash
cd earned-ask
python3 test.py
```

Prints realistic mock output. No API key needed.

Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` and it calls the real LLM with the `sample_data/` fixtures automatically.

### 2. `python3 local.py` — Full local run

```bash
cd earned-ask
cp .env.example .env
# Edit .env — add API key, optionally Slack token
python3 local.py
```

Reads `config.yaml` for settings. When `provider=manual` (the default), loads data from `sample_data/`. With an API key, runs the full workflow end-to-end.

### 3. `modal deploy` — Production cloud

```bash
pip install modal
modal token new
modal secret create earned-ask-secrets ANTHROPIC_API_KEY=sk-ant-... SLACK_BOT_TOKEN=xoxb-...
cd earned-ask
modal deploy execution/main.py
```

Modal gives you a webhook URL. Point your CRM, Gong, or Zapier at it and the workflow runs on every trigger.

---

## Cost Estimate

Each workflow makes one LLM call per run:

| Model | Approx. cost per run |
|-------|---------------------|
| claude-opus-4-6 (default) | ~$0.05–$0.15 |
| gpt-4o | ~$0.05–$0.15 |

A team running 50 accounts through churn-risk-summarizer weekly ≈ $5–7/week.

---

## How Providers Work

Each workflow's `config.yaml` has provider settings:

```yaml
crm_provider: manual        # manual | salesforce | hubspot
transcript_provider: manual # manual | gong | fireflies | fathom | zoom
support_provider: manual    # manual | zendesk | intercom
```

**`manual`** = load from `sample_data/` files. No external APIs needed.

Change a provider value and add the credentials to `.env` to connect a real system. The `.env.example` file in each workflow shows what variables you need.

---

## Sample Data

Every workflow ships with realistic fixtures in `sample_data/`:

- `account.json` — Acme Corp, Sarah Johnson CSM, ARR, health score, contract date
- `transcript.json` — ~400-word realistic call transcript relevant to the workflow
- `tickets.json` — 3 fake support tickets (where relevant)

Edit these files to test with your own scenarios, or paste your own transcript into `transcript.json`.

---

## Prerequisites

```bash
python3 --version  # 3.8+
pip install anthropic openai slack-sdk requests pyyaml python-dotenv
```

That's everything you need for `test.py` and `local.py`. `modal` is only needed for cloud deployment.

---

## What's in Each Workflow

```
workflow-name/
├── config.yaml           # Account name, CSM, provider settings (no secrets)
├── .env.example          # All credentials — copy to .env and fill in
├── test.py               # Zero-setup test: mock output or live LLM with sample data
├── local.py              # Full local run — loads config.yaml and sample_data/
├── execution/main.py     # Modal deployment — adds Slack, CRM, transcript integrations
├── sample_data/
│   ├── account.json      # Fake Acme Corp account
│   ├── transcript.json   # Realistic call transcript
│   └── tickets.json      # 3 fake support tickets (where relevant)
├── examples/
│   └── sample_output.md  # What real output looks like
└── README.md             # Workflow-specific quickstart
```

---

## Need Help?

Built by [ExtensibleAgents](https://extensibleagents.com) — the agentic CS platform co-founded by Lincoln Murphy and Lewis Thompson.

Visit **[extensibleagents.com](https://extensibleagents.com)** for help customising these for your stack or to see a full agentic CS deployment.
