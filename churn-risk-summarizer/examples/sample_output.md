# Churn Risk Summarizer — Sample Output

## Slack Message (sent to CSM)

```
🔴 Churn Risk Alert — TechFlow Inc

📊 Urgency: HIGH

Summary: TechFlow started strong but has gone quiet over the past 30 days. Two previously active users have stopped logging in entirely. An open support ticket at 12 days is adding friction at exactly the wrong time.

Risk Story:
TechFlow was an enthusiastic customer in Q3, but the signals shifted in February. Dana hasn't logged in, the monthly check-ins have been ghosted, and NPS dropped two points. The 12-day support ticket isn't just a support problem — at this stage it becomes the reason they leave. If Marcus is pulling back from internal meetings, the economic buyer may already be disengaging.

Primary Risks:
• 12-day open support ticket creating active frustration
• Login frequency down 40% — 2 ghost users since February
• Missed last 2 monthly check-ins without rescheduling
• NPS dropped from 8 → 6 in latest survey

Stabilizers:
• Core product still in use by 62 of 100 seats
• Renewal is 113 days away — time to course-correct
• No formal cancellation request yet

Next Call Focus:
• Lead with the open support ticket — acknowledge the delay, give a timeline
• Ask about Dana and Tom's inactivity — is there a team change?
• Reframe check-ins as time-saving, not reporting
• Ask directly: "Is there anything we should be doing differently?"

Recommended action: Schedule EBR with Marcus Li this week before the support ticket becomes a decision point.
```

## Analysis JSON

```json
{
  "summary": "TechFlow Inc is showing early-to-mid churn indicators with declining usage, disengagement from check-ins, and an unresolved support ticket.",
  "risk_story": "TechFlow started strong but has gone quiet over the past 30 days. Two users who were previously active have stopped logging in entirely. The open support ticket at 12 days is adding friction at exactly the wrong time — if it's not resolved this week, it becomes the reason they leave.",
  "primary_risks": [
    "12-day open support ticket creating active frustration",
    "Login frequency down 40% — 2 ghost users since February",
    "Missed last 2 monthly check-ins without rescheduling",
    "NPS dropped from 8 to 6 in latest survey"
  ],
  "stabilizers": [
    "Core product still in use by majority of team (62/100 seats)",
    "Renewal is 113 days away — time to course-correct",
    "No formal cancellation request or competitor evaluation confirmed"
  ],
  "next_call_focus": [
    "Lead with the open support ticket — acknowledge the delay, give a concrete timeline",
    "Ask about Dana and Tom's inactivity — is there a team restructure?",
    "Reframe check-ins as time-saving, not reporting",
    "Directly ask: 'Is there anything we should be doing differently?'"
  ],
  "urgency": "high"
}
```
