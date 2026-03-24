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
    prompt = f"""Create a JSON CSM handoff brief from the context below.

Context:
{json.dumps(data, indent=2)}

Return JSON with keys:
customer_goals (list), pain_points (list), commitments_made (list), objections_raised (list),
stakeholder_map (list), communication_style, onboarding_risks (list),
first_call_agenda (list), top_3_watchouts (list), brief_summary.

Return valid JSON only."""
    raw = call_llm(prompt)
    for marker in ["```json", "```"]:
        if marker in raw:
            raw = raw.split(marker)[1].split("```")[0]
            break
    try:
        return json.loads(raw.strip())
    except Exception:
        return {"brief_summary": raw, "top_3_watchouts": [], "customer_goals": []}


sample = {
    "account_name": os.getenv("ACCOUNT_NAME", "Acme Corp"),
    "transcript_text": os.getenv("TRANSCRIPT_TEXT",
        "Sales promised API access in month 1 and a custom onboarding doc within 2 weeks. "
        "Customer's main goal is cutting manual onboarding time by 50%. "
        "IT approval still needed for the API integration. "
        "Champion Sarah is leaving in 6 weeks — need to build relationship with her replacement."),
    "opportunity_id": os.getenv("OPPORTUNITY_ID", "OPP-001"),
    "account_id": os.getenv("ACCOUNT_ID", "ACC-001"),
}

# --- No API key? Show mock output and exit ---
if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    print("No API key set — showing mock output. Set ANTHROPIC_API_KEY in .env to run with real AI.\n")
    mock = {
        "customer_goals": [
            "Cut manual onboarding time by 50%",
            "Replace manual CSV exports with API-driven workflow"
        ],
        "pain_points": [
            "Current process requires 3 manual steps per account",
            "No API access in current plan"
        ],
        "commitments_made": [
            "API access delivered in month 1",
            "Custom onboarding doc within 2 weeks of go-live"
        ],
        "objections_raised": [
            "IT approval still required for API integration — not yet started"
        ],
        "stakeholder_map": [
            "Sarah (Champion) — leaving in 6 weeks, need to identify replacement",
            "IT team (Blocker) — must approve API integration before go-live"
        ],
        "communication_style": "Detail-oriented, prefers written summaries over verbal updates",
        "onboarding_risks": [
            "IT approval not secured — flag this in the first call",
            "Champion Sarah departing in 6 weeks — relationship continuity at risk"
        ],
        "first_call_agenda": [
            "Confirm onboarding timeline and API access date",
            "Introduce CSM process and cadence",
            "Identify IT contact for integration approval",
            "Set 30/60/90 day success metrics"
        ],
        "top_3_watchouts": [
            "IT approval not secured — make this the first priority",
            "Sales promised custom onboarding doc — coordinate with solutions team immediately",
            "Champion Sarah leaving in 6 weeks — start building relationship with her replacement now"
        ],
        "brief_summary": "Acme is focused on cutting manual ops work. Sales committed to API access and a custom onboarding doc. IT approval is the main blocker. Champion Sarah is engaged but leaving soon — prioritise getting a second contact before she goes."
    }
    print(json.dumps(mock, indent=2))
    raise SystemExit(0)

print(f"Testing Invisible Handoff with account: {sample['account_name']}\n")
result = build_brief(sample)
print(json.dumps(result, indent=2))
