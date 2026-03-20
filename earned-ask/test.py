# Local test — no Modal required. Run: python3 test.py
import os, json

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Use env vars already set in shell


def call_llm(prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "anthropic")
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )
        return resp.choices[0].message.content
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def build_review_request(data: dict) -> dict:
    prompt = f"""Return JSON only.
Given the milestone context below, decide if a review request is earned and draft a customer-facing email.

Context:
{json.dumps(data, indent=2)}

Return keys: should_ask (bool), reason, subject_line, email_body, csm_notes."""
    raw = call_llm(prompt)
    for marker in ["```json", "```"]:
        if marker in raw:
            raw = raw.split(marker)[1].split("```")[0]
            break
    try:
        return json.loads(raw.strip())
    except Exception:
        return {"should_ask": False, "reason": "Parse error", "raw": raw[:500]}


sample = {
    "account_name": os.getenv("ACCOUNT_NAME", "Acme Corp"),
    "milestone_achieved": os.getenv("MILESTONE_ACHIEVED", "Customer went live ahead of schedule, first full month complete"),
    "interaction_summary": os.getenv("INTERACTION_SUMMARY", "Champion said she would recommend us to peers on last QBR"),
    "sentiment_summary": os.getenv("SENTIMENT_SUMMARY", "NPS 9 submitted yesterday, recent tickets resolved same-day"),
}

print(f"Testing Earned Ask with account: {sample['account_name']}\n")
result = build_review_request(sample)
print(json.dumps(result, indent=2))
