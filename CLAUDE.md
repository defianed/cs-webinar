# CLAUDE.md — CS Workflow Templates

You are helping a Customer Success leader set up, test, and run these agentic CS workflows locally using Claude Code. Your job is to be a guided setup assistant — take them from zero to a working local test, then optionally deploy to the cloud.

---

## What This Repo Is

5 plug-and-play agentic CS workflows built by [ExtensibleAgents.com](https://extensibleagents.com). Each one automates a specific high-friction moment in the CS lifecycle:

| Workflow | Problem it solves |
|----------|------------------|
| **Invisible Handoff** | CSM shows up to first customer call underprepared — sales-to-CS handoff was a Slack message and some notes |
| **Trust Radar** | CSM can't tell if a win-back customer is genuinely leaving or just negotiating |
| **Expansion Signal Detector** | Upsell opportunities sitting in transcripts go unnoticed until the moment passes |
| **Churn Risk Summarizer** | Health scores give a number, not a story. CSM walks into a QBR without knowing why |
| **Earned Ask** | Review requests go out at the wrong time, with the wrong message, and get ignored |

---

## Three Run Modes

### Mode 1 — Instant demo (no setup required)
```bash
python3 test.py
```
Shows you what the workflow does with **built-in sample data**. Zero config. No API key. Always works. Use this in demos or to understand what a workflow produces before wiring it up.

### Mode 2 — Local manual mode (sample_data/ files)
```bash
python3 local.py
```
Loads `sample_data/account.json` and `sample_data/notes.json` from the workflow folder and renders the mock output. No API key required. Useful for onboarding, demos, and customising the sample data to match your own accounts.

**To use manual mode:** edit `config.yaml` in the workflow folder and set:
```yaml
provider:
  llm: manual
```

### Mode 3 — Local live LLM mode (your own API key)
```bash
cp .env.example .env
# Edit .env — add ANTHROPIC_API_KEY or OPENAI_API_KEY
# Edit config.yaml — set provider.llm: anthropic (or openai)
python3 local.py
```
Runs the actual workflow logic using a real LLM. Costs ~$0.02–0.05 per run. Requires an API key.

### Mode 4 — Cloud deploy (production use)
```bash
modal deploy execution/main.py
```
Deploys as a cloud function with Modal. For always-on production use — triggered by CRM webhooks, Gong, Zapier, etc.

---

## config.yaml — Non-Secret Configuration

Each workflow has a `config.yaml` file. This is where you configure **which providers to use** — not secrets. Secrets always go in `.env`.

```yaml
# Non-secret configuration (secrets go in .env)
account_name: "TechFlow Inc"
csm_name: "Alex Chen"
provider:
  llm: manual       # anthropic | openai | manual
  crm: manual       # manual | salesforce | hubspot
  transcript: manual  # manual | gong | fireflies
```

**Provider options:**
- `llm: manual` — use built-in mock output (no API key needed)
- `llm: anthropic` — use Claude (requires `ANTHROPIC_API_KEY` in `.env`)
- `llm: openai` — use GPT-4o (requires `OPENAI_API_KEY` in `.env`)

If you set `llm: anthropic` but the API key is missing or invalid, `local.py` will automatically fall back to manual mode and tell you why — it will never crash.

---

## sample_data/ — Fixture Files

Each workflow has a `sample_data/` folder with two JSON files:

| File | Contents |
|------|----------|
| `account.json` | Account context: name, ARR, CSM, renewal date, champion, etc. |
| `notes.json` | Recent interaction notes, transcript snippets, support summary |

When running in **manual mode**, `local.py` loads these files and combines them as the input data. You can edit them to match a real account before a demo or call prep session.

---

## examples/ — Sample Output

Each workflow has an `examples/sample_output.md` file that shows exactly what the workflow produces — Slack message format and the full analysis JSON. Read these to understand what to expect before running anything.

---

## Repo Structure

```
cs-webinar/
├── README.md                          # 60-second quickstart
├── CLAUDE.md                          # This file
├── requirements.txt                   # pip install -r requirements.txt
├── churn-risk-summarizer/
│   ├── config.yaml                    # Provider config (no secrets)
│   ├── sample_data/
│   │   ├── account.json               # Sample account context
│   │   └── notes.json                 # Sample notes / activity
│   ├── examples/
│   │   └── sample_output.md           # What this workflow produces
│   ├── local.py                       # Run locally (manual or live LLM)
│   ├── test.py                        # Instant demo with built-in mock data
│   ├── execution/main.py              # Modal cloud function
│   ├── .env.example                   # Credential template
│   └── README.md                      # Workflow-specific docs
├── earned-ask/                        # Same structure
├── expansion-signal-detector/         # Same structure
├── invisible-handoff/                 # Same structure
└── trust-radar/                       # Same structure
```

---

## How to Guide the Client

### Step 1 — Check prerequisites

```bash
python3 --version   # Need 3.8+
pip --version
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — See what a workflow does (no setup)

```bash
cd earned-ask
python3 test.py
```

Recommend **Earned Ask** first — it's the simplest and the output is immediately legible.

### Step 4 — Customise the sample data

Edit `sample_data/account.json` and `sample_data/notes.json` to match a real account. Then:
```bash
python3 local.py   # Uses manual mode — no API key needed
```

### Step 5 — Run with a real API key

```bash
cp .env.example .env
# Add ANTHROPIC_API_KEY to .env
# Edit config.yaml: set provider.llm: anthropic
python3 local.py
```

Cost per run: ~$0.02–0.05 with Claude Sonnet. ~$0.03–0.06 with GPT-4o.

### Step 6 — Cloud deployment (when ready)

```bash
pip install modal
modal token new    # Opens browser, log in to modal.com (free account)

modal secret create earned-ask-secrets \
  LLM_PROVIDER=anthropic \
  ANTHROPIC_API_KEY=sk-ant-...

modal deploy execution/main.py
```

---

## Common Errors and Fixes

**`ModuleNotFoundError: No module named 'anthropic'`**
```bash
pip install -r requirements.txt
```

**`AuthenticationError` from Anthropic or OpenAI**
The API key in `.env` is wrong or revoked. Set `provider.llm: manual` in `config.yaml` to run without it.

**`ModuleNotFoundError: No module named 'yaml'`**
```bash
pip install pyyaml
```

**`KeyError` or `IndexError` when parsing output**
The LLM returned unexpected output. Switch to a stronger model in `.env`:
```
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**Slack DM not arriving**
- `SLACK_BOT_TOKEN` must start with `xoxb-`
- `CSM_SLACK_USER_ID` must be a Slack member ID (`U012AB3CD`), not `@username`

---

## Provider Cheat Sheet

| Category | Options | Config key |
|----------|---------|------------|
| LLM | anthropic, openai, manual | `provider.llm` in config.yaml |
| CRM | salesforce, hubspot, manual | `provider.crm` in config.yaml |
| Transcripts | gong, fireflies, manual | `provider.transcript` in config.yaml |

**You don't need all of them.** Every workflow works with `manual` for all providers — paste sample text into `sample_data/notes.json` and you're running in seconds. Wire up real integrations once the workflow is proven locally.

---

## Need Help?

Built by [ExtensibleAgents](https://extensibleagents.com) — the agentic CS platform co-founded by Lincoln Murphy and Lewis Thompson.

Visit **[extensibleagents.com](https://extensibleagents.com)** if you want help customising these for your stack or want to see a full agentic CS deployment.
