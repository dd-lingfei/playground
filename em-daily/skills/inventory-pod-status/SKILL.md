---
name: inventory-pod-status
description: Inventory POD execution status report for the team manager. Fetches Google Docs and Slack channels in parallel, synthesizes project health, and delivers a structured report via Slack DM. Run this when you want a current snapshot of all Inventory POD projects.
user_invocable: true
---

# Inventory POD Status

Produces a manager-facing status report for the Inventory POD. Fetches all data sources in parallel, classifies each project by health signal, and sends the report as a Slack DM to Lingfei Li (U0876VCA5SP).

## Step 1: Load memory

Read `/Users/lingfei.li/AiPlaygroundCode/playground/em-daily/skills/inventory-pod-status/MEMORY.md`. This contains all doc IDs, channel IDs, and the project-to-workstream mapping. Use it throughout — do not look up IDs again.

## Step 2: Auto-detect placeholder channels

For each project listed as `TODO` in MEMORY.md (currently: **Zero Ingestion Latency**), run a Slack channel search:

```
slack_search_channels: "proj--zero latency" OR "proj--ingestion latency" OR "proj--mx data latency"
```

If a matching channel is found with activity in the last 7 days:
- Include it in Step 3 as an additional project channel to read
- Note in the report that it was auto-detected
- Update `/Users/lingfei.li/AiPlaygroundCode/playground/em-daily/skills/inventory-pod-status/MEMORY.md` to record the channel ID so future runs skip the search

## Step 3: Fetch all data sources in parallel

Launch ALL of the following fetches simultaneously — do not wait for one before starting the next.

**Google Docs** — use `get_doc` for each:
- Weather Report (doc ID from MEMORY.md)
- Initiative Review (doc ID from MEMORY.md)
- Inventory Huddle Notes (doc ID from MEMORY.md)
- InventoryML Standup (doc ID from MEMORY.md)
- SIP Leads Weekly (doc ID from MEMORY.md)
- Experiment Tracker (doc ID from MEMORY.md)

Note: The Execution Gantt is a Google Sheet — read what is accessible; if unavailable, skip and note in report.

**Slack channels** — use `slack_read_channel` with `oldest` = 3 days ago for each channel ID in MEMORY.md:
- All project channels (proj--*)
- All team channels

**Private channel** — for `mxpick-inf-p-tiger-team-weekly`: use `slack_search_channels` to find the channel ID by name, then read it. If inaccessible (private and not a member), note it as "inaccessible" in the report.

## Step 4: Build the project inventory

From the **Weather Report** and **Inventory Huddle Notes**, extract the canonical list of active projects. For each project record:
- **Name** (canonical name as used in the docs)
- **DRI** (person responsible, from doc)
- **Doc status** (any status note or ETA mentioned in the doc)
- **Workstream** (map using the Projects by Workstream table in MEMORY.md)

If a project appears in Slack channels but not in any doc, add it to the inventory with DRI = "unknown" and flag it in the report.

## Step 5: Enrich each project with Slack signals

For each project, find relevant Slack messages from Step 3. Match project names and keywords (e.g., "JETS INF-P", "manual badging", "PKG hot partition", "USL holdout") against channel content.

For each project, extract:
- **Latest notable update** (most recent signal worth surfacing)
- **Blockers** — messages containing: blocked, waiting on, can't proceed, dependency, need from, need sync, escalat
- **Experiments** — messages containing: launched, ramped, DV, experiment, rollout, %, treatment
- **Decisions pending** — messages ending in "?", or containing: need alignment, need decision, LGTM?, approve?, should we
- **Asks directed at manager** — messages that @-mention U0876VCA5SP or contain: Lingfei, LL, manager

## Step 6: Classify each project

Assign one status based on the combined doc + Slack signals:

| Status | When to assign |
|--------|---------------|
| 🟢 On Track | No blockers found. Recent signals show forward progress (shipped, ramped, merged, launched, code complete). |
| 🟡 At Risk | A dependency or delay is mentioned but the team is actively working around it. No hard blocker. |
| 🔴 Blocked | An explicit blocker is present, or the project has been silent for 5+ days with an open question unanswered. |

If a project has no signals at all in the last 3 days and is listed as active in docs, mark it 🟡 (stale — no recent signal).

## Step 7: Detect active incidents

Search the fetched Slack data for any `#pev-*` channel names mentioned in messages (they appear as links like `#pev-24435-...`). For each one found:
- Note the channel name
- Extract the one-line topic/description
- Note who is involved (DRI from the channel)

## Step 8: Compose the report

Use this exact format. Keep each project block to 3 lines max. Be terse — the manager reads this on their phone.

```
📊 Inventory POD Status — [Weekday, Month Day]

━━━━━━━━━━━━━━ TL;DR ━━━━━━━━━━━━━━
🔴 [project name]: [one-line blocker or reason]
🟡 [project name]: [one-line risk or stale note]
🟢 [N] projects on track: [name1, name2, ...]
⚠️  Needs your input: [specific ask or decision, if any]

━━━━━━━━━━ PROJECT STATUS ━━━━━━━━━━

*[Workstream: INF-P Model]*

*INF-P v7 Backend* 🟢/🟡/🔴
DRI: [name]  |  [doc ETA if present]
[1-2 sentence status combining doc + latest Slack signal]
Latest: [most recent notable update, ~timestamp]

*JETS INF-P v2* 🟢/🟡/🔴
...

*Mx Pick INF-P* 🟢/🟡/🔴
...

*[Workstream: Badging]*

*Operator Overrides / Manual Badging over PKG* 🟢/🟡/🔴
...

[continue for all workstreams and projects]

━━━━━━━━━━ ACTIVE INCIDENTS ━━━━━━━━━━
[If none: "No active incidents in the last 3 days."]
• #pev-XXXXX: [one-line description] — DRI: [name]

━━━━━━━━━━ ACTION ITEMS FOR YOU ━━━━━━━━━━
[If none: "No immediate action items."]
• [Decision needed / person waiting / risk to escalate]
```

Rules for composing the report:
- List workstreams in this order: INF-P Model → Badging → Platform → Data/Signals → OE/AI
- Within each workstream, list 🔴 first, then 🟡, then 🟢
- TL;DR must list ALL 🔴 and 🟡 projects. For 🟢, consolidate to a single count line.
- Action Items must only contain items that actually require the manager's input — not general status.
- If Zero Ingestion Latency was auto-detected in Step 2, add a note: "📡 Auto-detected new channel: #[name]"

## Step 9: Send the report as a Slack DM

Use `slack_send_message` with:
- `channel_id`: `U0876VCA5SP`
- `message`: the full report text from Step 8

After sending, confirm: "Report sent. [Link to the DM]"
