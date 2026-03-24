# Local test — no Modal required. Run: python3 test.py
# To run with live AI: python3 test.py --live
import os, json, sys

LIVE_MODE = "--live" in sys.argv

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


ACCOUNT_NAME = os.getenv("ACCOUNT_NAME", "ScaleUp Ltd")

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


def has_api_key() -> bool:
    return bool((os.getenv("ANTHROPIC_API_KEY") or "").strip()) or bool((os.getenv("OPENAI_API_KEY") or "").strip())


def get_provider() -> str:
    """Auto-detect provider from which key is actually set."""
    explicit = os.getenv("LLM_PROVIDER", "").strip()
    if explicit:
        return explicit
    if (os.getenv("ANTHROPIC_API_KEY") or "").strip():
        return "anthropic"
    if (os.getenv("OPENAI_API_KEY") or "").strip():
        return "openai"
    return "anthropic"



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
        return {"expansion_ready": False, "confidence": 0.0, "rationale": f"Parse error.", "buying_signals": [], "blockers": [], "recommended_timing": "unknown", "next_steps": []}


print(f"Testing Expansion Signal Detector with account: {ACCOUNT_NAME}\n")

if not LIVE_MODE:
    print("Sample output — run with: python3 test.py --live  (requires ANTHROPIC_API_KEY or OPENAI_API_KEY in .env)\n")
    print(json.dumps(MOCK_OUTPUT, indent=2))
else:
    sample = {
        "account_name": ACCOUNT_NAME,
        "transcript_snippets": os.getenv("TRANSCRIPT_SNIPPETS", "We're rolling this out to the sales team next quarter... this has transformed our workflow... asked about pricing for 20 more seats"),
        "post_call_notes": os.getenv("POST_CALL_NOTES", "Champion mentioned they're at 95 seats and approaching their limit. Discussed expansion pricing briefly. Budget opens in Q3."),
        "usage_summary": os.getenv("USAGE_SUMMARY", "95 of 100 seats active. API calls up 40% month-over-month. 3 power users in engineering team."),
    }
    result = detect_expansion_signals(sample)
    print(json.dumps(result, indent=2))
