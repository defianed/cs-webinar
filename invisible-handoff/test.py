# Local test — no Modal required. Run: python3 test.py
# To run with live AI: python3 test.py --live
import os, json, sys

LIVE_MODE = "--live" in sys.argv

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


ACCOUNT_NAME = os.getenv("ACCOUNT_NAME", "Acme Corp")

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


def build_brief(data: dict) -> dict:
    prompt = f"""Return JSON only.
Create a CSM handoff brief from the sales context below.

Context:
{json.dumps(data, indent=2)}

Return keys: account_overview, customer_goals (list), pain_points (list), commitments_made (list), objections_handled (list), key_stakeholders (list of objects with name/title/role), urgency_timeline, watchouts (list), suggested_first_call_agenda (list)."""
    raw = call_llm(prompt)
    for marker in ["```json", "```"]:
        if marker in raw:
            raw = raw.split(marker)[1].split("```")[0]
            break
    try:
        return json.loads(raw.strip())
    except Exception:
        return {"account_overview": raw, "parse_error": True}


print(f"Testing Invisible Handoff with account: {ACCOUNT_NAME}\n")

if not LIVE_MODE:
    print("Sample output — run with: python3 test.py --live  (requires ANTHROPIC_API_KEY or OPENAI_API_KEY in .env)\n")
    print(json.dumps(MOCK_OUTPUT, indent=2))
else:
    sample = {
        "account_name": ACCOUNT_NAME,
        "deal_value": os.getenv("DEAL_VALUE", "$48,000 ACV"),
        "transcript_summary": os.getenv("TRANSCRIPT_SUMMARY", "Closed Won. Final call confirmed API GA, dedicated onboarding engineer, and milestone-based payments."),
        "sales_rep_notes": os.getenv("SALES_REP_NOTES", "Champion is Sarah VP Eng. CTO Mike is skeptical. Q3 launch is hard deadline. Watch James in DevOps — wasn't in demo."),
    }
    result = build_brief(sample)
    print(json.dumps(result, indent=2))
