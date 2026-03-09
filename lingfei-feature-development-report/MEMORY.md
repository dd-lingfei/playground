# Local Memory - dd-lingfei Feature Development Report

## Last Updated
2026-03-09 (morning run)

## GitHub Profile
- **Username:** dd-lingfei

## Workstreams

### Diglett iOS App
- **Goal:** Build the Diglett iOS app - photo capture, session management, store ID entry, and item comparison views
- **Repos:** doordash/ios
- **Last Active:** 2026-03-09

### Diglett Backend
- **Goal:** Build the Diglett backend - Pedregal graph scaffolding, infra, Vault, GenAI, Snowflake, S3, and Taulu integrations
- **Repos:** doordash/pedregal, doordash/tf_account_dash_management
- **Last Active:** 2026-03-09

### Developer Workflow (Playground)
- **Goal:** Improve personal developer workflow with skills, PR tracking, and automation tooling
- **Repos:** dd-lingfei/playground
- **Last Active:** 2026-03-09

### Inventory Skills
- **Goal:** Build and maintain inventory investigation skills (telescope, microscope, weather-report)
- **Repos:** doordash/inventory-skills
- **Last Active:** 2026-02-27

## Open PR Summary (as of 2026-03-09 morning)

### Diglett iOS App
- **doordash/ios#66194** - Barcode guardrail for photo review - CI PASSING (all green), APPROVED, ready to merge, +219/-18, 2 files
- **doordash/ios#66259** - Invoke Diglett gRPC backend for photo processing - CI PASSING (all green), no review yet, +1425/-41, 7 files
- **doordash/ios#66162** - Sequential photo IDs - CI passing (pullapprove only pending), no review yet, +13/-1, 2 files
- **doordash/ios#66161** - Session management + store ID entry - CI passing (pullapprove only pending), no review yet, +374/-52, 6 files

### Diglett Backend
- **doordash/tf_account_dash_management#2039** - Vault registration for diglett staging - CI all green, APPROVED, ready to merge, +16/-0, 2 files
- **doordash/pedregal#105244** - Catalog store with S3 cache and enrich Diglett Get API - CI PASSING (all green), no review yet, +1481/-43, 12 files
- **doordash/pedregal#105109** - Async job processor for Diglett pipeline - CI PASSING (all green), no review yet, +487/-350, 8 files
- **doordash/pedregal#105075** - Diglett graph scaffold v2 - CI passing (aviator pending), review required, +1389/-0, 26 files

### Developer Workflow (Playground)
- No open PRs

### Inventory Skills
- No open PRs

## Action Items
- PR #66194 (ios) barcode guardrail is APPROVED and all CI passing - MERGE NOW
- PR #2039 (tf_account_dash_management) is approved and all checks passing - MERGE NOW
- PR #66259 (ios) gRPC backend invocation - CI now all PASSING, needs code review (+1425/-41, 7 files)
- PR #105244 (pedregal) catalog store + S3 cache - CI all green, needs reviewer (+1481/-43, 12 files)
- PR #105109 (pedregal) async job processor - CI passing, needs reviewer (+487/-350, 8 files)
- PR #105075 (pedregal) CI all green (aviator pending) - needs reviewer (+1389/-0, 26 files)
- PRs #66161 and #66162 (ios) need code review - all real CI passing, only pullapprove pending
- Inventory Skills workstream is STALE - last activity was 2026-02-27

## Recently Closed/Merged PRs
- **dd-lingfei/playground#27** - Update BL-4: connect with production UG endpoint - MERGED 2026-03-09
- **dd-lingfei/playground#26** - Update feature development report - 2026-03-08 late night - MERGED 2026-03-09
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

## Skill Location
- Skill installed at: `~/.claude/skills/lingfei-feature-development-report/SKILL.md`
- Invoke with: `/lingfei-feature-development-report`
