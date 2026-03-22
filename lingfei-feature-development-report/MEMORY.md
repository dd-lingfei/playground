# Local Memory - dd-lingfei Feature Development Report

## Last Updated
2026-03-22 (evening run)

## GitHub Profile
- **Username:** dd-lingfei

## Workstreams

### Diglett iOS App
- **Goal:** Build the Diglett iOS app - photo capture, session management, store ID entry, and item comparison views
- **Repos:** doordash/ios
- **Last Active:** 2026-03-22

### Diglett Backend
- **Goal:** Build the Diglett backend - Pedregal graph scaffolding, infra, Vault, GenAI, Snowflake, S3, and Taulu integrations
- **Repos:** doordash/pedregal, doordash/tf_account_dash_management
- **Last Active:** 2026-03-09

### Developer Workflow (Playground)
- **Goal:** Improve personal developer workflow with skills, PR tracking, and automation tooling
- **Repos:** dd-lingfei/playground
- **Last Active:** 2026-03-22

### Inventory Skills
- **Goal:** Build and maintain inventory investigation skills (telescope, microscope, weather-report)
- **Repos:** doordash/inventory-skills
- **Last Active:** 2026-02-27

## Open PR Summary (as of 2026-03-22 evening)

### Diglett iOS App
- **doordash/ios#68925** - [DIGLETT-27] Allow user to upload photos from photo library - CI PENDING (Bitrise running), REVIEW_REQUIRED, +86/-8, 3 files
- **doordash/ios#68837** - [DIGLETT-11] Diglett upload-only: capture, barcode detect, and upload photos - CI PASSING (all green), REVIEW_REQUIRED, +187/-204, 7 files
- **doordash/ios#66259** - Invoke Diglett gRPC backend for photo processing - CI FAILING (Bitrise), APPROVED, +2018/-111, 11 files
- **doordash/ios#66269** - [DIGLETT-11] Persist match results to disk and fix image upload - CI FAILING, no review, +119/-30, 4 files (stale 13 days)
- **doordash/ios#66266** - [DIGLETT-11] Allow deleting pending photos from capture queue - CI PENDING (pullapprove only), no review, +165/-53, 6 files (stale 13 days)

### Diglett Backend
- No open PRs

### Developer Workflow (Playground)
- No open PRs

### Inventory Skills
- No open PRs

## Action Items
- PR #66259 (ios) gRPC backend is APPROVED but CI FAILING - fix Bitrise failure to unblock merge
- PR #68837 (ios) upload-only is all CI PASSING - needs code review
- PR #68925 (ios) photo library import CI still running - wait then request review
- PR #66269 (ios) persist results is FAILING and 13 days stale - fix or close
- PR #66266 (ios) delete pending photos is 13 days stale - request review or close
- Diglett Backend workstream has no open PRs - check if previous PRs merged
- Inventory Skills workstream STALE since Feb 27

## JIRA Integration Notes
- Skill was updated to use JIRA (DIGLETT project, Epic DIGLETT-1) as source of truth
- Atlassian MCP tools not available in this session - JIRA sync skipped
- JIRA tasks referenced in PR titles: DIGLETT-11, DIGLETT-27

## Skill Location
- Skill installed at: `~/.claude/skills/lingfei-feature-development-report/SKILL.md`
- Invoke with: `/lingfei-feature-development-report`
