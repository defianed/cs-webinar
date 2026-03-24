#!/usr/bin/env python3
"""
Trust Radar — local runner (no Modal required)
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

SYSTEM_PROMPT = """You are an expert CS analyst specialising in trust signals during win-back and escalation calls.

Classify trust status as one of:
- GENUINE_LOSS_OF_TRUST: real relationship damage, needs repair before anything else
- NEGOTIATING: customer is using dissatisfaction as leverage for concessions
- MIXED: genuine frustration with openness to repair
- UNCLEAR: insufficient signal to classify

Return JSON with keys:
classification, confidence (0.0-1.0), reasoning,
evidence_snippets (list of {timestamp, speaker, text, signal_type, confidence}),
response_strategy, urgency_score (1-10), recommended_actions (list)."""

# ── MOCK OUTPUT (mirrors test.py) ─────────────────────────────────────────────
MOCK_OUTPUT = {
    "classification": "NEGOTIATING",
    "confidence": 0.79,
    "reasoning": "The customer's frustration is real — three missed commitments is legitimately damaging — but the language pattern is classic negotiation, not relationship exit. The conditional offer at 11:04 ('If you can get the API live this week... I'll hold off the evaluation') is the tell. Someone who has genuinely lost trust doesn't give you an out. They leave. She's giving you a very specific, actionable bar to clear.",
    "evidence_snippets": [
        {
            "timestamp": "08:45",
            "speaker": "Sarah",
            "text": "You've missed three commitments in a row. The API was supposed to be live in January. It's March.",
            "signal_type": "genuine_frustration",
            "confidence": 0.92
        },
        {
            "timestamp": "10:02",
            "speaker": "Sarah",
            "text": "We're actively evaluating Salesforce and HubSpot right now. Just so you're aware.",
            "signal_type": "negotiation_leverage",
            "confidence": 0.85
        },
        {
            "timestamp": "11:04",
            "speaker": "Sarah",
            "text": "If you can get the API live this week and give me a written commitment on the next two milestones, I'll hold off the evaluation.",
            "signal_type": "conditional_opening",
            "confidence": 0.88
        },
        {
            "timestamp": "11:52",
            "speaker": "Sarah",
            "text": "Okay. But I mean it — this is the last chance.",
            "signal_type": "urgency_signal",
            "confidence": 0.75
        }
    ],
    "response_strategy": "Do not get defensive. Do not hedge. Go away from this call and confirm the API date with engineering today. Come back within 24 hours with: (1) confirmed API GA date in writing, (2) written commitment on the next two milestones with specific dates, (3) a weekly sync with PM present. She's given you a specific bar — clear it.",
    "urgency_score": 8,
    "recommended_actions": [
        "Confirm API GA date with engineering before end of day",
        "Draft written commitment letter — specific dates, no ranges",
        "Schedule follow-up within 24 hours — bring PM",
        "Propose PM-led weekly milestone syncs until resolved"
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


def call_llm(system: str, user: str, provider: str) -> str:
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=1500,
            response_format={"type": "json_object"},
        )
        return resp.choices[0].message.content
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-opus-4-6"),
        max_tokens=1500,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text


def analyse_trust_live(data: dict, provider: str) -> dict:
    user_msg = f"Analyse this call and return your classification as JSON.\n\n{json.dumps(data, indent=2)}"
    try:
        raw = call_llm(SYSTEM_PROMPT, user_msg, provider)
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
        return {
            "classification": "UNCLEAR",
            "confidence": 0.0,
            "reasoning": f"Parse error. Raw: {raw[:300]}",
            "evidence_snippets": [],
            "response_strategy": "Manual review required.",
            "urgency_score": 5,
            "recommended_actions": ["Review transcript manually"],
        }


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
            "customer_name": "Acme Corp",
            "transcript": "[08:45] Sarah: You've missed three commitments in a row.\n[11:04] Sarah: If you can get the API live this week, I'll hold off the evaluation.",
        }
    return data


def main():
    config = load_config()
    llm_provider = get_llm_provider(config)
    account_name = config.get("account_name") or os.getenv("ACCOUNT_NAME", "Acme Corp")
    csm_name = config.get("csm_name") or os.getenv("CSM_NAME", "Taylor Brooks")

    print("=" * 60)
    print("  Trust Radar")
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
            "customer_name": account_name,
            "transcript": os.getenv("TRANSCRIPT_TEXT",
                "[08:45] Sarah: You've missed three commitments in a row. The API was supposed to be live in January. It's March.\n"
                "[09:15] Sarah: We built our entire Q1 onboarding workflow around that API. We had to do everything manually.\n"
                "[10:02] Sarah: We're actively evaluating Salesforce and HubSpot right now. Just so you're aware.\n"
                "[10:31] Sarah: I don't know. Maybe. But I need to see action, not promises.\n"
                "[11:04] Sarah: If you can get the API live this week and give me a written commitment on the next two milestones, I'll hold off the evaluation.\n"
                "[11:52] Sarah: Okay. But I mean it — this is the last chance."),
        }
        result = analyse_trust_live(data, llm_provider)
        if result is None:
            data = load_sample_data()
            result = MOCK_OUTPUT

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
