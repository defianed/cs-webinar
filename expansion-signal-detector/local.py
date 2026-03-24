#!/usr/bin/env python3
"""
Expansion Signal Detector — local runner (no Modal required)
Run: python3 local.py

Runs the full workflow logic locally. Requires ANTHROPIC_API_KEY or OPENAI_API_KEY in .env
"""
import os, json, sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_provider():
    if (os.getenv("ANTHROPIC_API_KEY") or "").strip():
        return os.getenv("LLM_PROVIDER", "anthropic")
    if (os.getenv("OPENAI_API_KEY") or "").strip():
        return "openai"
    return None


def call_llm(prompt: str) -> str:
    provider = get_provider()
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


def detect_expansion_signals(data: dict) -> dict:
    prompt = f"""Return JSON only.
Analyse this account context for expansion readiness signals.

Context:
{json.dumps(data, indent=2)}

Return keys: expansion_ready (bool), confidence (0.0-1.0), buying_signals (list), blockers (list), recommended_timing, next_steps (list), rationale."""
    raw = call_llm(prompt)
    for marker in ["```json", "```"]:
        if marker in raw:
            raw = raw.split(marker)[1].split("```")[0]
            break
    try:
        return json.loads(raw.strip())
    except Exception:
        return {"expansion_ready": False, "confidence": 0.0, "rationale": "Parse error.", "buying_signals": [], "blockers": [], "recommended_timing": "unknown", "next_steps": []}


def main():
    provider = get_provider()
    if not provider:
        print("ERROR: No API key found. Add ANTHROPIC_API_KEY or OPENAI_API_KEY to your .env file.")
        print("       cp .env.example .env  — then fill in your key.")
        sys.exit(1)

    data = {
        "account_name": os.getenv("ACCOUNT_NAME", "ScaleUp Ltd"),
        "transcript_snippets": os.getenv("TRANSCRIPT_SNIPPETS", "We're rolling this out to the sales team next quarter... this has transformed our workflow... asked about pricing for 20 more seats"),
        "post_call_notes": os.getenv("POST_CALL_NOTES", "Champion mentioned they're at 95 seats and approaching their limit. Discussed expansion pricing briefly. Budget opens in Q3."),
        "usage_summary": os.getenv("USAGE_SUMMARY", "95 of 100 seats active. API calls up 40% month-over-month. 3 power users in engineering team."),
    }

    print(f"Expansion Signal Detector — running locally with {provider}")
    print(f"Account: {data['account_name']}\n")

    result = detect_expansion_signals(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
