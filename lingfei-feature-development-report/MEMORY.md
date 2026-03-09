# Local Memory - dd-lingfei Feature Development Report

## Last Updated
2026-03-08 (late night run)

## GitHub Profile
- **Username:** dd-lingfei

## Workstreams

### Diglett iOS App
- **Goal:** Build the Diglett iOS app - photo capture, session management, store ID entry, and item comparison views
- **Repos:** doordash/ios
- **Last Active:** 2026-03-08

### Diglett Backend
- **Goal:** Build the Diglett backend - Pedregal graph scaffolding, infra, Vault, GenAI, Snowflake, S3, and Taulu integrations
- **Repos:** doordash/pedregal, doordash/tf_account_dash_management
- **Last Active:** 2026-03-08

### Developer Workflow (Playground)
- **Goal:** Improve personal developer workflow with skills, PR tracking, and automation tooling
- **Repos:** dd-lingfei/playground
- **Last Active:** 2026-03-08

### Inventory Skills
- **Goal:** Build and maintain inventory investigation skills (telescope, microscope, weather-report)
- **Repos:** doordash/inventory-skills
- **Last Active:** 2026-02-27

## Open PR Summary (as of 2026-03-08 late night)

### Diglett iOS App
- **doordash/ios#66259** - Invoke Diglett gRPC backend for photo processing - CI PENDING (bitrise running), no review yet, +1361/-41, 7 files
- **doordash/ios#66194** - Barcode guardrail for photo review - CI PASSING (all green), APPROVED, ready to merge, +219/-18
- **doordash/ios#66162** - Sequential photo IDs - CI passing (pullapprove only pending), no review yet, +13/-1
- **doordash/ios#66161** - Session management + store ID entry - CI passing (pullapprove only pending), no review yet, +374/-52

### Diglett Backend
- **doordash/pedregal#105244** - Catalog store with S3 cache and enrich Diglett Get API - CI PASSING (all green), no review yet, +1481/-43, 12 files
- **doordash/pedregal#105109** - Async job processor for Diglett pipeline - CI PASSING (all green), no review yet, +487/-350, 8 files
- **doordash/pedregal#105075** - Diglett graph scaffold v2 - CI passing (aviator pending), review required, +1389/-0, 26 files
- **doordash/tf_account_dash_management#2039** - Vault registration for diglett staging - CI all green, APPROVED, ready to merge, +16/-0

### Developer Workflow (Playground)
- No open PRs

### Inventory Skills
- No open PRs

## Action Items
- PR #66194 (ios) barcode guardrail is APPROVED and all CI passing - MERGE NOW
- PR #2039 (tf_account_dash_management) is approved and all checks passing - MERGE NOW
- PR #66259 (ios) gRPC backend invocation - CI running, needs review when CI completes
- PR #105244 (pedregal) catalog store + S3 cache - CI all green, needs reviewer (+1481/-43, 12 files)
- PR #105109 (pedregal) async job processor - CI passing, needs reviewer
- PR #105075 (pedregal) CI all green (aviator pending) - needs reviewer (+1389/-0, 26 files)
- PRs #66161 and #66162 (ios) need code review - all real CI passing, only pullapprove pending
- Inventory Skills workstream is STALE - last activity was 2026-02-27

## Recently Closed/Merged PRs
- **dd-lingfei/playground#25** - Add backlog BL-13 and BL-14: iOS local backend E2E and UG connection - MERGED 2026-03-08
- **dd-lingfei/playground#24** - Add backlog BL-12: expose Pedregal graph via Unified Gateway - MERGED 2026-03-08
- **dd-lingfei/playground#23** - Update feature development report - 2026-03-08 evening - MERGED
- **dd-lingfei/playground#22** - Update feature development report - 2026-03-08 - CLOSED (superseded)
- **dd-lingfei/playground#21** - Update feature development report - auto-detect backlog from PRs - CLOSED (superseded)
- **dd-lingfei/playground#20** - Add auto-detect backlog items from unlinked open PRs - MERGED
- **dd-lingfei/playground#19** - Update feature development report - 2026-03-07 post-BL8 - CLOSED (superseded)
- **dd-lingfei/playground#18** - Add backlog BL-8: async job processing pipeline - CLOSED (superseded)
- **dd-lingfei/playground#17** - Update feature development report - 2026-03-07 end of day - CLOSED (superseded)
- **doordash/pedregal#105103** - Add in-memory job store for local development - MERGED
- **dd-lingfei/playground#16** - Check in SKILL.md for feature development report - MERGED
- **dd-lingfei/playground#15** - Add README.md report for feature development tracking - MERGED
- **dd-lingfei/playground#14** - Add backlog BL-7: detect QR codes in addition to barcodes - MERGED
- **dd-lingfei/playground#13** - Add BL-6 (local KV store) to backlog, move BL-2 to IN PROGRESS - MERGED
- **dd-lingfei/playground#12** - Update feature development report - 2026-03-07 v2 - MERGED
- **dd-lingfei/playground#11** - Update feature development report - 2026-03-07 final - CLOSED (stale)
- **dd-lingfei/playground#10** - Merge Diglett Infra workstream into Diglett Backend - MERGED
- **dd-lingfei/playground#9** - Update feature development report - 2026-03-07 late night - CLOSED (stale)
- **dd-lingfei/playground#8** - Add backlog BL-5: delete photos from list view - MERGED
- **dd-lingfei/playground#7** - Add backlog items BL-2, BL-3, BL-4 - MERGED
- **dd-lingfei/playground#6** - Add backlog feature to feature development report - MERGED
- **dd-lingfei/playground#5** - Update feature development report - 2026-03-07 night - CLOSED (stale)
- **dd-lingfei/playground#4** - Add Best Buy scraper and update requirements - MERGED
- **dd-lingfei/playground#3** - Update feature development report - 2026-03-07 - MERGED
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
| BL-1 | Barcode detection for photo quality validation | IN PROGRESS | #66194 | APPROVED - ready to merge | 2026-03-07 |
| BL-3 | Trigger backend processing after photo upload + poll for status | IN PROGRESS | #66259 | Matched via ios#66259 (gRPC backend invocation) | 2026-03-07 |
| BL-4 | Use local backend endpoint in simulator | BACKLOG | - | When running in simulator, hit local Diglett backend instead of pedregal endpoint | 2026-03-07 |
| BL-5 | Delete photos from list view | BACKLOG | - | Allow user to delete individual photos from the current session in the list view | 2026-03-07 |
| BL-7 | Detect QR codes in addition to barcodes | BACKLOG | - | Extend the barcode guardrail to also detect QR codes for photo quality validation | 2026-03-07 |
| BL-9 | Sequential photo IDs for Diglett captures | IN PROGRESS | #66162 | Use sequential photo IDs instead of random | 2026-03-07 |
| BL-10 | Session management with store ID entry and photo persistence | IN PROGRESS | #66161 | Session management, store ID entry, and photo persistence | 2026-03-07 |
| BL-13 | Connect Dasher iOS app to local backend for end-to-end testing | BACKLOG | - | Hit local running Diglett backend instance from the iOS app for E2E testing | 2026-03-08 |
| BL-14 | Connect iOS app to backend via Unified Gateway (UG) | BACKLOG | - | Route iOS app requests to Diglett backend through UG in non-local environments | 2026-03-08 |
| BL-18 | Stabilize session and photo ordering in list view | BACKLOG | - | When user clicks "upload for processing", the list view reorders sessions and photos. Fix ordering to remain stable. | 2026-03-08 |

### Diglett Backend
| ID | Feature | Status | PR | Notes | Added |
|----|---------|--------|----|-------|-------|
| BL-2 | Update Diglett Taulu schema to match AskDataAI | IN PROGRESS | #105075 | Taulu schema updated to match ask-diglett tools.py response (committed 2026-03-07) | 2026-03-07 |
| BL-6 | Diglett local KV store for development | DONE | #105103 | In-memory KV store simulating Taulu - pedregal#105103 merged 2026-03-07 | 2026-03-07 |
| BL-8 | Async job processing pipeline | IN PROGRESS | #105109 | After job creation, kick off async process: 1) query Snowflake table, 2) query PortKey GenAI, 3) update Taulu database | 2026-03-07 |
| BL-11 | Register diglett staging service with Vault | IN PROGRESS | #2039 | Vault registration for diglett staging. APPROVED - ready to merge | 2026-03-07 |
| BL-12 | Expose Pedregal graph via Unified Gateway (UG) | BACKLOG | - | Expose the Diglett Pedregal graph endpoints through Unified Gateway | 2026-03-08 |
| BL-15 | Catalog retrieval and S3-based cache system | IN PROGRESS | #105244 | Matched via pedregal#105244 (catalog store + S3 cache) | 2026-03-08 |
| BL-16 | PortKey / GenAI integration | BACKLOG | - | Backend support for calling PortKey / GenAI services | 2026-03-08 |
| BL-17 | Item-catalog matching | BACKLOG | - | Backend support for matching captured items against catalog data | 2026-03-08 |

### Developer Workflow (Playground)
_No backlog items_

### Inventory Skills
_No backlog items_

## Skill Location
- Skill installed at: `~/.claude/skills/lingfei-feature-development-report/SKILL.md`
- Invoke with: `/lingfei-feature-development-report`
