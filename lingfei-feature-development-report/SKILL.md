---
name: lingfei-feature-development-report
description: Track feature development progress across repos for the current project. Shows PRs, branches, CI status, and action items organized by workstream.
user_invocable: true
---

# Lingfei Feature Development Report

Tracks high-level project goals, groups PRs by workstream, and flags stale or blocked work. Backlog and status tracking is managed in JIRA (DIGLETT project).

## How to Execute

### Step 1: Load workstream config from JIRA

Fetch the DIGLETT Epic (DIGLETT-1) from JIRA (cloudId: `doordash.atlassian.net`). The Epic's description contains the workstream definitions — each workstream's name, goal, and which repos belong to it.

IMPORTANT: Workstreams are persistent. NEVER remove a workstream even if it has zero open PRs. Only the user can retire a workstream by explicitly asking.

If a new workstream is discovered (a PR doesn't match any existing workstream), present it to the user for confirmation, then add it to the DIGLETT-1 Epic description.

### Step 2: Identify the GitHub user

```bash
gh api user --jq '.login'
```

### Step 3: Fetch open PRs

```bash
gh search prs --author=<username> --state=open --limit=30 --json repository,title,number,state,createdAt,updatedAt,url
```

### Step 4: Fetch recent closed/merged PRs

```bash
gh search prs --author=<username> --state=closed --limit=20 --json repository,title,number,state,createdAt,updatedAt,url --sort=updated
```

### Step 5: Get detailed status for each open PR

For each open PR, fetch detailed info:

```bash
gh pr view <number> --repo <owner/repo> --json title,state,statusCheckRollup,mergeable,reviewDecision,isDraft,additions,deletions,changedFiles,url,number,createdAt,updatedAt,headRefName
```

### Step 6: Compute overall CI status per PR

For each PR, look at `statusCheckRollup`:
- If any check has `state: "FAILURE"` or `conclusion: "FAILURE"` or `state: "ERROR"` -> CI: FAILING
- If any check has `state: "PENDING"` or `status: "IN_PROGRESS"` (and none failing) -> CI: PENDING
- If all checks are `SUCCESS`/`COMPLETED` with `conclusion: "SUCCESS"` -> CI: PASSING

### Step 7: Classify PRs into workstreams

Using the workstream definitions loaded from JIRA in Step 1, assign each PR to a workstream based on:
1. The repo it belongs to (primary signal)
2. The PR title / branch name (secondary signal for repos shared across workstreams)

If a PR doesn't match any existing workstream, auto-infer a new workstream name and add it. Present the new workstream to the user for confirmation.

### Step 8: Present the report

For each workstream, present in this format:

```
## <Workstream Name>
**Goal:** <one-line goal from memory>
**Repos:** repo1, repo2
**Status:** ACTIVE / STALE (no open PRs) / BLOCKED (failing CI or review issues)

### Open PRs
| # | Repo | Title | CI | Review | Mergeable | +/- | Updated |
|---|------|-------|----|--------|-----------|-----|---------|
| [#N](url) | repo | title | PASSING/FAILING/PENDING | APPROVED/CHANGES_REQUESTED/PENDING | YES/NO | +X/-Y | relative time |

### Recently Closed/Merged
| # | Repo | Title | State | Updated |
|---|------|-------|-------|---------|
| [#N](url) | repo | title | MERGED/CLOSED | relative time |
```

If a workstream has NO open PRs, still show it with an empty table and mark status as STALE:
```
## <Workstream Name>
**Goal:** <goal>
**Repos:** repo1, repo2
**Status:** STALE - no open PRs since <last PR date>

_No open PRs. Last activity: [#N](url) <title> (MERGED <date>)_
```

After all workstreams, show a summary:
```
## Action Items
- Bullet list of things needing attention (failing CI, ready to merge, stale workstreams, etc.)
```

### Step 9: Save report to JIRA

Post the full report from Step 8 as a comment on DIGLETT-1 (the Epic) using the `addCommentToJiraIssue` Atlassian MCP tool (cloudId: `doordash.atlassian.net`, issueIdOrKey: `DIGLETT-1`).

The comment body should be the full rendered report — all workstream sections, PR tables, and action items — so it's visible directly on the Epic in JIRA.

If any new workstreams were discovered in Step 7, update the DIGLETT-1 Epic description to include the new workstream definition.
