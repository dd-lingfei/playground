---
name: slack-mention-triage
description: Use when you want to review, classify, or send a report of unread Slack messages where the user was mentioned - classifies by urgency into immediate, later, or FYI categories
user_invocable: true
---

# Slack Mention Triage

Searches for recent Slack messages where the user (ID: `U0876VCA5SP`) was mentioned and classifies them by urgency.

## Search Parameters

- **User ID:** `U0876VCA5SP`
- **Lookback window:** Last 3 days (`after:YYYY-MM-DD` using 3 days before today)
- **Channel types:** `public_channel,private_channel,mpim,im` (all channel types)
- **Tool:** `slack_search_public_and_private` with query `<@U0876VCA5SP> after:YYYY-MM-DD`
- For threaded messages, use `slack_read_thread` to get full context before classifying.

---

## Classification Rules

### Need Immediate Response
Apply this label when the message matches any of:
- Contains urgency keywords: "urgent", "asap", "today", "blocking", "blocked", "deadline", "right now", "need you", "live issue"
- Ends with a direct question ("?") addressed to you specifically
- Time-sensitive context: specific launch dates, Mx timelines, oncall issues, production incidents
- You are explicitly the blocker for someone else's work
- Thread is active today and others are waiting on your reply

### Need Response Later
Apply this label when the message matches any of:
- Direct question or request with no explicit deadline or urgency signal
- "WDYT?" or opinion requested without time pressure
- DRI assignment or ownership decision being discussed
- Review or sign-off requested (async, no deadline)
- Follow-up on something you previously said you'd do

### For Information Only
Apply this label when the message matches any of:
- Status updates or announcements where you are cc'd but no action is directed at you
- Bot alerts, automated notifications, monitoring messages
- Threads where others are handling the action and you're tagged for visibility
- Social messages, kudos, casual mentions
- You were mentioned in passing, not as the target of a request

---

## Output

After classifying all messages, send the report as a Slack DM to `U0876VCA5SP` (yourself) using `slack_send_message`. Use the following format:

```
## Slack Mentions Report — [Date Range]

### Need Immediate Response ([count])

**[#channel or DM context] — [Sender Name]**
[1–2 sentence summary of message + why it's urgent]
[Link] | [Timestamp]

### Need Response Later ([count])

...

### For Information Only ([count])

...

---
**Summary:** [X] immediate · [Y] respond later · [Z] FYI only
```

Return the sent message link to the user after delivery.

---

## Customization Notes

To add or adjust classification rules, edit this file under the relevant section in **Classification Rules** above. Rules are applied top-down; the first matching category wins.

---

## Scheduled Delivery

To send this report as a Slack DM to yourself (`U0876VCA5SP`) hourly during a session, use `CronCreate` with:
- **Cron:** `*/60 * * * *` (or pick an off-minute like `7 * * * *`)
- **Prompt:** "Run /slack-mention-triage and send the formatted report as a Slack DM to U0876VCA5SP"

Note: `CronCreate` jobs are session-scoped — they expire when the Claude session ends.
For a persistent scheduled job, use a system cron or launchd to invoke Claude CLI with this skill.
