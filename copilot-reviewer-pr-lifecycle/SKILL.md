---
name: copilot-reviewer-pr-lifecycle
description: Request Copilot review on a PR, monitor for comments, auto-fix them, and re-request review until clean.
user_invocable: true
---

# Copilot Reviewer PR Lifecycle

Automates the Copilot code review loop: request review, wait for comments, fix critical ones (bugs), dismiss minor ones, push, re-request, repeat until Copilot is satisfied.

## How to Execute

### Step 1: Detect PR

Get the PR for the current branch:

```bash
gh pr view --json number,url,headRefName,reviews,reviewRequests
```

If no PR exists for the current branch, tell the user and stop.

Save the PR number and repo for use in subsequent steps.

### Step 2: Check if Copilot review is already requested or in progress

Inspect the `reviewRequests` and `reviews` fields from Step 1.

- Copilot's reviewer login is `copilot-pull-request-reviewer` (a bot account).
- If Copilot has already been requested but hasn't reviewed yet, skip to Step 4 (polling).
- If Copilot has already left a review, skip to Step 5 (check comments).
- Otherwise, proceed to Step 3.

### Step 3: Request Copilot review

```bash
gh pr edit <PR_NUMBER> --add-reviewer copilot-pull-request-reviewer
```

If this fails (e.g., Copilot reviewer not available on the repo), tell the user and stop.

### Step 4: Poll for Copilot review

Set up a CronCreate job that polls every 30 seconds for Copilot's review:

**Cron schedule:** `* * * * *` (fires every minute; the scheduler adds jitter, but this is the fastest cron granularity)

**Poll prompt:**

> You are monitoring PR #<NUMBER> for Copilot review comments. Run this check:
>
> ```bash
> gh api repos/<OWNER>/<REPO>/pulls/<NUMBER>/reviews --jq '[.[] | select(.user.login == "copilot-pull-request-reviewer" or .user.login == "github-actions[bot]")] | last'
> ```
>
> If the result is empty or null, Copilot hasn't reviewed yet. Do nothing — wait for the next poll.
>
> If a review exists, check its state:
> - If `state` is `APPROVED` or the body indicates no issues found: delete this cron job, and tell the user "Copilot approved the PR with no comments."
> - If `state` is `COMMENTED` or `CHANGES_REQUESTED`: proceed to fetch and fix comments. Delete this cron job first, then follow Steps 5-8 below.
>
> **Step 5: Fetch Copilot comments**
>
> Fetch all review comments from Copilot:
>
> ```bash
> gh api repos/<OWNER>/<REPO>/pulls/<NUMBER>/comments --jq '[.[] | select(.user.login == "copilot-pull-request-reviewer" or .user.login == "github-actions[bot]")] | .[] | {id: .id, path: .path, line: .line, side: .side, body: .body, diff_hunk: .diff_hunk}'
> ```
>
> Also fetch the review body itself (the top-level review summary) from the review object obtained above.
>
> If there are no actionable comments (only praise or informational notes), delete the cron job and tell the user "Copilot review complete — no actionable comments."
>
> **Step 6: Triage and fix comments**
>
> For each Copilot comment, first classify it:
>
> **Critical (fix these):** Bugs, logic errors, security vulnerabilities, null/undefined access, race conditions, resource leaks, incorrect behavior, missing error handling that would cause crashes.
>
> **Minor (dismiss these):** Code style suggestions, naming conventions, refactoring proposals, performance micro-optimizations, documentation improvements, alternative approaches that aren't buggy.
>
> For each **critical** comment:
> 1. Read the file at the specified `path`
> 2. Understand the comment in context of the `diff_hunk`
> 3. Make the fix using the Edit tool
>
> For each **minor** comment:
> 1. Reply to the comment on the PR with: "Minor comments are ignored by Claude Code rule"
>    ```bash
>    gh api repos/<OWNER>/<REPO>/pulls/<NUMBER>/comments/<COMMENT_ID>/replies -f body="Minor comments are ignored by Claude Code rule"
>    ```
> 2. Do NOT make any code changes for this comment
>
> If a comment is unclear or not actionable (e.g., a question rather than a suggestion), skip it and note it in the summary.
>
> **Step 7: Commit, push, and re-request review**
>
> ```bash
> git add -A
> git commit -m "Address Copilot review comments"
> git push
> ```
>
> Then re-request Copilot review:
>
> ```bash
> gh pr edit <PR_NUMBER> --add-reviewer copilot-pull-request-reviewer
> ```
>
> Tell the user what was fixed and that review has been re-requested.
>
> **Step 8: Resume polling**
>
> Set up a new CronCreate job with the same poll prompt to wait for Copilot's next review. This continues the loop.

IMPORTANT: The poll prompt must be self-contained — it includes Steps 5-8 so the cron-triggered execution has all the instructions it needs to complete the full cycle.

### Error handling

- If `gh pr edit --add-reviewer` fails, it may mean Copilot isn't enabled on the repo. Tell the user and stop.
- If the gh API calls fail (rate limiting, network), log the error and retry on the next poll cycle.
- If a file referenced in a Copilot comment no longer exists or the line doesn't match, skip that comment and note it.

### Completion

The skill completes when:
- Copilot approves or leaves no actionable comments
- The gh API returns an error that prevents further progress (tell the user)

On completion, delete any active cron jobs and present a summary:
```
# Copilot Review Complete

PR: #<NUMBER> (<URL>)
Rounds: <N>
Critical comments fixed: <M>
Minor comments dismissed: <J>
Skipped: <K> (with reasons)
Status: Approved / No more comments / Error
```
