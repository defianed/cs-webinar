# ExtensibleAgents — CS Workflow Templates

Five plug-and-play agentic workflows for Customer Success teams. Each workflow runs on Modal cloud, swaps between your existing tools via env vars, and delivers output to your CSM via Slack.

---

## The 5 Workflows

| Workflow | What it does |
|----------|-------------|
| **Invisible Handoff** | Briefs your CSM from the sales transcript before the first customer call |
| **Trust Radar** | Analyses win-back calls to distinguish genuine trust loss from negotiation tactics |
| **Expansion Signal Detector** | Scans transcripts and notes for customers ready to expand |
| **Churn Risk Summarizer** | Generates a plain-English risk narrative before a QBR or renewal |
| **Earned Ask** | Detects the right moment and drafts a personalised review request |

Each workflow has its own folder with a README, `.env.example`, and `execution/main.py`.

---

## Prerequisites

Before setting up any workflow, you need:

### 1. Python 3.8+
```bash
python3 --version  # Should show 3.8 or higher
```

### 2. pip
```bash
python3 -m pip --version
# If missing on Ubuntu/Debian:
sudo apt-get install python3-pip
```

### 3. Modal account + CLI
Modal is the cloud platform these workflows deploy to. Free tier available.

```bash
# Create a free account at https://modal.com

# Install Modal
pip install modal

# Authenticate
modal token new
# This opens a browser to log in — follow the prompts
```

### 4. An LLM API key
Each workflow needs either:
- **Anthropic:** Get a key at https://console.anthropic.com — recommended, works out of the box
- **OpenAI:** Get a key at https://platform.openai.com

---

## Quick Start (pick one workflow to start)

We recommend starting with **Earned Ask** — it's the simplest and has no external provider dependencies beyond Slack and an LLM.

```bash
cd earned-ask
cp .env.example .env
# Edit .env and fill in your values
modal deploy execution/main.py
```

See the individual README in each folder for the full setup guide, example payloads, and expected outputs.

---

## Choosing your providers

Each workflow supports multiple tools in each category. You pick one per category and set it in your `.env`:

| Category | Options | Env var |
|----------|---------|---------|
| LLM | Anthropic, OpenAI | `LLM_PROVIDER=anthropic` or `openai` |
| CRM | Salesforce, HubSpot | `CRM_PROVIDER=salesforce` or `hubspot` |
| Call transcripts | Gong, Fireflies, Zoom | `CALL_TRANSCRIPT_PROVIDER=gong` etc |
| Support | Zendesk, Intercom | `SUPPORT_PROVIDER=zendesk` or `intercom` |
| Notifications | Slack | `SLACK_BOT_TOKEN=xoxb-...` |

You don't need all of them. Each workflow's README lists exactly which ones it uses.

---

## Troubleshooting

**"Token missing" error from Modal**
Run `modal token new` and follow the browser login flow.

**"Module not found" error locally**
The workflows install their own dependencies when deployed to Modal. For local testing, install manually:
```bash
pip install anthropic openai slack-sdk requests
```

**LLM returns garbled output / JSON parse error**
The workflow will fall back gracefully and return the raw text. Try a more capable model (`claude-3-5-sonnet-20241022` or `gpt-4o`).

**Slack notification not arriving**
Check that your `SLACK_BOT_TOKEN` starts with `xoxb-` and the bot has been invited to the relevant channel or can open DMs.

---

## Need help?

These workflows were built by [ExtensibleAgents](https://extensibleagents.com) — the agentic CS platform co-founded by Lincoln Murphy and Lewis Thompson.

If you want help deploying these for your team, or want to see what a full agentic CS stack looks like in production, visit **[extensibleagents.com](https://extensibleagents.com)**.
