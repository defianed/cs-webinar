# Invisible Handoff — Sample Output

## Slack Message (sent to incoming CSM)

```
📋 Handoff Brief Ready — Acme Corp ($48K ACV)

Deal closed 2026-03-20 by Jake Hoffman. CSM: Sam Rivera.

Quick read before your first call 👇

Account: 200-person fintech. Replacing 3 legacy tools with our platform.
Q3 launch is a HARD deadline — their product team is building on top of the API.

Key people:
• Sarah Okonkwo (VP Eng) — your champion. She drove the whole eval. Day-to-day contact.
• Mike Chen (CTO) — economic buyer. Skeptical. Been burned before on vendor timelines.
  Do NOT hedge on the API GA date in front of Mike.
• James (DevOps) — wasn't in any demos. Will do the actual integration work.
  Get him into the kickoff. He can be a blocker if he feels ignored.

Commitments we made:
✅ API GA by May 15 — confirmed with product
✅ Marcus (onboarding engineer) assigned for 30 days
✅ Custom migration guide for Node.js + Postgres
✅ 50/50 milestone payment agreed

First call agenda suggestion:
1. Introduce Marcus — confirm his availability
2. Confirm API GA date in writing, in the call
3. Get James on the kickoff invite
4. Walk through migration guide outline together
5. Set weekly sync cadence through Q3 launch

Full brief below ↓
```

## Analysis JSON

```json
{
  "account_overview": "Acme Corp is a 200-person fintech company that closed a $48K ACV deal on 2026-03-20. Sarah (VP Engineering) is the champion who drove the full evaluation. Mike (CTO) holds budget and was skeptical — he's been burned by vendor timeline promises before. The deal closed faster than average because they were actively evaluating two other vendors.",
  "customer_goals": [
    "Replace fragmented toolchain (3 tools → 1 platform) by Q3",
    "Reduce time-to-integrate from 3 weeks to under 5 days",
    "Hit Q3 product launch deadline with new API layer in place"
  ],
  "pain_points": [
    "Previous vendor had good uptime but terrible support SLAs — left them stranded",
    "Engineering team is stretched — any migration overhead is costly",
    "CTO is skeptical of vendor commitments after being burned before"
  ],
  "commitments_made": [
    "API GA by May 15 — confirmed with product team",
    "Dedicated onboarding engineer (Marcus) for first 30 days",
    "Custom migration guide for Node.js + Postgres stack",
    "Milestone-based payment: 50% at kickoff, 50% at API GA"
  ],
  "objections_handled": [
    "Security: SOC 2 Type II + pen test report reviewed and approved",
    "Migration effort: committed to co-building migration guide",
    "Pricing: milestone-based payment schedule agreed",
    "Competitor comparison: outlined 3 technical differentiators vs DataBridge"
  ],
  "key_stakeholders": [
    {"name": "Sarah Okonkwo", "title": "VP Engineering", "role": "Champion — drove evaluation, day-to-day contact"},
    {"name": "Mike Chen", "title": "CTO", "role": "Economic buyer — skeptical, needs action not promises"},
    {"name": "James", "title": "Senior DevOps", "role": "Will own the integration — wasn't in demo, get him into kickoff"}
  ],
  "urgency_timeline": "Q3 launch deadline is hard. API GA date is May 15. First CSM call must happen within 48 hours of deal close.",
  "watchouts": [
    "Mike's skepticism is real — do not hedge on the API GA date in his presence",
    "API GA date is tight — reconfirm with product before first call",
    "James wasn't in any demos — he will have his own concerns, get him on kickoff"
  ],
  "suggested_first_call_agenda": [
    "Introduce Marcus (onboarding engineer) and confirm his 30-day availability",
    "Confirm API GA date on the call — show it in writing",
    "Get James added to kickoff invite — ask Sarah to facilitate",
    "Walk through migration guide outline together",
    "Set weekly sync cadence through Q3 launch"
  ]
}
```
