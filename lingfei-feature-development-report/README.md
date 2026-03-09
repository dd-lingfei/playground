# Feature Development Report
_Last updated: 2026-03-08 (late night run)_

---

## Diglett iOS App
**Goal:** Build the Diglett iOS app - photo capture, session management, store ID entry, and item comparison views
**Repos:** doordash/ios
**Status:** ACTIVE - 4 open PRs, 1 approved and ready to merge, 1 new PR with CI running

### Open PRs
| # | Repo | Title | CI | Review | Mergeable | +/- | Updated |
|---|------|-------|----|--------|-----------|-----|---------|
| [#66259](https://github.com/doordash/ios/pull/66259) | ios | Invoke Diglett gRPC backend for photo processing | PENDING (bitrise running) | PENDING | YES | +1361/-41 | 2026-03-08 |
| [#66194](https://github.com/doordash/ios/pull/66194) | ios | Add barcode detection guardrail to Diglett photo review | PASSING | APPROVED | YES | +219/-18 | 2026-03-08 |
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
| BL-1 | Barcode detection for photo quality validation | **IN PROGRESS** | [#66194](https://github.com/doordash/ios/pull/66194) | APPROVED - ready to merge | 2026-03-07 |
| BL-3 | Trigger backend processing after photo upload + poll for status | **IN PROGRESS** | [#66259](https://github.com/doordash/ios/pull/66259) | Matched via ios#66259 (gRPC backend invocation). CI running. | 2026-03-07 |
| BL-4 | Connect with the production UG endpoint for backend processing | BACKLOG | - | Connect iOS app to production Unified Gateway endpoint for backend processing | 2026-03-07 |
| BL-5 | Delete photos from list view | BACKLOG | - | Allow user to delete individual photos from current session | 2026-03-07 |
| BL-7 | Detect QR codes in addition to barcodes | BACKLOG | - | Extend barcode guardrail to also detect QR codes | 2026-03-07 |
| BL-9 | Sequential photo IDs for Diglett captures | **IN PROGRESS** | [#66162](https://github.com/doordash/ios/pull/66162) | Needs code review | 2026-03-07 |
| BL-10 | Session management with store ID entry and photo persistence | **IN PROGRESS** | [#66161](https://github.com/doordash/ios/pull/66161) | Needs code review | 2026-03-07 |
| BL-13 | Connect Dasher iOS app to local backend for end-to-end testing | BACKLOG | - | Hit local running Diglett backend instance from the iOS app for E2E testing | 2026-03-08 |
| BL-14 | Connect iOS app to backend via Unified Gateway (UG) | BACKLOG | - | Route iOS app requests to Diglett backend through UG in non-local environments | 2026-03-08 |
| BL-18 | Stabilize session and photo ordering in list view | BACKLOG | - | When user clicks "upload for processing", list view reorders sessions/photos. Fix to remain stable. | 2026-03-08 |

---

## Diglett Backend
**Goal:** Build the Diglett backend - Pedregal graph scaffolding, infra, Vault, GenAI, Snowflake, S3, and Taulu integrations
**Repos:** doordash/pedregal, doordash/tf_account_dash_management
**Status:** ACTIVE - 4 open PRs, 1 approved and ready to merge, 1 new PR with all CI passing

### Open PRs
| # | Repo | Title | CI | Review | Mergeable | +/- | Updated |
|---|------|-------|----|--------|-----------|-----|---------|
| [#105244](https://github.com/doordash/pedregal/pull/105244) | pedregal | Add catalog store with S3 cache and enrich Diglett Get API | PASSING | PENDING | YES | +1481/-43 | 2026-03-08 |
| [#105109](https://github.com/doordash/pedregal/pull/105109) | pedregal | Add async job processor for Diglett pipeline | PASSING | PENDING | YES | +487/-350 | 2026-03-08 |
| [#105075](https://github.com/doordash/pedregal/pull/105075) | pedregal | Scaffold Diglett graph with GenAI, Snowflake, and Taulu | PENDING (aviator) | REVIEW_REQUIRED | UNKNOWN | +1389/-0 | 2026-03-07 |
| [#2039](https://github.com/doordash/tf_account_dash_management/pull/2039) | tf_account_dash_management | Register diglett staging service with Vault | PASSING | APPROVED | YES | +16/-0 | 2026-03-07 |

### Recently Closed/Merged
| # | Repo | Title | State | Updated |
|---|------|-------|-------|---------|
| [#105103](https://github.com/doordash/pedregal/pull/105103) | pedregal | Add in-memory job store for local development | MERGED | 2026-03-07 |
| [#105035](https://github.com/doordash/pedregal/pull/105035) | pedregal | Scaffold Diglett graph v1 | CLOSED | 2026-03-07 |

### Backlog
| ID | Feature | Status | PR | Notes | Added |
|----|---------|--------|----|-------|-------|
| BL-2 | Update Diglett Taulu schema to match AskDataAI | **IN PROGRESS** | [#105075](https://github.com/doordash/pedregal/pull/105075) | Needs reviewer (+1389/-0, 26 files) | 2026-03-07 |
| BL-6 | Diglett local KV store for development | **DONE** | [#105103](https://github.com/doordash/pedregal/pull/105103) | In-memory KV store simulating Taulu - MERGED | 2026-03-07 |
| BL-8 | Async job processing pipeline | **IN PROGRESS** | [#105109](https://github.com/doordash/pedregal/pull/105109) | CI passing, needs reviewer | 2026-03-07 |
| BL-11 | Register diglett staging service with Vault | **IN PROGRESS** | [#2039](https://github.com/doordash/tf_account_dash_management/pull/2039) | APPROVED - ready to merge | 2026-03-07 |
| BL-12 | Expose Pedregal graph via Unified Gateway (UG) | BACKLOG | - | Expose Diglett endpoints through Unified Gateway | 2026-03-08 |
| BL-15 | Catalog retrieval and S3-based cache system | **IN PROGRESS** | [#105244](https://github.com/doordash/pedregal/pull/105244) | Matched via pedregal#105244 (catalog store + S3 cache). CI all green. | 2026-03-08 |
| BL-16 | PortKey / GenAI integration | BACKLOG | - | Backend support for calling PortKey / GenAI services | 2026-03-08 |
| BL-17 | Item-catalog matching | BACKLOG | - | Backend support for matching captured items against catalog data | 2026-03-08 |

---

## Developer Workflow (Playground)
**Goal:** Improve personal developer workflow with skills, PR tracking, and automation tooling
**Repos:** dd-lingfei/playground
**Status:** STALE - no open PRs

_No open PRs. Last activity: [#25](https://github.com/dd-lingfei/playground/pull/25) Add backlog BL-13 and BL-14 (MERGED 2026-03-08)_

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
- **MERGE NOW:** PR [#66194](https://github.com/doordash/ios/pull/66194) (barcode guardrail) is **APPROVED**, all CI passing - ready to merge!
- **MERGE NOW:** PR [#2039](https://github.com/doordash/tf_account_dash_management/pull/2039) (Vault registration) is **APPROVED**, all CI passing
- **NEW PR:** [#66259](https://github.com/doordash/ios/pull/66259) (gRPC backend invocation) CI running - needs review when CI completes
- **NEW PR:** [#105244](https://github.com/doordash/pedregal/pull/105244) (catalog store + S3 cache) all CI passing - needs reviewer (+1481/-43, 12 files)
- **REQUEST REVIEW:** PR [#105109](https://github.com/doordash/pedregal/pull/105109) async job processor - CI passing, needs reviewer
- **REQUEST REVIEW:** PR [#105075](https://github.com/doordash/pedregal/pull/105075) graph scaffold - CI passing (aviator pending), needs reviewer (+1389/-0, 26 files)
- **REQUEST REVIEW:** PRs [#66161](https://github.com/doordash/ios/pull/66161), [#66162](https://github.com/doordash/ios/pull/66162) (ios) - all real CI passing, only pullapprove pending
- **BACKLOG TRANSITION:** BL-3 moved to IN PROGRESS via ios#66259 (gRPC backend invocation)
- **BACKLOG TRANSITION:** BL-15 moved to IN PROGRESS via pedregal#105244 (catalog store + S3 cache)
- Inventory Skills workstream remains STALE (last activity 2026-02-27)
