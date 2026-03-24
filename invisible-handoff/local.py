#!/usr/bin/env python3
"""
Invisible Handoff — local runner (no Modal required)
Run: python3 local.py

Runs the full workflow logic locally. Requires ANTHROPIC_API_KEY or OPENAI_API_KEY in .env
"""
import os, json, sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_provider():
    if (os.getenv("ANTHROPIC_API_KEY") or "").strip():
        return os.getenv("LLM_PROVIDER", "anthropic")
    if (os.getenv("OPENAI_API_KEY") or "").strip():
        return "openai"
    return None


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
        model=os.getenv("ANTHROPIC_MODEL", "claude-opus-4-6"),
        max_tokens=1400,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def build_handoff_brief(data: dict) -> dict:
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


def main():
    provider = get_provider()
    if not provider:
        print("ERROR: No API key found. Add ANTHROPIC_API_KEY or OPENAI_API_KEY to your .env file.")
        print("       cp .env.example .env  — then fill in your key.")
        sys.exit(1)

    data = {
        "account_name": os.getenv("ACCOUNT_NAME", "Acme Corp"),
        "deal_value": os.getenv("DEAL_VALUE", "$48,000 ACV"),
        "transcript_summary": os.getenv("TRANSCRIPT_SUMMARY", "Closed Won. Final call confirmed API GA, dedicated onboarding engineer, and milestone-based payments."),
        "sales_rep_notes": os.getenv("SALES_REP_NOTES", "Champion is Sarah VP Eng. CTO Mike is skeptical. Q3 launch is hard deadline. Watch James in DevOps — wasn't in demo."),
    }

    print(f"Invisible Handoff — running locally with {provider}")
    print(f"Account: {data['account_name']}\n")

    result = build_handoff_brief(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
