# Local test — no Modal required. Run: python3 test.py
import os, json

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def call_llm(prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "anthropic")
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
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def detect_expansion_signals(data: dict) -> dict:
    prompt = f"""Return JSON only.
Analyse the transcript and notes for expansion readiness signals.

Context:
{json.dumps(data, indent=2)}

Return keys: ready_for_expansion (bool), confidence (high/medium/low), buying_signals (list), blockers (list), recommended_next_action, summary."""
    raw = call_llm(prompt)
    for marker in ["```json", "```"]:
        if marker in raw:
            raw = raw.split(marker)[1].split("```")[0]
            break
    try:
        return json.loads(raw.strip())
    except Exception:
        return {"ready_for_expansion": False, "confidence": "low", "buying_signals": [], "blockers": [], "recommended_next_action": "Manual review", "summary": raw}


sample = {
    "account_name": os.getenv("ACCOUNT_NAME", "ScaleUp Ltd"),
    "transcript_text": os.getenv("TRANSCRIPT_TEXT", "We're rolling out to the EMEA team next quarter and want to understand your enterprise tier pricing. Also asked about multi-region support and bringing the finance team on."),
    "post_call_notes": os.getenv("POST_CALL_NOTES", "Customer proactively asked about API rate limits, suggesting higher volume needs."),
}

# --- No API key? Show mock output and exit ---
if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    print("No API key set — showing mock output. Set ANTHROPIC_API_KEY in .env to run with real AI.\n")
    mock = {
        "ready_for_expansion": True,
        "confidence": "high",
        "buying_signals": [
            "Explicitly asked about enterprise tier pricing",
            "Mentioned EMEA rollout planned for next quarter",
            "Asked about API rate limits — suggests higher volume needs",
            "Referenced bringing the finance team on"
        ],
        "blockers": [
            "Multi-region support availability not confirmed",
            "Budget approval may be required"
        ],
        "recommended_next_action": "Schedule a discovery call focused on enterprise tier — customer is signalling intent. Come prepared with volume pricing and multi-region specs.",
        "summary": "ScaleUp Ltd is showing strong expansion signals. They are planning a full EMEA rollout next quarter and proactively asked about enterprise features and API limits. High-confidence expansion opportunity — act within 2 weeks."
    }
    print(json.dumps(mock, indent=2))
    raise SystemExit(0)

print(f"Testing Expansion Signal Detector with account: {sample['account_name']}\n")
result = detect_expansion_signals(sample)
print(json.dumps(result, indent=2))
