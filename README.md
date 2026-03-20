# ExtensibleAgents — CS Workflow Templates

Five plug-and-play agentic workflows for Customer Success teams. Test them locally with Claude Code, deploy to the cloud when you're ready.

---

## The 5 Workflows

| Workflow | What it does |
|----------|-------------|
| **Invisible Handoff** | Briefs your CSM from the sales transcript before the first customer call |
| **Trust Radar** | Analyses win-back calls to distinguish genuine trust loss from negotiation tactics |
| **Expansion Signal Detector** | Scans transcripts and notes for customers ready to expand |
| **Churn Risk Summarizer** | Generates a plain-English risk narrative before a QBR or renewal |
| **Earned Ask** | Detects the right moment and drafts a personalised review request |

Each workflow folder contains: `execution/main.py`, `.env.example`, and a `README.md` with setup steps, example inputs, and example outputs.

---

## How it works

**Local first. Cloud later.**

1. Install dependencies, fill in your credentials
2. Run locally — test with real or sample data, see the output
3. When you're happy — deploy to Modal and point your tools at the webhook

You don't need a Modal account to test. Everything runs locally with Python.

---

## Prerequisites

### Python 3.8+
```bash
python3 --version
```

### pip
```bash
pip --version

# If missing on Mac:
brew install python

# If missing on Ubuntu/Debian:
sudo apt-get install python3-pip
```

### Python dependencies
```bash
pip install anthropic openai slack-sdk requests
```

### An LLM API key
Pick one:
- **Anthropic Claude** — [console.anthropic.com](https://console.anthropic.com) (recommended)
- **OpenAI GPT** — [platform.openai.com](https://platform.openai.com)

---

## Quick Start

We recommend starting with **Earned Ask** — it's the simplest, no CRM or transcript provider needed.

```bash
cd earned-ask
cp .env.example .env
# Open .env and fill in your LLM API key + any other values
```

Run it:
```bash
export $(cat .env | xargs)
python3 execution/main.py
```

You'll see the output printed to your terminal. If you've added a Slack bot token, the result lands in the CSM's Slack DM.

See the `README.md` inside each workflow folder for the full setup guide, required env vars, example inputs, and example outputs.

---

## Cloud Deployment (optional)

When you want a workflow running automatically — triggered by your CRM, Gong, or Zapier — deploy to Modal:

```bash
pip install modal
modal token new   # Free account at modal.com

modal secret create earned-ask-secrets \
  LLM_PROVIDER=anthropic \
  ANTHROPIC_API_KEY=sk-ant-... \
  SLACK_BOT_TOKEN=xoxb-...

modal deploy execution/main.py
```

Modal gives you a webhook URL. Point your tools at it and the workflow runs automatically.

---

## Testing without real integrations

Every workflow accepts raw text directly — no Gong, Salesforce, or Zendesk required to get started. Paste sample transcript text or notes in the env vars and run it. Wire up real integrations once the output quality is proven.

---

## Need help?

These workflows were built by [ExtensibleAgents](https://extensibleagents.com) — the agentic CS platform co-founded by Lincoln Murphy and Lewis Thompson.

If you want help deploying these for your team, or want to see what a full agentic CS stack looks like in production, visit **[extensibleagents.com](https://extensibleagents.com)**.
