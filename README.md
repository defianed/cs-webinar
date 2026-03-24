# CS Agentic Workflow Templates

5 agentic CS workflows you can run today, built for the [ExtensibleAgents](https://extensibleagents.com) webinar.

No developer. No infrastructure. Just Python.

---

## The 5 Workflows

| Workflow | What it does |
|---|---|
| **Churn Risk Summarizer** | Turns recent account activity into a plain-language risk narrative before a QBR or renewal call |
| **Earned Ask** | Detects when a positive milestone has been hit, then drafts the review request email |
| **Expansion Signal Detector** | Scans call notes and transcripts for signals that a customer is ready to expand |
| **Invisible Handoff** | Turns a Closed Won deal into a structured CSM handoff brief |
| **Trust Radar** | Analyses escalation call transcripts to tell you: genuine loss of trust, or negotiating? |

---

## Three ways to run

### 1. Instant demo (no setup required)
```bash
python3 test.py
```
Shows you what the workflow does with sample data. No API key needed. Always works.

### 2. Local real run (your own API key)
```bash
python3 local.py
```
Runs the actual workflow logic locally. No Modal account needed. Requires an API key.

### 3. Cloud deploy (production use)
```bash
modal deploy execution/main.py
```
Deploys as a cloud function with Modal. For always-on production use.

---

## Getting started

**Step 1: Clone the repo**
```bash
git clone https://github.com/defianed/cs-webinar
cd cs-webinar
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: See the workflow in action**
```bash
cd trust-radar   # (or any other workflow)
python3 test.py
```

**Step 4: Run with your own API key**
```bash
cp .env.example .env
# Edit .env — add ANTHROPIC_API_KEY (or OPENAI_API_KEY)
python3 local.py
```

**Step 5: Deploy to the cloud (optional)**
```bash
pip install modal
modal setup
modal deploy execution/main.py
```

---

## Requirements

- Python 3.9+
- An [Anthropic](https://anthropic.com) or [OpenAI](https://openai.com) API key
- (Optional) A Slack bot token for notifications
- (Optional) Modal account for cloud deployment

---

Built with [Claude](https://anthropic.com) by [ExtensibleAgents](https://extensibleagents.com)
