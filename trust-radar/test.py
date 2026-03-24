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
    "classification": "NEGOTIATING",
    "confidence": 0.79,
    "reasoning": "The customer's frustration is real — three missed commitments is legitimately damaging — but the language pattern is classic negotiation, not relationship exit. The conditional offer at 11:04 ('If you can get the API live this week... I'll hold off the evaluation') is the tell. Someone who has genuinely lost trust doesn't give you an out. They leave. She's giving you a very specific, actionable bar to clear.",
    "evidence_snippets": [
        {
            "timestamp": "08:45",
            "speaker": "Sarah",
            "text": "You've missed three commitments in a row. The API was supposed to be live in January. It's March.",
            "signal_type": "genuine_frustration",
            "confidence": 0.92
        },
        {
            "timestamp": "10:02",
            "speaker": "Sarah",
            "text": "We're actively evaluating Salesforce and HubSpot right now. Just so you're aware.",
            "signal_type": "negotiation_leverage",
            "confidence": 0.85
        },
        {
            "timestamp": "11:04",
            "speaker": "Sarah",
            "text": "If you can get the API live this week and give me a written commitment on the next two milestones, I'll hold off the evaluation.",
            "signal_type": "conditional_opening",
            "confidence": 0.88
        },
        {
            "timestamp": "11:52",
            "speaker": "Sarah",
            "text": "Okay. But I mean it — this is the last chance.",
            "signal_type": "urgency_signal",
            "confidence": 0.75
        }
    ],
    "response_strategy": "Do not get defensive. Do not hedge. Go away from this call and confirm the API date with engineering today. Come back within 24 hours with: (1) confirmed API GA date in writing, (2) written commitment on the next two milestones with specific dates, (3) a weekly sync with PM present. She's given you a specific bar — clear it.",
    "urgency_score": 8,
    "recommended_actions": [
        "Confirm API GA date with engineering before end of day",
        "Draft written commitment letter — specific dates, no ranges",
        "Schedule follow-up within 24 hours — bring PM",
        "Propose PM-led weekly milestone syncs until resolved"
    ]
}

SYSTEM_PROMPT = """You are an expert CS analyst specialising in trust signals during win-back and escalation calls.

Classify trust status as one of:
- GENUINE_LOSS_OF_TRUST: real relationship damage, needs repair before anything else
- NEGOTIATING: customer is using dissatisfaction as leverage for concessions
- MIXED: genuine frustration with openness to repair
- UNCLEAR: insufficient signal to classify

Return JSON with keys:
classification, confidence (0.0-1.0), reasoning, 
evidence_snippets (list of {timestamp, speaker, text, signal_type, confidence}),
response_strategy, urgency_score (1-10), recommended_actions (list)."""


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



def call_llm(system: str, user: str) -> str:
    provider = get_provider()
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=1500,
            response_format={"type": "json_object"},
        )
        return resp.choices[0].message.content
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-opus-4-6"),
        max_tokens=1500,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text


def analyse_trust(data: dict) -> dict:
    user_msg = f"Analyse this call and return your classification as JSON.\n\n{json.dumps(data, indent=2)}"
    raw = call_llm(SYSTEM_PROMPT, user_msg)
    for marker in ["```json", "```"]:
        if marker in raw:
            raw = raw.split(marker)[1].split("```")[0]
            break
    try:
        return json.loads(raw.strip())
    except Exception:
        return {
            "classification": "UNCLEAR",
            "confidence": 0.0,
            "reasoning": f"Parse error. Raw: {raw[:300]}",
            "evidence_snippets": [],
            "response_strategy": "Manual review required.",
            "urgency_score": 5,
            "recommended_actions": ["Review transcript manually"],
        }


print(f"Testing Trust Radar with account: {ACCOUNT_NAME}\n")

if not LIVE_MODE:
    print("Sample output — run with: python3 test.py --live  (requires ANTHROPIC_API_KEY or OPENAI_API_KEY in .env)\n")
    print(json.dumps(MOCK_OUTPUT, indent=2))
else:
    sample = {
        "customer_name": ACCOUNT_NAME,
        "transcript": os.getenv("TRANSCRIPT_TEXT",
            "[08:45] Sarah: You've missed three commitments in a row. The API was supposed to be live in January. It's March.\n"
            "[09:15] Sarah: We built our entire Q1 onboarding workflow around that API. We had to do everything manually.\n"
            "[10:02] Sarah: We're actively evaluating Salesforce and HubSpot right now. Just so you're aware.\n"
            "[10:31] Sarah: I don't know. Maybe. But I need to see action, not promises.\n"
            "[11:04] Sarah: If you can get the API live this week and give me a written commitment on the next two milestones, I'll hold off the evaluation.\n"
            "[11:52] Sarah: Okay. But I mean it — this is the last chance."),
    }
    result = analyse_trust(sample)
    print(json.dumps(result, indent=2))
