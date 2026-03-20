# Local test — no Modal required. Run: python3 test.py
import os, json

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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


def call_llm(system: str, user: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "anthropic")
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
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
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


sample = {
    "customer_name": os.getenv("ACCOUNT_NAME", "Acme Corp"),
    "transcript": os.getenv("TRANSCRIPT_TEXT",
        "[08:45] Sarah: You've missed three commitments in a row. The API was supposed to be live in January. It's March.\n"
        "[09:15] Sarah: We built our entire Q1 onboarding workflow around that API. We had to do everything manually.\n"
        "[10:02] Sarah: We're actively evaluating Salesforce and HubSpot right now. Just so you're aware.\n"
        "[10:31] Sarah: I don't know. Maybe. But I need to see action, not promises.\n"
        "[11:04] Sarah: If you can get the API live this week and give me a written commitment on the next two milestones, I'll hold off the evaluation.\n"
        "[11:52] Sarah: Okay. But I mean it — this is the last chance."),
}

print(f"Testing Trust Radar with account: {sample['customer_name']}\n")
result = analyse_trust(sample)
print(json.dumps(result, indent=2))
