# Local test — no Modal required. Run: python3 test.py
# To run with live AI: python3 test.py --live
import os, json, sys

LIVE_MODE = "--live" in sys.argv

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


ACCOUNT_NAME = os.getenv("ACCOUNT_NAME", "TechFlow Inc")

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
            max_tokens=1400,
        )
        return resp.choices[0].message.content
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        max_tokens=1400,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def build_risk_story(data: dict) -> dict:
    prompt = f"""Return JSON only.
Create a plain-language churn risk story from the account context below.
Do not output a numeric health score only — explain the situation as a narrative.

Context:
{json.dumps(data, indent=2)}

Return keys: summary, risk_story, primary_risks (list), stabilizers (list), next_call_focus (list), urgency."""
    raw = call_llm(prompt)
    for marker in ["```json", "```"]:
        if marker in raw:
            raw = raw.split(marker)[1].split("```")[0]
            break
    try:
        return json.loads(raw.strip())
    except Exception:
        return {"summary": raw, "risk_story": raw, "primary_risks": [], "stabilizers": [], "next_call_focus": [], "urgency": "unknown"}


print(f"Testing Churn Risk Summarizer with account: {ACCOUNT_NAME}\n")

if not LIVE_MODE:
    print("Sample output — run with: python3 test.py --live  (requires ANTHROPIC_API_KEY or OPENAI_API_KEY in .env)\n")
    print(json.dumps(MOCK_OUTPUT, indent=2))
else:
    sample = {
        "account_name": ACCOUNT_NAME,
        "recent_activity": os.getenv("RECENT_ACTIVITY", "Login frequency dropped 40% over last 30 days. 2 users haven't logged in since February."),
        "support_summary": os.getenv("SUPPORT_SUMMARY", "3 tickets in past 30 days: 2 resolved quickly, 1 open for 12 days (integration issue). Frustrated tone in latest reply."),
        "engagement_summary": os.getenv("ENGAGEMENT_SUMMARY", "Skipped last 2 monthly check-ins. NPS dropped from 8 to 6 in last survey."),
    }
    result = build_risk_story(sample)
    print(json.dumps(result, indent=2))
