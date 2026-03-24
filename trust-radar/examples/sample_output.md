# Trust Radar — Sample Output

## Slack Message (sent to CSM + escalation lead)

```
🔍 Trust Radar Analysis — Acme Corp
Classification: NEGOTIATING (79% confidence)

This is NOT a genuine loss of trust — it's leverage.

Here's why: Someone who has genuinely lost trust doesn't give you an out.
They go quiet and start the procurement process. Sarah gave you a specific,
actionable bar to clear at 11:04: "Get the API live this week and give me
written commitments on the next two milestones."

That's not someone exiting — that's someone telling you exactly what she needs
to stay. The competitor mention (Salesforce, HubSpot) is leverage, not a
resignation letter.

Urgency Score: 8/10

You have a path. Use it.

Recommended actions:
1. Confirm API GA date with engineering TODAY (not tomorrow)
2. Draft written commitment letter — specific dates, no ranges
3. Follow up within 24 hours — bring your PM
4. Propose PM-led weekly milestone syncs until resolved

Key evidence snippets below ↓
```

## Analysis JSON

```json
{
  "classification": "NEGOTIATING",
  "confidence": 0.79,
  "reasoning": "The customer's frustration is real — three missed commitments caused genuine operational pain (40 hours of manual work). But the language pattern is classic negotiation, not relationship exit. The conditional offer at 11:04 is the tell: 'If you can get the API live this week... I'll hold off the evaluation.' Someone who has genuinely lost trust doesn't give you a specific, actionable bar to clear. They leave quietly and start procurement. She's giving you a very precise path to keep the account.",
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
      "confidence": 0.91
    },
    {
      "timestamp": "11:52",
      "speaker": "Sarah",
      "text": "Okay. But I mean it — this is the last chance.",
      "signal_type": "urgency_signal",
      "confidence": 0.75
    }
  ],
  "response_strategy": "Do not get defensive. Do not hedge. Confirm the API date with engineering today and come back within 24 hours with: (1) confirmed API GA date in writing, (2) written commitment on the next two milestones with specific dates — no ranges, (3) proposed PM-led weekly milestone syncs. She gave you a specific bar — clear it.",
  "urgency_score": 8,
  "recommended_actions": [
    "Confirm API GA date with engineering before end of day — do not guess",
    "Draft written commitment letter with specific dates (not ranges)",
    "Follow up with Sarah within 24 hours — bring PM to the call",
    "Propose PM-led weekly milestone syncs until API is stable",
    "Do not offer financial concessions yet — she hasn't asked for them"
  ]
}
```
