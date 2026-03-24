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

# --- No API key? Show mock output and exit ---
if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    print("No API key set — showing mock output. Set ANTHROPIC_API_KEY in .env to run with real AI.\n")
    mock = {
        "should_ask": True,
        "reason": "Customer just hit a major milestone (went live ahead of schedule), champion expressed intent to recommend peers, and NPS is 9. This is the ideal moment — positive sentiment is high and the value is fresh in their mind.",
        "subject_line": "Quick favour from one of our favourite customers?",
        "email_body": "Hi Sarah,\n\nReally glad to hear the first month went so well — going live ahead of schedule is no small thing, and it reflects how seriously your team took the rollout.\n\nWe're building out our G2 profile and a review from you would mean a lot right now. Takes about 3 minutes and I can send you a direct link.\n\nOnly if you're happy to — no pressure at all.\n\n[Your name]",
        "csm_notes": "Sarah is warm and has already said she'd recommend us. Send this week while the momentum is fresh. If she agrees, send the G2 link directly. Don't wait more than 5 days."
    }
    print(json.dumps(mock, indent=2))
    raise SystemExit(0)

print(f"Testing Earned Ask with account: {sample['account_name']}\n")
result = build_review_request(sample)
print(json.dumps(result, indent=2))
