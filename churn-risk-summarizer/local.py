#!/usr/bin/env python3
"""
Churn Risk Summarizer — local runner (no Modal required)
Run: python3 local.py

Run modes:
  Manual (default): loads sample_data/ and shows mock output — no API key needed
  LLM mode:         set provider.llm: anthropic (or openai) in config.yaml + add key to .env

Config: edit config.yaml to change provider settings (no secrets there).
Secrets: copy .env.example → .env and add your API key.
"""
import os, json, sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import yaml
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False

WORKFLOW_DIR = Path(__file__).parent

# ── MOCK OUTPUT (mirrors test.py) ─────────────────────────────────────────────
MOCK_OUTPUT = {
    "summary": "TechFlow Inc is showing early churn indicators with declining usage and disengagement from check-ins.",
    "risk_story": "TechFlow started strong but has gone quiet over the past 30 days. Two users who were previously active have stopped logging in entirely. The open support ticket at 12 days is adding friction at exactly the wrong time — if it's not resolved this week, it becomes the reason they leave.",
    "primary_risks": [
        "12-day open support ticket creating active frustration",
        "Login frequency down 40% — 2 ghost users since February",
        "Missed last 2 monthly check-ins"
    ],
    "stabilizers": [
        "Core product still in use by majority of team",
        "Renewal not imminent — time to course-correct"
    ],
    "next_call_focus": [
        "Lead with the open support ticket — acknowledge the delay, give a timeline",
        "Ask about the 2 inactive users — is there a team change?",
        "Reframe check-ins as time-saving, not reporting"
    ],
    "urgency": "high"
}


def load_config() -> dict:
    config_path = WORKFLOW_DIR / "config.yaml"
    if _YAML_AVAILABLE and config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f) or {}
    return {}


def get_llm_provider(config: dict) -> str:
    """Return 'anthropic', 'openai', or 'manual'."""
    provider_config = config.get("provider", {})
    return provider_config.get("llm", "manual")


def has_valid_key(provider: str) -> bool:
    if provider == "anthropic":
        key = (os.getenv("ANTHROPIC_API_KEY") or "").strip()
        return bool(key)
    if provider == "openai":
        key = (os.getenv("OPENAI_API_KEY") or "").strip()
        return bool(key) and key.startswith("sk-")
    return False


def call_llm(prompt: str, provider: str) -> str:
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1400,
        )
        return resp.choices[0].message.content
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-opus-4-6"),
        max_tokens=1400,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def build_risk_story_live(data: dict, provider: str) -> dict:
    prompt = f"""Return JSON only.
Create a plain-language churn risk story from the account context below.
Do not output a numeric health score only — explain the situation as a narrative.

Context:
{json.dumps(data, indent=2)}

Return keys: summary, risk_story, primary_risks (list), stabilizers (list), next_call_focus (list), urgency."""
    try:
        raw = call_llm(prompt, provider)
    except Exception as e:
        print(f"⚠️  LLM call failed: {e}")
        print("   Falling back to manual mode with sample data.\n")
        return None
    for marker in ["```json", "```"]:
        if marker in raw:
            raw = raw.split(marker)[1].split("```")[0]
            break
    try:
        return json.loads(raw.strip())
    except Exception:
        return {"summary": raw, "risk_story": raw, "primary_risks": [], "stabilizers": [], "next_call_focus": [], "urgency": "unknown"}


def load_sample_data() -> dict:
    account_path = WORKFLOW_DIR / "sample_data" / "account.json"
    notes_path = WORKFLOW_DIR / "sample_data" / "notes.json"
    data = {}
    if account_path.exists():
        data.update(json.loads(account_path.read_text()))
    if notes_path.exists():
        data.update(json.loads(notes_path.read_text()))
    if not data:
        data = {
            "account_name": "TechFlow Inc",
            "recent_activity": "Login frequency dropped 40% over last 30 days.",
            "support_summary": "3 tickets in past 30 days; 1 open for 12 days.",
            "engagement_summary": "Skipped last 2 monthly check-ins.",
        }
    return data


def main():
    config = load_config()
    llm_provider = get_llm_provider(config)
    account_name = config.get("account_name") or os.getenv("ACCOUNT_NAME", "TechFlow Inc")
    csm_name = config.get("csm_name") or os.getenv("CSM_NAME", "Alex Chen")

    print("=" * 60)
    print("  Churn Risk Summarizer")
    print("=" * 60)
    print(f"  Account : {account_name}")
    print(f"  CSM     : {csm_name}")

    use_manual = llm_provider == "manual" or not has_valid_key(llm_provider)

    if use_manual:
        if llm_provider != "manual":
            print(f"\n⚠️  No valid {llm_provider.upper()} API key found.")
            print("   Running in manual mode using sample_data/.\n")
            print("   To use live LLM: add your key to .env and set provider.llm in config.yaml\n")
        else:
            print(f"\n📂 Mode: manual (loading sample_data/)\n")

        data = load_sample_data()
        result = MOCK_OUTPUT
    else:
        print(f"\n🤖 Mode: live LLM ({llm_provider})\n")
        data = {
            "account_name": account_name,
            "recent_activity": os.getenv("RECENT_ACTIVITY", "Login frequency dropped 40% over last 30 days. 2 users haven't logged in since February."),
            "support_summary": os.getenv("SUPPORT_SUMMARY", "3 tickets in past 30 days: 2 resolved quickly, 1 open for 12 days (integration issue). Frustrated tone in latest reply."),
            "engagement_summary": os.getenv("ENGAGEMENT_SUMMARY", "Skipped last 2 monthly check-ins. NPS dropped from 8 to 6 in last survey."),
        }
        result = build_risk_story_live(data, llm_provider)
        if result is None:
            data = load_sample_data()
            result = MOCK_OUTPUT

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
