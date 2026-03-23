---
name: development-report
description: Development changelog — tracks completed work (merged PRs, JIRA tasks, manual entries) organized by date. Appends new entries since last run.
user_invocable: true
---

# Development Report

A running changelog of completed work. Each invocation fetches new activity since the last run and appends it to MEMORY.md. Tracks only dd-lingfei's work.

## How to Execute

### Step 1: Load state

Read `MEMORY.md` (in the same directory as this SKILL.md) to get:
- `last_run_date` — the date of the most recent run (YYYY-MM-DD format)
- `github_username` — cached GitHub username
- Existing changelog entries (to avoid duplicates)

If `last_run_date` is missing, default to 7 days ago.

### Step 2: Identify GitHub user

If `github_username` is not cached in MEMORY.md:

```bash
gh api user --jq '.login'
```

Cache the result in MEMORY.md.

### Step 3: Fetch recently merged PRs

```bash
gh search prs --author=dd-lingfei --state=closed --merged --sort=updated --limit=50 --json repository,title,number,url,mergedAt
```

Filter results to only include PRs merged **after** `last_run_date`. If `mergedAt` is not available in search results, fetch individual PR details:

```bash
gh pr view <number> --repo <owner/repo> --json title,number,url,mergedAt,headRefName
```

Group the merged PRs by date (using the `mergedAt` date, in the user's local timezone).

### Step 4: Fetch JIRA updates (when Atlassian MCP is available)

Search for DIGLETT subtasks transitioned to Done since the last run:

```
searchJiraIssuesUsingJql: project = DIGLETT AND issuetype = Subtask AND status = Done AND updated >= "last_run_date" ORDER BY updated DESC
```

If Atlassian MCP tools are not available, skip this step and note it in the output.

### Step 5: Accept manual entries

Ask the user:
> Any manual entries to add? (meetings, design reviews, docs, etc.) Enter items or press Enter to skip.

Each manual entry becomes a `- Manual: <description>` line under today's date.

### Step 6: Format changelog entries

Group all entries by date (newest first). Each entry follows this format:

```
## YYYY-MM-DD
- [owner/repo] Merged: PR title ([#N](url)) — DIGLETT-XX
- [owner/repo] Merged: PR title ([#N](url))
- JIRA: DIGLETT-XX marked Done — task summary
- Manual: description
```

Rules:
- If a merged PR title contains a JIRA key (e.g. `[DIGLETT-27]`), append `— DIGLETT-27` to the entry
- If a JIRA task was completed but has no corresponding merged PR in this batch, add a standalone JIRA entry
- Avoid duplicates: skip any PR or JIRA task that already appears in MEMORY.md

### Step 7: Append to MEMORY.md

Prepend the new date sections to the `## Changelog` section of MEMORY.md (newest first, before existing entries). Do NOT remove or modify existing entries.

### Step 8: Present the report

Show the user the new entries that were just added. Format:

```
# Development Report — YYYY-MM-DD

## New entries since last run (YYYY-MM-DD):

## YYYY-MM-DD
- [owner/repo] Merged: PR title ([#N](url)) — DIGLETT-XX
...

---
Total: X merged PRs, Y JIRA completions, Z manual entries
```

If no new activity was found, say so clearly.

### Step 9: Update last_run_date

Update the `last_run_date` field in MEMORY.md to today's date (YYYY-MM-DD).
