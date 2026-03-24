# CS Agentic Workflow Templates

5 agentic CS workflows you can run today, built for the [ExtensibleAgents](https://extensibleagents.com) webinar.

No developer. No infrastructure. Just Python.

---

## 60-Second Quickstart

```bash
# 1. Clone
git clone https://github.com/defianed/cs-webinar
cd cs-webinar

# 2. Install dependencies
pip install -r requirements.txt

# 3. See a workflow in action — no API key needed
cd trust-radar
python3 test.py

# 4. Run with sample data in manual mode — no API key needed
python3 local.py

# 5. (Optional) Run with your real API key
cp .env.example .env
# Edit .env: add ANTHROPIC_API_KEY=sk-ant-...
# Edit config.yaml: set provider.llm: anthropic
python3 local.py
```

That's it. You'll see real output in under 60 seconds.

---

## The 5 Workflows

| Workflow | What it produces | Sample output |
|---|---|---|
| **Churn Risk Summarizer** | Plain-language risk narrative for a QBR or renewal call — not a health score, a story | [sample_output.md](churn-risk-summarizer/examples/sample_output.md) |
| **Earned Ask** | Detects genuine milestone moments, then drafts the G2/review request email ready to send | [sample_output.md](earned-ask/examples/sample_output.md) |
| **Expansion Signal Detector** | Scans call notes for buying signals, rates expansion readiness, and suggests next steps | [sample_output.md](expansion-signal-detector/examples/sample_output.md) |
| **Invisible Handoff** | Turns a Closed Won deal into a structured CSM brief: stakeholders, commitments, watchouts | [sample_output.md](invisible-handoff/examples/sample_output.md) |
| **Trust Radar** | Classifies escalation call transcripts: genuine loss of trust, negotiating, or mixed? | [sample_output.md](trust-radar/examples/sample_output.md) |

---

## Three Ways to Run

### 1. Instant demo — no setup required
```bash
python3 test.py
```
Built-in sample data. No API key. Always works. Use this to show a colleague what a workflow does in 10 seconds.

### 2. Manual mode — customise sample data, no API key needed
```bash
python3 local.py
```
Loads `sample_data/account.json` and `sample_data/notes.json`. Edit those files to match a real account and run again. No API key required. Default mode when `config.yaml` has `provider.llm: manual`.

### 3. Live LLM mode — real AI output, ~$0.02–0.05 per run
```bash
cp .env.example .env
# Add ANTHROPIC_API_KEY or OPENAI_API_KEY to .env
# Edit config.yaml: set provider.llm: anthropic (or openai)
python3 local.py
```
Runs with a real LLM. Cost estimate: ~$0.02–0.05 per workflow run with Claude Sonnet, ~$0.03–0.06 with GPT-4o.

---

## Requirements

- Python 3.9+
- No API key needed for demo and manual modes
- Anthropic or OpenAI API key for live LLM mode (~$0.02–0.05/run)
- (Optional) Modal account for cloud deployment — free tier available

---

## Customise the Sample Data

Each workflow has a `sample_data/` folder:
- `account.json` — account context (name, ARR, CSM, renewal date, etc.)
- `notes.json` — recent notes, transcript snippets, support summary

Edit these files to match a real account before your next QBR prep or handoff call, then run `python3 local.py`.

---

## How Providers Work

Each workflow has a `config.yaml` with a `provider` section:

```yaml
provider:
  llm: manual       # anthropic | openai | manual
  crm: manual       # manual | salesforce | hubspot
  transcript: manual  # manual | gong | fireflies
```

- `manual` — uses built-in sample data (no external connection needed)
- `anthropic` / `openai` — calls the real API (key required in `.env`)

If `local.py` can't find a valid API key for the configured provider, it falls back to manual mode automatically and tells you why — it never crashes.

---

## Cloud Deployment (Optional)

When you're ready to run these automatically in production:

```bash
pip install modal
modal token new   # free account at modal.com

cd earned-ask
modal secret create earned-ask-secrets \
  ANTHROPIC_API_KEY=sk-ant-...

modal deploy execution/main.py
```

Modal gives you a webhook URL. Point your CRM, Gong, or Zapier at it and the workflow runs automatically when triggered.

---

## Cost Estimates

| Model | Tokens per run | Approx cost |
|-------|---------------|-------------|
| Claude Sonnet (Anthropic) | ~1,500–2,000 | ~$0.02–0.03 |
| Claude Opus (Anthropic) | ~1,500–2,000 | ~$0.04–0.06 |
| GPT-4o (OpenAI) | ~1,500–2,000 | ~$0.02–0.05 |

All well under $0.10 per run. For a team running 20 workflows/day, budget ~$10–20/month.

---

Built with [Claude](https://anthropic.com) by [ExtensibleAgents](https://extensibleagents.com)
