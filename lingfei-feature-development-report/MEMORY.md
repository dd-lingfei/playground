# Local Memory - dd-lingfei Feature Development Report

## Last Updated
2026-03-07 (sample PR run)

## GitHub Profile
- **Username:** dd-lingfei

## Workstreams

### Diglett iOS App
- **Goal:** Build the Diglett iOS app - photo capture, session management, store ID entry, and item comparison views
- **Repos:** doordash/ios
- **Last Active:** 2026-03-07

### Diglett Backend
- **Goal:** Build the Diglett backend - Pedregal graph scaffolding, infra, Vault, GenAI, Snowflake, S3, and Taulu integrations
- **Repos:** doordash/pedregal, doordash/tf_account_dash_management
- **Last Active:** 2026-03-07

### Developer Workflow (Playground)
- **Goal:** Improve personal developer workflow with skills, PR tracking, and automation tooling
- **Repos:** dd-lingfei/playground
- **Last Active:** 2026-03-07

### Inventory Skills
- **Goal:** Build and maintain inventory investigation skills (telescope, microscope, weather-report)
- **Repos:** doordash/inventory-skills
- **Last Active:** 2026-02-27

## Open PR Summary (as of 2026-03-07 late evening)

### Diglett iOS App
- **doordash/ios#66162** - Sequential photo IDs - CI passing (pullapprove pending), no review yet, +13/-1
- **doordash/ios#66161** - Session management + store ID entry - CI passing (pullapprove pending), no review yet, +374/-52

### Diglett Backend
- **doordash/pedregal#105075** - Diglett graph scaffold v2 - CI PENDING (buildkite running), review required, +850/-0, 23 files
- **doordash/tf_account_dash_management#2039** - Vault registration for diglett staging - CI all green, APPROVED, ready to merge, +16/-0

### Developer Workflow (Playground)
- No open PRs

### Inventory Skills
- No open PRs

## Action Items
- PR #2039 (tf_account_dash_management) is approved and all checks passing - MERGE NOW
- PR #105075 (pedregal) has buildkite CI still running - monitor for completion (v1 PR #105035 failed CI previously)
- PRs #66161 and #66162 (ios) need code review - pullapprove pending, all other CI checks passing
- Developer Workflow workstream is STALE - last activity was playground#2 (merged 2026-03-07)
- Inventory Skills workstream is STALE - last activity was 2026-02-27

## Recently Closed/Merged PRs
- **dd-lingfei/playground#2** - Rename feature-development to lingfei-feature-development-report - MERGED
- **dd-lingfei/playground#1** - Add PR tracker memory - MERGED
- **doordash/pedregal#105035** - Diglett graph scaffold v1 - CLOSED (not merged, CI failed)
- **doordash/ios#66158** - Photo upload flow - MERGED
- **doordash/ios#65950** - Item detail comparison view - MERGED
- **doordash/ios#65948** - Simulator sample images - MERGED
- **doordash/ios#65946** - Diglett photo capture tool - MERGED
- **doordash/inventory-skills#35** - Restore MCP server config docs - MERGED
- **doordash/inventory-skills#34** - Remove Snowflake skill and MCP server config - MERGED
- **doordash/inventory-skills#33** - Add bias-for-action philosophy - MERGED
- **doordash/inventory-skills#32** - Add AI-first authorship policy - MERGED
- **doordash/inventory-skills#30** - Update AGENT.md for telescope/microscope - MERGED

## Backlog

### Diglett iOS App
| ID | Feature | Status | PR | Notes | Added |
|----|---------|--------|----|-------|-------|
| BL-1 | Barcode detection for photo quality validation | BACKLOG | - | Auto-detect barcodes in captured photo. 1 barcode = green confirm. 0 or 2+ barcodes = show warning + change button to "Still Confirm" | 2026-03-07 |
| BL-3 | Trigger backend processing after photo upload + poll for status | BACKLOG | - | After successful upload, call Diglett backend to start processing job. Poll status endpoint until complete. On success: log response to debug console + update row text to "Processing completed." | 2026-03-07 |
| BL-4 | Use local backend endpoint in simulator | BACKLOG | - | When running in simulator, hit local Diglett backend instead of pedregal endpoint | 2026-03-07 |
| BL-5 | Delete photos from list view | BACKLOG | - | Allow user to delete individual photos from the current session in the list view | 2026-03-07 |

### Diglett Backend
| ID | Feature | Status | PR | Notes | Added |
|----|---------|--------|----|-------|-------|
| BL-2 | Update Diglett Taulu schema to match AskDataAI | IN PROGRESS | #105075 | Taulu schema updated to match ask-diglett tools.py response (committed 2026-03-07) | 2026-03-07 |
| BL-6 | Diglett local KV store for development | IN PROGRESS | - | Branch: feature/diglett-local-store. In-memory KV store simulating Taulu so StartDiglettJob persists results and GetDiglettJobResult retrieves them locally | 2026-03-07 |

### Developer Workflow (Playground)
_No backlog items_

### Inventory Skills
_No backlog items_

## Skill Location
- Skill installed at: `~/.claude/skills/lingfei-feature-development-report/SKILL.md`
- Invoke with: `/lingfei-feature-development-report`
