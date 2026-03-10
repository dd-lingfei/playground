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

## Repo structure

```
em-daily/
├── skills/
│   └── inventory-pod-status/
│       ├── SKILL.md     # Skill instructions for Claude
│       └── MEMORY.md    # Doc IDs, channel IDs, project mappings
└── docs/
    └── superpowers/
        ├── specs/       # Design specs for skills
        └── plans/       # Implementation plans
```

## Setup

Skills in `skills/` are symlinked or copied to `~/.claude/skills/` to be available in Claude Code sessions. See the design spec in `docs/superpowers/specs/` for full details on each skill's data sources and behavior.
