# Inventory POD Status Skill Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `/inventory-pod-status` Claude skill that fetches Google Docs and Slack channels in parallel, synthesizes a manager-facing status report, and delivers it as a Slack DM.

**Architecture:** A single SKILL.md instructs Claude to fetch all data sources in parallel, classify each project by status signals (🟢/🟡/🔴), compose a structured report, and DM it to the manager. A MEMORY.md alongside stores channel IDs, doc IDs, and last-run metadata so the skill doesn't need to re-discover them on every run.

**Tech Stack:** Claude skill (SKILL.md), Slack MCP (`slack_read_channel`, `slack_send_message`, `slack_search_channels`), Google Docs MCP (`get_doc`)

---

## Chunk 1: Skill scaffolding and data fetch

### Task 1: Create skill directory and MEMORY.md

**Files:**
- Create: `~/.claude/skills/inventory-pod-status/MEMORY.md`

This file stores all hardcoded IDs so the SKILL.md stays readable and IDs live in one place.

- [ ] **Step 1: Create the skill directory**

```bash
mkdir -p ~/.claude/skills/inventory-pod-status
```

- [ ] **Step 2: Create MEMORY.md with all data source IDs**

Create `~/.claude/skills/inventory-pod-status/MEMORY.md` with this exact content:

```markdown
# Inventory POD Status — Memory

## Manager
- Slack user ID: U0876VCA5SP (Lingfei Li)

## Google Doc IDs
- Weather Report: 1E_VAu6-YbQNqA7HTTruStNGdNdX4iYmR96aGGEgFcrY
- Initiative Review: 18hfe-uZW6GcooEfmSul2eNLHa7ETJOKOPW9GIecmckA
- Execution Gantt: 1eVaKCKMfSp1ButxvS5CYy4xirOCV-oZ6dUrXkoNgcXg
- Inventory Huddle Notes: 1BrBU1fxogYXVfGM0wvRpbw-z2HBCiJxXLvm42HlavHI
- InventoryML Standup: 171ZgfuP1TpqEBzWiVCo-Ldy5iFYRaHz1MsBDIQB6BhQ
- SIP Leads Weekly: 12062BmDMzV-K0kCoYwIs0uDhauYAL5G2_yVtVGUX_Dc
- Experiment Tracker: 1uGm0uKvY7tja0SvXn5GHwcKjQEnEyqhHYjT3PEGQO_0

## Slack Channel IDs — Project Channels
- proj--infp-v7-backend: C09QQDY8VGD
- proj--jets_infp_v2: C09V10FSWSE
- proj--usl-adoption: C0AJVGH9VPC
- proj--usl-holdout: C0A8QBY0WLV
- proj--pkg-product-tag-node-hot-partition: C0ACX5NEPQ9
- proj--manual-badging-in-pkg: C090RQ1GY80
- proj--mpg-query-by-itemid: C0AHU9DKBMX
- proj-just-in-time-inventory-2026: C0ADJK34SET
- loos-badge-iterations-v2: C0ABD058JAD
- mxpick-inf-p-tiger-team-weekly: (private — look up by name at runtime)

## Slack Channel IDs — Team Channels
- inventory_pod_leads: C05K5JX39L3
- offer-platform-inventory-pod-ai: C0AK31P26JE
- nv-inventory-metrics-pod: C090ASW66V6
- nv-inventory-core-leads: C09CG81BHDJ
- ask-nv-mx-offer-platform: C094JK8NCCX
- nvml-mx-offer-platform-eng: C07MGNQ9Z96
- nv-inventory-selection-2026-data-source-working-group: C0A1MMZH18W
- nv-inventoryinformed-shopex: C06FVNYMQS3
- eng-nv-inventoryinformed-shopex: C08H4DY5L4T

## Placeholder Projects (no channel yet)
- Zero Ingestion Latency: TODO — auto-detect at runtime by searching for channels matching
  `proj--*zero*latency*` or `proj--*ingestion*latency*` or `proj--*mx*data*latency*`
  If found, read it and include in the report. Update this file with the channel ID.

## Projects by Workstream
### INF-P Model
- INF-P v7 Backend (reranking + selection-aware)
- JETS INF-P v2
- Mx Pick INF-P

### Badging
- Operator Overrides / Manual Badging over PKG
- LOOS Badge Iterations v2
- Badging Threshold Tuning

### Platform
- PKG Hot Partition
- Query by Item ID
- USL Adoption
- USL Holdout

### Data / Signals
- Just-in-Time Inventory
- Zero Ingestion Latency (placeholder)

### OE / AI
- AI Anomaly Detection / DevOps Agent
- INFP EOL Sunset
- Inventory Pod AI Ideas
```

- [ ] **Step 3: Verify the file was created**

```bash
cat ~/.claude/skills/inventory-pod-status/MEMORY.md
```

Expected: File contents printed with all IDs present.

- [ ] **Step 4: Commit**

```bash
cd /Users/lingfei.li/AiPlaygroundCode/playground
git add em-daily/
git commit -m "feat: scaffold inventory-pod-status skill directory and MEMORY.md"
```

---

### Task 2: Create the SKILL.md

**Files:**
- Create: `~/.claude/skills/inventory-pod-status/SKILL.md`

This is the core skill file. It is a Claude prompt — write it as clear, imperative instructions. Every step must be explicit so an agent executing it makes no decisions on its own.

- [ ] **Step 1: Create SKILL.md**

Create `~/.claude/skills/inventory-pod-status/SKILL.md` with the following content:

````markdown
---
name: inventory-pod-status
description: Inventory POD execution status report for the team manager. Fetches Google Docs and Slack channels in parallel, synthesizes project health, and delivers a structured report via Slack DM. Run this when you want a current snapshot of all Inventory POD projects.
user_invocable: true
---

# Inventory POD Status

Produces a manager-facing status report for the Inventory POD. Fetches all data sources in parallel, classifies each project by health signal, and sends the report as a Slack DM to Lingfei Li (U0876VCA5SP).

## Step 1: Load memory

Read `~/.claude/skills/inventory-pod-status/MEMORY.md`. This contains all doc IDs, channel IDs, and the project-to-workstream mapping. Use it throughout — do not look up IDs again.

## Step 2: Auto-detect placeholder channels

For each project listed as `TODO` in MEMORY.md (currently: **Zero Ingestion Latency**), run a Slack channel search:

```
slack_search_channels: "proj--zero latency" OR "proj--ingestion latency" OR "proj--mx data latency"
```

If a matching channel is found with activity in the last 7 days:
- Include it in Step 3 as an additional project channel to read
- Note in the report that it was auto-detected
- Update MEMORY.md to record the channel ID so future runs skip the search

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
````

- [ ] **Step 2: Verify the file exists and has the correct frontmatter**

```bash
head -5 ~/.claude/skills/inventory-pod-status/SKILL.md
```

Expected output:
```
---
name: inventory-pod-status
description: Inventory POD execution status report...
user_invocable: true
---
```

- [ ] **Step 3: Commit**

```bash
cd /Users/lingfei.li/AiPlaygroundCode/playground
git add -A
git commit -m "feat: add inventory-pod-status SKILL.md"
```

---

## Chunk 2: Smoke test and refinement

### Task 3: Run the skill for the first time

**Files:**
- Read: `~/.claude/skills/inventory-pod-status/SKILL.md`
- Read: `~/.claude/skills/inventory-pod-status/MEMORY.md`

- [ ] **Step 1: Invoke the skill**

In a Claude Code session in any directory, run:

```
/inventory-pod-status
```

- [ ] **Step 2: Verify Step 1–3 execute correctly**

Confirm Claude:
- Reads MEMORY.md before starting
- Runs `slack_search_channels` for Zero Ingestion Latency
- Launches all Google Doc + Slack fetches simultaneously (not sequentially)

If Claude fetches sources one-by-one instead of in parallel, edit SKILL.md Step 3 to add: "IMPORTANT: Use a single tool-call block with all fetches listed. Do not await any result before issuing the next fetch."

- [ ] **Step 3: Verify the report structure**

The Slack DM should arrive with:
- A TL;DR section with at least one emoji bullet
- At least 3 project blocks with DRI and status
- A workstream header (e.g., `*[Workstream: INF-P Model]*`)
- An Action Items section (even if empty)

If the report is missing sections, add explicit format enforcement to Step 8 of SKILL.md:
"Every section heading in the format above is mandatory. If you have no data for a section, write 'No data available.' — never omit the section."

- [ ] **Step 4: Verify the private channel handling**

Confirm the report either:
- Includes Mx Pick INF-P data (if the private channel was accessible), or
- Notes "mxpick-inf-p-tiger-team-weekly: inaccessible" in the report

- [ ] **Step 5: Commit any SKILL.md edits made during testing**

```bash
cd /Users/lingfei.li/AiPlaygroundCode/playground
git add -A
git commit -m "fix: refine inventory-pod-status skill after smoke test"
```

---

### Task 4: Final install verification

- [ ] **Step 1: Confirm skill appears in available skills list**

In a fresh Claude Code session, verify `/inventory-pod-status` appears as an available slash command.

- [ ] **Step 2: Confirm MEMORY.md was updated if Zero Ingestion Latency channel was found**

```bash
grep -i "zero\|latency" ~/.claude/skills/inventory-pod-status/MEMORY.md
```

If the auto-detection found a channel, its ID should now be recorded here (no longer `TODO`).

- [ ] **Step 3: Final commit with any remaining changes**

```bash
cd /Users/lingfei.li/AiPlaygroundCode/playground
git add -A
git commit -m "feat: inventory-pod-status skill complete"
```
