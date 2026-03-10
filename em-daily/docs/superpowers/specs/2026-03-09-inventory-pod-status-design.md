# Inventory POD Status Skill — Design Spec

**Date:** 2026-03-09
**Skill name:** `inventory-pod-status`
**Invoked with:** `/inventory-pod-status`
**Owner:** Lingfei Li (U0876VCA5SP)

---

## Purpose

A Claude skill that gives the Inventory POD manager a single, synthesized view of execution health across all active projects. Run on demand to get a Slack DM with a TL;DR, per-project status, active incidents, and action items requiring manager attention.

---

## Approach

**Document-structured, Slack-enriched.**

Google Docs provide the stable project inventory (what exists, DRIs, timelines). Slack channels (last 3 days) provide freshness signals — blockers raised, experiments launched, decisions pending. Docs give the skeleton; Slack gives the pulse.

---

## Data Sources

### Google Docs (read in parallel, once per run)

| Doc | Doc ID | What to extract |
|-----|--------|----------------|
| Weather Report | `1E_VAu6-YbQNqA7HTTruStNGdNdX4iYmR96aGGEgFcrY` | Active projects, DRIs, status notes, blockers |
| Initiative Review | `18hfe-uZW6GcooEfmSul2eNLHa7ETJOKOPW9GIecmckA` | OKR/metric tracking, workstream updates |
| Execution Gantt | `1eVaKCKMfSp1ButxvS5CYy4xirOCV-oZ6dUrXkoNgcXg` | Project timelines, milestones, completion % |
| Inventory Huddle Notes | `1BrBU1fxogYXVfGM0wvRpbw-z2HBCiJxXLvm42HlavHI` | Recent decisions, action items, discussion topics |
| InventoryML Standup | `171ZgfuP1TpqEBzWiVCo-Ldy5iFYRaHz1MsBDIQB6BhQ` | Upcoming launches, experiment readiness, ML status |
| SIP Leads Weekly | `12062BmDMzV-K0kCoYwIs0uDhauYAL5G2_yVtVGUX_Dc` | Strategic dependencies, risks, cross-team asks |
| Experiment Tracker | `1uGm0uKvY7tja0SvXn5GHwcKjQEnEyqhHYjT3PEGQO_0` | Active experiments, DV status, launch readiness |

### Slack Channels (last 3 days, read in parallel)

#### Project channels
| Channel | Channel ID | Project |
|---------|-----------|---------|
| `#proj--infp-v7-backend` | C09QQDY8VGD | INF-P v7 backend |
| `#proj--jets_infp_v2` | C09V10FSWSE | JETS INF-P v2 |
| `#proj--usl-adoption` | C0AJVGH9VPC | USL Adoption |
| `#proj--usl-holdout` | C0A8QBY0WLV | USL Holdout |
| `#proj--pkg-product-tag-node-hot-partition` | C0ACX5NEPQ9 | PKG Hot Partition |
| `#proj--manual-badging-in-pkg` | C090RQ1GY80 | Operator Overrides / Manual Badging |
| `#proj--mpg-query-by-itemid` | C0AHU9DKBMX | Query by Item ID |
| `#proj-just-in-time-inventory-2026` | C0ADJK34SET | Just-in-Time Inventory |
| `#loos-badge-iterations-v2` | C0ABD058JAD | LOOS Badge Iterations v2 |
| `#mxpick-inf-p-tiger-team-weekly` | *(private — hardcoded by name)* | Mx Pick INF-P |

#### Team channels
| Channel | Channel ID | Purpose |
|---------|-----------|---------|
| `#inventory_pod_leads` | C05K5JX39L3 | Team-wide status, decisions, escalations |
| `#offer-platform-inventory-pod-ai` | C0AK31P26JE | AI/OE initiatives |
| `#nv-inventory-metrics-pod` | C090ASW66V6 | Metrics & KPI alerts |
| `#nv-inventory-core-leads` | C09CG81BHDJ | Core platform decisions |
| `#ask-nv-mx-offer-platform` | C094JK8NCCX | Oncall + cross-team decisions |
| `#nvml-mx-offer-platform-eng` | C07MGNQ9Z96 | ML + Eng cross-team |
| `#nv-inventory-selection-2026-data-source-working-group` | C0A1MMZH18W | Data source dependencies |
| `#nv-inventoryinformed-shopex` | C06FVNYMQS3 | ShopEx cross-team |
| `#eng-nv-inventoryinformed-shopex` | C08H4DY5L4T | ShopEx engineering |

#### Placeholder projects (no channel yet)
| Project | Status | Auto-detect query |
|---------|--------|-------------------|
| Zero Ingestion Latency | TODO: no channel yet | Search `proj--*zero*latency* OR proj--*ingestion*latency*` at runtime; add to report if found |

---

## Execution Steps

### Step 1: Fetch all sources in parallel
Read all 7 Google Docs and all 19+ Slack channels simultaneously. For Slack, fetch the last 3 days of messages per channel.

### Step 2: Auto-detect missing channels (placeholder projects)
For each placeholder project (currently: Zero Ingestion Latency), run a Slack channel search using the auto-detect query. If a matching channel is found with recent activity, include it in the report and note it was auto-detected.

### Step 3: Build project inventory
From the Weather Report and Huddle docs, extract the canonical list of active projects:
- Project name
- DRI
- Current status note (from doc)
- ETA / milestone if present

### Step 4: Enrich with Slack signals
For each project, merge signals from its dedicated `#proj--*` channel (if any) and relevant team channels. Extract:
- Blockers or waiting-on dependencies
- Experiments launched, ramped, or paused
- Decisions made or pending
- Open questions or asks directed at manager
- Any active `#pev-*` incident channels linked to the project

### Step 5: Classify each project
Assign a status based on signal keywords:

| Status | Signals |
|--------|---------|
| 🟢 On Track | shipped, launched, ramped, merged, no blockers |
| 🟡 At Risk | waiting on, dependency, delayed, need alignment, need sync |
| 🔴 Blocked | blocked, cannot proceed, escalation needed, incident |

### Step 6: Compose the report

```
📊 Inventory POD Status — [Day Date]

━━━━━━━━━━━━━━━━ TL;DR ━━━━━━━━━━━━━━━━
🔴 [project]: [one-line blocker]
🟡 [project]: [one-line risk]
🟢 [N] projects on track: [comma-separated names]
⚠️  Needs your input: [specific ask]

━━━━━━━━━━ PROJECT STATUS ━━━━━━━━━━

*[Project Name]* 🟢/🟡/🔴
DRI: [name]
Status: [1-2 sentences combining doc status + latest Slack signal]
Latest: [most recent notable update, with rough timestamp]

[... one block per active project ...]

━━━━━━━━━━ ACTIVE INCIDENTS ━━━━━━━━━━
[List any open #pev-* channels with activity in last 3 days]
• [channel name]: [one-line summary]

━━━━━━━━━━ ACTION ITEMS FOR YOU ━━━━━━━━━━
• [decision needed from manager]
• [person/team waiting on manager response]
• [risk that warrants escalation]
```

### Step 7: Send as Slack DM
Send the composed report as a DM to `U0876VCA5SP` (Lingfei Li) using the Slack MCP tool.

---

## Projects Tracked

| Workstream | Projects |
|-----------|---------|
| INF-P Model | INF-P v7 (reranking, selection-aware), JETS INF-P v2, Mx Pick INF-P |
| Badging | Operator Overrides/Manual Badging over PKG, LOOS Badge Iterations, Threshold Tuning |
| Platform | PKG Hot Partition, Query by Item ID, USL Adoption, USL Holdout |
| Data / Signals | Just-in-Time Inventory, Zero Ingestion Latency *(placeholder)* |
| OE / AI | AI anomaly detection, INFP EOL sunset, DevOps Agent |

---

## Skill Installation

- **File:** `~/.claude/skills/inventory-pod-status/SKILL.md`
- **Invoked with:** `/inventory-pod-status`
- **No arguments** — all sources hardcoded in skill

---

## Out of Scope

- Historical trend tracking (no diff from previous runs)
- Automatic scheduling (user invokes manually)
- Metric/KPI dashboards (use `/inventory-telescope` for that)
