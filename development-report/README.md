# Development Report

A Claude Code skill that maintains a running changelog of completed development work. Each invocation fetches new activity since the last run and appends it to a persistent log.

## What it tracks

- **Merged PRs** — fetched from GitHub for `dd-lingfei` across all tracked repos
- **JIRA completions** — DIGLETT subtasks transitioned to Done (when Atlassian MCP is available)
- **Manual entries** — meetings, design reviews, docs, and other work not captured by PRs or JIRA

## Output format

Entries are grouped by date, newest first:

```
## 2026-03-22
- [doordash/ios] Merged: Upload photos from photo library (#68925) — DIGLETT-27
- [doordash/pedregal] Merged: Add S3 cache layer (#105244) — DIGLETT-15
- Manual: Reviewed design spec for barcode detection v2

## 2026-03-21
- [doordash/ios] Merged: Diglett upload-only flow (#68837) — DIGLETT-11
```

## Invoke

```
/development-report
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill instructions for Claude |
| `MEMORY.md` | Persistent changelog and metadata (last_run_date, workstreams) |
