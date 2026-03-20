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


sample = {
    "account_name": os.getenv("ACCOUNT_NAME", "TechFlow Inc"),
    "recent_activity": os.getenv("RECENT_ACTIVITY", "Login frequency dropped 40% over last 30 days. 2 users haven't logged in since February."),
    "support_summary": os.getenv("SUPPORT_SUMMARY", "3 tickets in past 30 days: 2 resolved quickly, 1 open for 12 days (integration issue). Frustrated tone in latest reply."),
    "engagement_summary": os.getenv("ENGAGEMENT_SUMMARY", "Skipped last 2 monthly check-ins. NPS dropped from 8 to 6 in last survey."),
}

print(f"Testing Churn Risk Summarizer with account: {sample['account_name']}\n")
result = build_risk_story(sample)
print(json.dumps(result, indent=2))
