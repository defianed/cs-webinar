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

print(f"Testing Invisible Handoff with account: {sample['account_name']}\n")
result = build_brief(sample)
print(json.dumps(result, indent=2))
