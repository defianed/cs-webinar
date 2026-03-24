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
    "should_ask": True,
    "reason": "Acme Corp hit their go-live milestone ahead of schedule, their champion mentioned they'd recommend the product to peers, and they submitted a 9 NPS yesterday. This is a genuine earned ask.",
    "subject_line": "Quick favour — would mean a lot",
    "email_body": "Hi [Champion Name],\n\nJust wanted to say — watching your team hit go-live ahead of schedule was genuinely one of those moments that reminds me why I love this work.\n\nIf you've got 2 minutes, would you mind leaving us a review on G2? Even a sentence about what's worked would make a big difference for us.\n\n[G2 Review Link]\n\nNo pressure at all — and thanks again for being such a great partner through the onboarding.\n\n[CSM Name]",
    "csm_notes": "This is an earned ask. Send it. Don't overthink it. They gave you a 9 NPS and their champion is already promoting you internally."
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


print(f"Testing Earned Ask with account: {ACCOUNT_NAME}\n")

if not LIVE_MODE:
    print("Sample output — run with: python3 test.py --live  (requires ANTHROPIC_API_KEY or OPENAI_API_KEY in .env)\n")
    print(json.dumps(MOCK_OUTPUT, indent=2))
else:
    sample = {
        "account_name": ACCOUNT_NAME,
        "milestone_achieved": os.getenv("MILESTONE_ACHIEVED", "Customer went live ahead of schedule, first full month complete"),
        "interaction_summary": os.getenv("INTERACTION_SUMMARY", "Champion said she would recommend us to peers on last QBR"),
        "sentiment_summary": os.getenv("SENTIMENT_SUMMARY", "NPS 9 submitted yesterday, recent tickets resolved same-day"),
    }
    result = build_review_request(sample)
    print(json.dumps(result, indent=2))
