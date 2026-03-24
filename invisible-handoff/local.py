#!/usr/bin/env python3
"""
Invisible Handoff — local runner (no Modal required)
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
    "account_overview": "Acme Corp is a 200-person fintech company that closed a $48K ACV deal. Sarah (VP Engineering) is the champion; Mike (CTO) holds budget. Deal closed faster than average — they were actively evaluating two other vendors.",
    "customer_goals": [
        "Reduce time-to-integrate from 3 weeks to under 5 days",
        "Replace their current fragmented toolchain (3 tools → 1 platform)",
        "Hit their Q3 product launch with the new API layer in place"
    ],
    "pain_points": [
        "Previous vendor had good uptime but terrible support SLAs — left them stranded",
        "Engineering team is stretched thin — any migration overhead is costly",
        "Their CTO is skeptical of vendor commitments after being burned before"
    ],
    "commitments_made": [
        "API will be GA by May 15 — confirmed with product",
        "Dedicated onboarding engineer (Marcus) assigned for 30 days",
        "Custom migration guide for their stack (Node.js + Postgres)"
    ],
    "objections_handled": [
        "Security: SOC 2 Type II + pen test report shared and reviewed",
        "Pricing: Agreed to milestone-based payment schedule",
        "Migration effort: Committed to co-building migration guide"
    ],
    "key_stakeholders": [
        {"name": "Sarah", "title": "VP Engineering", "role": "Champion — drove evaluation, day-to-day contact"},
        {"name": "Mike", "title": "CTO", "role": "Economic buyer — skeptical, needs to see action not promises"},
        {"name": "James", "title": "Senior DevOps", "role": "Will own the integration — address his operational concerns early"}
    ],
    "urgency_timeline": "Q3 launch deadline is hard. API GA date is May 15. First CSM call should happen within 48 hours of deal close.",
    "watchouts": [
        "Mike's skepticism is real — he's been burned before. Do not overpromise in early calls.",
        "API GA date is tight. Confirm with product before first call and do not hedge.",
        "James wasn't in the demo. He'll have his own concerns. Get him into the kickoff."
    ],
    "suggested_first_call_agenda": [
        "1. Introduce Marcus (onboarding engineer) and confirm availability",
        "2. Confirm API GA date and show it in writing",
        "3. Walk through migration guide outline — get James involved",
        "4. Set weekly check-in cadence through Q3 launch"
    ]
}


def load_config() -> dict:
    config_path = WORKFLOW_DIR / "config.yaml"
    if _YAML_AVAILABLE and config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f) or {}
    return {}


def get_llm_provider(config: dict) -> str:
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


def build_handoff_brief_live(data: dict, provider: str) -> dict:
    prompt = f"""Return JSON only.
Create a CSM handoff brief from the sales context below.

Context:
{json.dumps(data, indent=2)}

Return keys: account_overview, customer_goals (list), pain_points (list), commitments_made (list), objections_handled (list), key_stakeholders (list of objects with name/title/role), urgency_timeline, watchouts (list), suggested_first_call_agenda (list)."""
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
        return {"account_overview": raw, "parse_error": True}


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
            "account_name": "Acme Corp",
            "deal_value": "$48,000 ACV",
            "transcript_summary": "Closed Won. Final call confirmed API GA, dedicated onboarding engineer, and milestone-based payments.",
            "sales_rep_notes": "Champion is Sarah VP Eng. CTO Mike is skeptical. Q3 launch is hard deadline.",
        }
    return data


def main():
    config = load_config()
    llm_provider = get_llm_provider(config)
    account_name = config.get("account_name") or os.getenv("ACCOUNT_NAME", "Acme Corp")
    csm_name = config.get("csm_name") or os.getenv("CSM_NAME", "Sam Rivera")

    print("=" * 60)
    print("  Invisible Handoff")
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
            "deal_value": os.getenv("DEAL_VALUE", "$48,000 ACV"),
            "transcript_summary": os.getenv("TRANSCRIPT_SUMMARY", "Closed Won. Final call confirmed API GA, dedicated onboarding engineer, and milestone-based payments."),
            "sales_rep_notes": os.getenv("SALES_REP_NOTES", "Champion is Sarah VP Eng. CTO Mike is skeptical. Q3 launch is hard deadline. Watch James in DevOps — wasn't in demo."),
        }
        result = build_handoff_brief_live(data, llm_provider)
        if result is None:
            data = load_sample_data()
            result = MOCK_OUTPUT

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
