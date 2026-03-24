#!/usr/bin/env python3
"""
Earned Ask — local runner (no Modal required)
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
    "should_ask": True,
    "reason": "Acme Corp hit their go-live milestone ahead of schedule, their champion mentioned they'd recommend the product to peers, and they submitted a 9 NPS yesterday. This is a genuine earned ask.",
    "subject_line": "Quick favour — would mean a lot",
    "email_body": "Hi [Champion Name],\n\nJust wanted to say — watching your team hit go-live ahead of schedule was genuinely one of those moments that reminds me why I love this work.\n\nIf you've got 2 minutes, would you mind leaving us a review on G2? Even a sentence about what's worked would make a big difference for us.\n\n[G2 Review Link]\n\nNo pressure at all — and thanks again for being such a great partner through the onboarding.\n\n[CSM Name]",
    "csm_notes": "This is an earned ask. Send it. Don't overthink it. They gave you a 9 NPS and their champion is already promoting you internally."
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
            max_tokens=1000,
        )
        return resp.choices[0].message.content
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-opus-4-6"),
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def build_review_request_live(data: dict, provider: str) -> dict:
    prompt = f"""Return JSON only.
Given the milestone context below, decide if a review request is earned and draft a customer-facing email.

Context:
{json.dumps(data, indent=2)}

Return keys: should_ask (bool), reason, subject_line, email_body, csm_notes."""
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
        return {"should_ask": False, "reason": "Parse error", "raw": raw[:500]}


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
            "milestone_achieved": "Customer went live ahead of schedule",
            "interaction_summary": "Champion said she would recommend us to peers",
            "sentiment_summary": "NPS 9 submitted yesterday",
        }
    return data


def main():
    config = load_config()
    llm_provider = get_llm_provider(config)
    account_name = config.get("account_name") or os.getenv("ACCOUNT_NAME", "Acme Corp")
    csm_name = config.get("csm_name") or os.getenv("CSM_NAME", "Jordan Kim")

    print("=" * 60)
    print("  Earned Ask")
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
            "milestone_achieved": os.getenv("MILESTONE_ACHIEVED", "Customer went live ahead of schedule, first full month complete"),
            "interaction_summary": os.getenv("INTERACTION_SUMMARY", "Champion said she would recommend us to peers on last QBR"),
            "sentiment_summary": os.getenv("SENTIMENT_SUMMARY", "NPS 9 submitted yesterday, recent tickets resolved same-day"),
        }
        result = build_review_request_live(data, llm_provider)
        if result is None:
            data = load_sample_data()
            result = MOCK_OUTPUT

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
