#!/usr/bin/env python3
"""
Expansion Signal Detector — local runner (no Modal required)
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
    "expansion_ready": True,
    "confidence": 0.81,
    "buying_signals": [
        "Mentioned rolling platform out to sales team next quarter",
        "At 95 of 100 seat capacity — naturally approaching plan limits",
        "Champion said 'this has transformed how we work'",
        "Proactively asked about pricing for additional seats"
    ],
    "blockers": [
        "Budget cycle restarts in Q3 — may need to wait for approval",
        "Current integration issue should be resolved first to avoid risk"
    ],
    "recommended_timing": "Initiate expansion conversation in 3-4 weeks once integration is resolved and Q3 budget opens",
    "next_steps": [
        "Get the integration ticket closed this week",
        "Prepare a custom expansion quote based on their stated headcount plans",
        "Schedule a dedicated expansion call — don't do this as an add-on to a check-in"
    ],
    "rationale": "ScaleUp is organically growing into expansion: they're near plan limits, the champion is vocal about ROI, and they're already thinking about broader rollout. The only thing holding this back is the integration issue and budget timing — both solvable."
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
            max_tokens=1200,
        )
        return resp.choices[0].message.content
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-opus-4-6"),
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def detect_expansion_signals_live(data: dict, provider: str) -> dict:
    prompt = f"""Return JSON only.
Analyse this account context for expansion readiness signals.

Context:
{json.dumps(data, indent=2)}

Return keys: expansion_ready (bool), confidence (0.0-1.0), buying_signals (list), blockers (list), recommended_timing, next_steps (list), rationale."""
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
        return {"expansion_ready": False, "confidence": 0.0, "rationale": "Parse error.", "buying_signals": [], "blockers": [], "recommended_timing": "unknown", "next_steps": []}


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
            "account_name": "ScaleUp Ltd",
            "transcript_snippets": "We're rolling this out to the sales team next quarter... asked about pricing for 20 more seats",
            "post_call_notes": "Champion mentioned they're at 95 seats and approaching their limit.",
            "usage_summary": "95 of 100 seats active. API calls up 40% month-over-month.",
        }
    return data


def main():
    config = load_config()
    llm_provider = get_llm_provider(config)
    account_name = config.get("account_name") or os.getenv("ACCOUNT_NAME", "ScaleUp Ltd")
    csm_name = config.get("csm_name") or os.getenv("CSM_NAME", "Riley Morgan")

    print("=" * 60)
    print("  Expansion Signal Detector")
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
            "transcript_snippets": os.getenv("TRANSCRIPT_SNIPPETS", "We're rolling this out to the sales team next quarter... this has transformed our workflow... asked about pricing for 20 more seats"),
            "post_call_notes": os.getenv("POST_CALL_NOTES", "Champion mentioned they're at 95 seats and approaching their limit. Discussed expansion pricing briefly. Budget opens in Q3."),
            "usage_summary": os.getenv("USAGE_SUMMARY", "95 of 100 seats active. API calls up 40% month-over-month. 3 power users in engineering team."),
        }
        result = detect_expansion_signals_live(data, llm_provider)
        if result is None:
            data = load_sample_data()
            result = MOCK_OUTPUT

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
