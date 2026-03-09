---
name: lingfei-feature-development-report
description: Track feature development progress across repos for the current project. Shows JIRA tasks with linked PRs and CI status, organized by workstream.
user_invocable: true
---

# Lingfei Feature Development Report

Tracks high-level project goals and JIRA task progress per workstream. PRs are linked inline to their corresponding JIRA tasks. Status and backlog live in JIRA (DIGLETT project).

## How to Execute

### Step 1: Load workstream config from JIRA

Fetch the DIGLETT Epic (DIGLETT-1) from JIRA (cloudId: `doordash.atlassian.net`). The Epic's description contains the workstream definitions — each workstream's name, goal, and which repos belong to it.

IMPORTANT: Workstreams are persistent. NEVER remove a workstream even if it has zero open PRs. Only the user can retire a workstream by explicitly asking.

If a new workstream is discovered (a PR doesn't match any existing workstream), present it to the user for confirmation, then add it to the DIGLETT-1 Epic description.

### Step 2: Fetch JIRA tasks per workstream

For each workstream that has a corresponding JIRA Task (e.g. DIGLETT-2 for iOS, DIGLETT-3 for Backend), fetch all its subtasks:

```
searchJiraIssuesUsingJql: project = DIGLETT AND issuetype = Subtask ORDER BY created ASC
```

Group subtasks by their parent Task (DIGLETT-2 → Diglett iOS App, DIGLETT-3 → Diglett Backend).

### Step 3: Identify the GitHub user

```bash
gh api user --jq '.login'
```

### Step 4: Fetch open PRs

```bash
gh search prs --author=<username> --state=open --limit=30 --json repository,title,number,state,createdAt,updatedAt,url
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

### Step 7: Match PRs to JIRA tasks

For each open PR, attempt to match it to a JIRA subtask using:
1. Explicit PR links in the JIRA task description (primary signal)
2. Fuzzy keyword match between PR title/branch and JIRA task summary (secondary signal)

A PR is **unlinked** if it cannot be confidently matched to any JIRA task. Keep a list of unlinked PRs — they get their own table at the bottom of the report.

PRs in the `dd-lingfei/playground` repo are always unlinked (they are tooling/meta PRs for this report itself).

### Step 8: Sync JIRA task statuses

After matching PRs to tasks, update JIRA statuses to reflect current development state. Use `transitionJiraIssue` (cloudId: `doordash.atlassian.net`).

**DIGLETT transition IDs:** `"11"` = To Do, `"21"` = In Progress, `"31"` = Done

**Safety rules:**
- Never downgrade a task from "Done"
- Never automatically transition to Done — always ask the user first
- Skip tasks already in the correct target status

For each JIRA subtask, apply the following rules:

#### Rule A — Open PR found → In Progress
If a task has a matched open PR (from Step 7) **and** its current status is **"To Do"**:
→ Immediately transition to **In Progress** (transitionId: `"21"`). No confirmation needed.

#### Rule B — No open PR → check description for PR links
For tasks with no matched open PR, look for GitHub PR links in the JIRA task description.

**B1 — PR links found in description**: fetch the state of each linked PR in parallel:
```bash
gh pr view <number> --repo <owner/repo> --json state,mergedAt
```
- If any linked PR is still **OPEN** → treat as Rule A (transition To Do → In Progress if needed)
- If **all linked PRs are MERGED** → add task to "done candidates" list
- If all linked PRs are **CLOSED (not merged)** → treat as B2

**B2 — No PR links anywhere** and current status is **"In Progress"**:
→ Immediately transition to **To Do** (transitionId: `"11"`). No confirmation needed.
If status is already "To Do" → no change.

#### Rule C — Done candidates → ask user
After processing all tasks, if any tasks have all linked PRs merged, ask the user in one prompt:

```
The following tasks have all linked PRs merged. Mark as Done in JIRA?
- [DIGLETT-X](url): <title>  (merged: PR #N)
- [DIGLETT-Y](url): <title>  (merged: PR #N, #M)

Reply "yes" to mark all, "no" to skip, or list specific keys (e.g. "DIGLETT-X").
```

For confirmed tasks, transition to **Done** (transitionId: `"31"`).

---

### Step 9: Present the report

For each workstream that has JIRA tasks, present in this format:

```
## <Workstream Name>
**Goal:** <one-line goal>
**Repos:** repo1, repo2
**Status:** ACTIVE / STALE / BLOCKED

### Tasks
| JIRA | Title | Status | PR | CI | Review |
|------|-------|--------|----|----|--------|
| [DIGLETT-N](url) | task title | To Do / In Progress / Done | [#N](url) or - | PASSING/FAILING/PENDING or - | APPROVED/PENDING or - |
```

- Show ALL tasks for the workstream regardless of JIRA status (To Do, In Progress, Done)
- If a task has a matched open PR, populate the PR, CI, and Review columns
- If no open PR is matched, show `-` for PR/CI/Review

For workstreams with NO JIRA tasks (e.g. Developer Workflow, Inventory Skills), show:
```
## <Workstream Name>
**Goal:** <goal>
**Repos:** repo1, repo2
**Status:** ACTIVE / STALE
```
(Their PRs will appear in the Unlinked PRs table at the bottom if any exist.)

After all workstreams, show unlinked PRs (if any):
```
## Unlinked PRs
_PRs that could not be matched to a JIRA task_
| # | Repo | Title | CI | Review | +/- | Updated |
|---|------|-------|----|--------|-----|---------|
| [#N](url) | repo | title | PASSING/FAILING/PENDING | APPROVED/PENDING | +X/-Y | relative time |
```

Then show the action items summary:
```
## Action Items
- Bullet list of things needing attention (failing CI, ready to merge, blocked tasks, stale workstreams, etc.)
```

### Step 10: Save report to JIRA

Post the full report from Step 9 as a comment on DIGLETT-1 (the Epic) using the `addCommentToJiraIssue` Atlassian MCP tool (cloudId: `doordash.atlassian.net`, issueIdOrKey: `DIGLETT-1`).

The comment body should be the full rendered report so it's visible directly on the Epic in JIRA.

If any new workstreams were discovered in Step 7, update the DIGLETT-1 Epic description to include the new workstream definition.
