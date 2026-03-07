---
name: lingfei-feature-development-report
description: Track feature development progress across repos for the current project. Shows PRs, branches, CI status, and action items organized by workstream.
user_invocable: true
---

# Lingfei Feature Development Report

Tracks high-level project goals, groups PRs by workstream, maintains a feature backlog, and flags stale or blocked work.

## How to Execute

### Step 1: Load memory

Read `MEMORY.md` from the repo at `/Users/lingfei.li/AiPlaygroundCode/playground/lingfei-feature-development-report/MEMORY.md`.

This file contains:
- **Workstreams** - the user's high-level project goals and which repos belong to each
- **Previous state** - last known PR statuses, action items, and notes
- **Backlog** - feature ideas organized by workstream with status tracking

IMPORTANT: Workstreams are persistent. NEVER remove a workstream even if it has zero open PRs. Only the user can retire a workstream by explicitly asking.

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

Using the workstream definitions from MEMORY.md, assign each PR to a workstream based on:
1. The repo it belongs to (primary signal)
2. The PR title / branch name (secondary signal for repos shared across workstreams)

If a PR doesn't match any existing workstream, auto-infer a new workstream name and add it. Present the new workstream to the user for confirmation.

### Step 7b: Update backlog statuses

The Backlog section in MEMORY.md tracks feature ideas per workstream. Each item has a status lifecycle:
- `BACKLOG` - idea logged, no PR yet
- `IN PROGRESS` - an open PR matches this item
- `DONE` - a merged PR completed this item

During each report run, auto-maintain the backlog:
1. For each backlog item with status `BACKLOG`, check if any open PR title or branch name matches the feature description. If so, transition to `IN PROGRESS` and link the PR.
2. For each backlog item with status `IN PROGRESS`, check if the linked PR has been merged. If so, transition to `DONE`.
3. If an `IN PROGRESS` item's PR was closed without merging, transition back to `BACKLOG` and remove the PR link.
4. Report any transitions in the Action Items section (e.g. "BL-1 moved to IN PROGRESS via #66163").

IMPORTANT: Matching should be fuzzy - match on keywords from the feature title against PR titles and branch names. When uncertain, flag it for the user to confirm rather than auto-transitioning.

Backlog format in MEMORY.md (under `## Backlog`, with sub-sections per workstream):
```
### <Workstream Name>
| ID | Feature | Status | PR | Notes | Added |
|----|---------|--------|----|-------|-------|
| BL-1 | Feature title | BACKLOG/IN PROGRESS/DONE | - or #N | Optional notes | YYYY-MM-DD |
```

When the user describes a new feature idea outside of a report run:
1. Classify it into the appropriate workstream
2. Present it for user confirmation
3. On confirmation, assign the next available BL-N ID and add it to MEMORY.md
4. Commit via branch + PR (same workflow as report updates)

### Step 7c: Auto-create backlog items for unlinked open PRs

After updating existing backlog statuses in Step 7b, check for open PRs that have no corresponding backlog item. An open PR is "unlinked" if:
1. It is NOT already referenced by any backlog item (neither as an IN PROGRESS link nor as a DONE link)
2. It is NOT a playground report/meta PR (skip PRs in the `dd-lingfei/playground` repo since those are tooling PRs for this report itself)

For each unlinked open PR:
1. Assign the next available BL-N ID (scan all workstreams for the highest existing ID and increment)
2. Derive the feature title from the PR title - clean it up to be a concise feature description (e.g. "Add Diglett session management with store ID entry and photo persistence" -> "Session management with store ID entry and photo persistence")
3. Set status to `IN PROGRESS` and link the PR
4. Set Notes to a brief description derived from the PR title
5. Set Added to today's date
6. Place it under the correct workstream based on the PR's repo (same classification as Step 7)

Report any auto-created backlog items in the Action Items section (e.g. "Auto-created BL-9 for ios#66161 (session management)").

IMPORTANT: This runs automatically during every report run. No user confirmation is needed for auto-created items since the PR already exists as evidence of the work. The user can always rename or reorganize backlog items later.

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

### Backlog
| ID | Feature | Status | PR | Notes | Added |
|----|---------|--------|----|-------|-------|
| BL-N | feature | BACKLOG/IN PROGRESS/DONE | - or [#N](url) | notes | date |
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

### Step 9: Update memory and commit

1. Update `MEMORY.md` at `/Users/lingfei.li/AiPlaygroundCode/playground/lingfei-feature-development-report/MEMORY.md` with:
   - Updated timestamp
   - Current workstream definitions (preserving all existing ones)
   - Current open PR summary per workstream
   - Action items
   - Any new workstreams discovered

2. Update `README.md` at `/Users/lingfei.li/AiPlaygroundCode/playground/lingfei-feature-development-report/README.md` with the full human-readable report. This file should contain the same content presented to the user in Step 8 - the complete rendered report with all workstream sections, PR tables, backlog tables, and action items. A human reader should be able to open this file and immediately understand all project progress and backlog items.

   The README.md should follow this structure:
   ```
   # Feature Development Report
   _Last updated: <date and time description>_

   <Full report from Step 8: all workstream sections with Open PRs, Recently Closed/Merged, and Backlog tables, followed by Action Items>
   ```

   IMPORTANT: Update README.md whenever MEMORY.md is updated - this includes report runs, backlog additions, workstream changes, or any other memory update. They must always stay in sync.

3. Create a branch, commit, push, and open a PR for the updated files:
   ```bash
   cd /Users/lingfei.li/AiPlaygroundCode/playground
   git checkout -b update-dev-report-<date>
   git add lingfei-feature-development-report/MEMORY.md lingfei-feature-development-report/README.md
   git commit -m "Update feature development report - <date>"
   git push -u origin update-dev-report-<date>
   ```

   Then create a PR whose body contains the full feature development report (the same content as README.md). Use a HEREDOC to pass the body:
   ```bash
   gh pr create --title "Update feature development report - <date>" --body "$(cat <<'EOF'
   # Feature Development Report - <date>

   <Paste the full report from Step 8 here, including all workstream sections, tables, and action items>
   EOF
   )"
   ```

   IMPORTANT: Always use a branch and PR. Never push directly to main.
   IMPORTANT: The PR description must contain the full rendered report so the user's PR status is visible directly on the PR.
   IMPORTANT: Always include both MEMORY.md and README.md in the same commit.
