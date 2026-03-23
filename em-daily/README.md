# em-daily

Claude Code skills and tooling for engineering manager daily workflows on the Inventory POD.

## Skills

### `/inventory-pod-status`

Generates a synthesized execution health report for all Inventory POD projects and delivers it as a Slack DM.

**What it does:**
1. Fetches 7 Google Docs (Weather Report, Initiative Review, Huddle Notes, etc.) in parallel
2. Reads 19+ Slack channels (project `#proj--*` channels + team channels) for the last 3 days
3. Classifies each project as 🟢 On Track / 🟡 At Risk / 🔴 Blocked
4. Sends a structured report to Lingfei Li via Slack DM

**Invoke with:** `/inventory-pod-status`

**Projects tracked:**

| Workstream | Projects |
|------------|---------|
| INF-P Model | INF-P v7 Backend, JETS INF-P v2, Mx Pick INF-P |
| Badging | Operator Overrides / Manual Badging, LOOS Badge Iterations v2, Threshold Tuning |
| Platform | PKG Hot Partition, Query by Item ID, USL Adoption, USL Holdout |
| Data / Signals | Just-in-Time Inventory, Zero Ingestion Latency |
| OE / AI | AI Anomaly Detection, INFP EOL Sunset, Inventory Pod AI Ideas |

---

### `/slack-mention-triage`

Reviews unread Slack messages where the user was mentioned and classifies them by urgency.

**What it does:**
1. Fetches unread mentions across all Slack channels
2. Classifies each message into: **Immediate** (respond now) / **Later** (respond today) / **FYI** (no action needed)
3. Delivers a prioritized triage report

**Invoke with:** `/slack-mention-triage`

---

### `/inventory-telescope`

Macro-level inventory monitoring — detects anomalies at the merchant, store, job, and system level.

**What it does:**
- Monitors KPIs and detects anomalies at scale across merchants, stores, and jobs
- Surfaces system health issues and metric regressions
- NOT for root-causing specific items (use `/inventory-microscope` for that)

**Invoke with:** `/inventory-telescope`

---

### `/inventory-microscope`

Root cause analysis for specific inventory items — traces individual items through the full processing pipeline.

**What it does:**
- Queries data lakes (QIF, raw/hydrated feeds) for item-level data
- Cross-references observability logs and Glean for pipeline traces
- Explains exactly what happened to a specific item and why

**Invoke with:** `/inventory-microscope`

---

### `/development-report`

Maintains a running changelog of completed development work.

**What it does:**
- Fetches merged PRs from GitHub for dd-lingfei
- Tracks JIRA task completions (DIGLETT project)
- Accepts manual entries (meetings, design reviews, docs)
- Appends new entries to a persistent date-grouped log

**Invoke with:** `/development-report`

---

### `/copilot-reviewer-pr-lifecycle`

Automates the GitHub Copilot code review loop on a PR.

**What it does:**
- Detects the PR for the current branch
- Requests Copilot review if not already requested
- Polls every 30 seconds for Copilot's review comments
- Auto-fixes all actionable comments, commits, pushes, and re-requests review
- Repeats until Copilot approves or has no more comments

**Invoke with:** `/copilot-reviewer-pr-lifecycle`

---

## Repo structure

```
em-daily/
├── skills/
│   ├── inventory-pod-status/
│   │   ├── SKILL.md     # Skill instructions for Claude
│   │   └── MEMORY.md    # Doc IDs, channel IDs, project mappings
│   └── slack-mention-triage/
│       └── SKILL.md
└── docs/
    └── superpowers/
        ├── specs/       # Design specs for skills
        └── plans/       # Implementation plans
```

Skills under `skills/` are the canonical source. `~/.claude/skills/` contains pointer files that redirect Claude to the canonical location, so slash commands work from any directory.

## Setup

Copy or symlink each skill directory from `skills/` to `~/.claude/skills/`. The pointer pattern means edits to the canonical files are picked up immediately without re-copying.
