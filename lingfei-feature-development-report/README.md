# Feature Development Report
_Last updated: 2026-03-08 (morning run)_

---

## Diglett iOS App
**Goal:** Build the Diglett iOS app - photo capture, session management, store ID entry, and item comparison views
**Repos:** doordash/ios
**Status:** ACTIVE

### Open PRs
| # | Repo | Title | CI | Review | Mergeable | +/- | Updated |
|---|------|-------|----|--------|-----------|-----|---------|
| [#66194](https://github.com/doordash/ios/pull/66194) | ios | Add barcode detection guardrail to Diglett photo review | PASSING (pullapprove only pending) | PENDING | YES | +219/-18 | 2026-03-08 |
| [#66162](https://github.com/doordash/ios/pull/66162) | ios | Use sequential photo IDs for Diglett captures | PASSING (pullapprove only pending) | PENDING | YES | +13/-1 | 2026-03-07 |
| [#66161](https://github.com/doordash/ios/pull/66161) | ios | Add Diglett session management with store ID entry and photo persistence | PASSING (pullapprove only pending) | PENDING | YES | +374/-52 | 2026-03-07 |

### Recently Closed/Merged
| # | Repo | Title | State | Updated |
|---|------|-------|-------|---------|
| [#66158](https://github.com/doordash/ios/pull/66158) | ios | Add Diglett photo upload flow | MERGED | 2026-03-07 |
| [#65950](https://github.com/doordash/ios/pull/65950) | ios | Add Diglett item detail comparison view | MERGED | 2026-03-06 |
| [#65948](https://github.com/doordash/ios/pull/65948) | ios | Add simulator sample images | MERGED | 2026-03-07 |
| [#65946](https://github.com/doordash/ios/pull/65946) | ios | Add Diglett photo capture tool | MERGED | 2026-03-06 |

### Backlog
| ID | Feature | Status | PR | Notes | Added |
|----|---------|--------|----|-------|-------|
| BL-1 | Barcode detection for photo quality validation | **IN PROGRESS** | [#66194](https://github.com/doordash/ios/pull/66194) | Auto-detect barcodes. 1 = green confirm. 0 or 2+ = warning + "Still Confirm" | 2026-03-07 |
| BL-3 | Trigger backend processing after photo upload + poll for status | BACKLOG | - | After upload, start processing job. Poll until complete. Log response + show "Processing completed." | 2026-03-07 |
| BL-4 | Use local backend endpoint in simulator | BACKLOG | - | Hit local Diglett backend instead of pedregal endpoint in simulator | 2026-03-07 |
| BL-5 | Delete photos from list view | BACKLOG | - | Allow user to delete individual photos from current session | 2026-03-07 |
| BL-7 | Detect QR codes in addition to barcodes | BACKLOG | - | Extend barcode guardrail to also detect QR codes for photo quality validation | 2026-03-07 |
| BL-9 | Sequential photo IDs for Diglett captures | **IN PROGRESS** | [#66162](https://github.com/doordash/ios/pull/66162) | Use sequential photo IDs instead of random | 2026-03-07 |
| BL-10 | Session management with store ID entry and photo persistence | **IN PROGRESS** | [#66161](https://github.com/doordash/ios/pull/66161) | Session management, store ID entry, and photo persistence | 2026-03-07 |

---

## Diglett Backend
**Goal:** Build the Diglett backend - Pedregal graph scaffolding, infra, Vault, GenAI, Snowflake, S3, and Taulu integrations
**Repos:** doordash/pedregal, doordash/tf_account_dash_management
**Status:** ACTIVE - one PR approved and ready to merge

### Open PRs
| # | Repo | Title | CI | Review | Mergeable | +/- | Updated |
|---|------|-------|----|--------|-----------|-----|---------|
| [#105109](https://github.com/doordash/pedregal/pull/105109) | pedregal | Add async job processor for Diglett pipeline | PENDING (aviator only) | PENDING | YES | +429/-320 | 2026-03-08 |
| [#105075](https://github.com/doordash/pedregal/pull/105075) | pedregal | Scaffold Diglett graph with GenAI, Snowflake, and Taulu | PENDING (aviator only) | REVIEW_REQUIRED | UNKNOWN | +1389/-0 | 2026-03-07 |
| [#2039](https://github.com/doordash/tf_account_dash_management/pull/2039) | tf_account_dash_management | Register diglett staging service with Vault | PASSING | APPROVED | YES | +16/-0 | 2026-03-07 |

### Recently Closed/Merged
| # | Repo | Title | State | Updated |
|---|------|-------|-------|---------|
| [#105103](https://github.com/doordash/pedregal/pull/105103) | pedregal | Add in-memory job store for local development | MERGED | 2026-03-07 |
| [#105035](https://github.com/doordash/pedregal/pull/105035) | pedregal | Scaffold Diglett graph v1 | CLOSED | 2026-03-07 |

### Backlog
| ID | Feature | Status | PR | Notes | Added |
|----|---------|--------|----|-------|-------|
| BL-2 | Update Diglett Taulu schema to match AskDataAI | **IN PROGRESS** | [#105075](https://github.com/doordash/pedregal/pull/105075) | Taulu schema updated to match ask-diglett tools.py response | 2026-03-07 |
| BL-6 | Diglett local KV store for development | **DONE** | [#105103](https://github.com/doordash/pedregal/pull/105103) | In-memory KV store simulating Taulu - MERGED | 2026-03-07 |
| BL-8 | Async job processing pipeline | **IN PROGRESS** | [#105109](https://github.com/doordash/pedregal/pull/105109) | After job creation, kick off async process: Snowflake, PortKey GenAI, Taulu | 2026-03-07 |
| BL-11 | Register diglett staging service with Vault | **IN PROGRESS** | [#2039](https://github.com/doordash/tf_account_dash_management/pull/2039) | Vault registration for diglett staging | 2026-03-07 |

---

## Developer Workflow (Playground)
**Goal:** Improve personal developer workflow with skills, PR tracking, and automation tooling
**Repos:** dd-lingfei/playground
**Status:** STALE - no open PRs

_No open PRs. Last activity: [#21](https://github.com/dd-lingfei/playground/pull/21) Update feature development report - auto-detect backlog (CLOSED 2026-03-08)_

### Backlog
_No backlog items_

---

## Inventory Skills
**Goal:** Build and maintain inventory investigation skills (telescope, microscope, weather-report)
**Repos:** doordash/inventory-skills
**Status:** STALE - no open PRs since 2026-02-27

_No open PRs. Last activity: [#35](https://github.com/doordash/inventory-skills/pull/35) Restore MCP server configuration documentation (MERGED 2026-02-27)_

### Backlog
_No backlog items_

---

## Action Items
- **MERGE NOW:** PR [#2039](https://github.com/doordash/tf_account_dash_management/pull/2039) is approved, all checks passing
- **REQUEST REVIEW:** PR [#105075](https://github.com/doordash/pedregal/pull/105075) CI all green (aviator pending), +1389/-0, 26 files - needs reviewer
- **REQUEST REVIEW:** PRs [#66161](https://github.com/doordash/ios/pull/66161), [#66162](https://github.com/doordash/ios/pull/66162), [#66194](https://github.com/doordash/ios/pull/66194) (ios) - all real CI passing, only pullapprove pending
- **NEW:** [#105109](https://github.com/doordash/pedregal/pull/105109) (async job processor) - CI passing (aviator pending), +429/-320, 8 files
- **BACKLOG TRANSITION:** BL-6 (Local KV store) -> **DONE** via merged [#105103](https://github.com/doordash/pedregal/pull/105103)
- **BACKLOG TRANSITION:** BL-8 (Async job processing) -> **IN PROGRESS** via [#105109](https://github.com/doordash/pedregal/pull/105109)
- **AUTO-CREATED:** BL-9 for [#66162](https://github.com/doordash/ios/pull/66162) (sequential photo IDs)
- **AUTO-CREATED:** BL-10 for [#66161](https://github.com/doordash/ios/pull/66161) (session management)
- **AUTO-CREATED:** BL-11 for [#2039](https://github.com/doordash/tf_account_dash_management/pull/2039) (Vault registration)
- **NOTE:** ios#66194 CI now fully passing (bitrise completed since last run)
- Inventory Skills workstream remains STALE
