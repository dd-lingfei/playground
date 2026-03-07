# Feature Development Report
_Last updated: 2026-03-07_

---

## Diglett iOS App
**Goal:** Build the Diglett iOS app - photo capture, session management, store ID entry, and item comparison views
**Repos:** doordash/ios
**Status:** ACTIVE

### Open PRs
| # | Repo | Title | CI | Review | Mergeable | +/- | Updated |
|---|------|-------|----|--------|-----------|-----|---------|
| [#66194](https://github.com/doordash/ios/pull/66194) | ios | Add barcode guardrail to Diglett photo review | PENDING (pullapprove only) | PENDING | YES | +121/-7 | 2026-03-07 |
| [#66162](https://github.com/doordash/ios/pull/66162) | ios | Use sequential photo IDs for Diglett captures | PENDING (pullapprove) | PENDING | YES | +13/-1 | 2026-03-07 |
| [#66161](https://github.com/doordash/ios/pull/66161) | ios | Add Diglett session management with store ID entry and photo persistence | PENDING (pullapprove) | PENDING | YES | +374/-52 | 2026-03-07 |

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

---

## Diglett Backend
**Goal:** Build the Diglett backend - Pedregal graph scaffolding, infra, Vault, GenAI, Snowflake, S3, and Taulu integrations
**Repos:** doordash/pedregal, doordash/tf_account_dash_management
**Status:** ACTIVE - one PR ready to merge

### Open PRs
| # | Repo | Title | CI | Review | Mergeable | +/- | Updated |
|---|------|-------|----|--------|-----------|-----|---------|
| [#105075](https://github.com/doordash/pedregal/pull/105075) | pedregal | Scaffold Diglett graph with GenAI, Snowflake, and Taulu | PASSING | REVIEW_REQUIRED | YES | +850/-0 | 2026-03-07 |
| [#2039](https://github.com/doordash/tf_account_dash_management/pull/2039) | tf_account_dash_management | Register diglett staging service with Vault | PASSING | APPROVED | YES | +16/-0 | 2026-03-07 |

### Recently Closed/Merged
| # | Repo | Title | State | Updated |
|---|------|-------|-------|---------|
| [#105035](https://github.com/doordash/pedregal/pull/105035) | pedregal | Scaffold Diglett graph v1 | CLOSED | 2026-03-07 |

### Backlog
| ID | Feature | Status | PR | Notes | Added |
|----|---------|--------|----|-------|-------|
| BL-2 | Update Diglett Taulu schema to match AskDataAI | **IN PROGRESS** | [#105075](https://github.com/doordash/pedregal/pull/105075) | Taulu schema updated to match ask-diglett tools.py response | 2026-03-07 |
| BL-6 | Diglett local KV store for development | **IN PROGRESS** | - | In-memory KV store simulating Taulu for local dev (branch: feature/diglett-local-store) | 2026-03-07 |
| BL-8 | Async job processing pipeline | BACKLOG | - | After job creation, kick off async process: 1) query Snowflake, 2) query PortKey GenAI, 3) update Taulu. Start with placeholder logic, get async framework running in Pedregal. | 2026-03-07 |

---

## Developer Workflow (Playground)
**Goal:** Improve personal developer workflow with skills, PR tracking, and automation tooling
**Repos:** dd-lingfei/playground
**Status:** STALE - no open PRs

_No open PRs. Last activity: [#10](https://github.com/dd-lingfei/playground/pull/10) Merge Diglett Infra into Backend (MERGED 2026-03-07)_

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
- **REQUEST REVIEW:** PR [#105075](https://github.com/doordash/pedregal/pull/105075) CI is all green - needs reviewer
- **REQUEST REVIEW:** PRs [#66161](https://github.com/doordash/ios/pull/66161), [#66162](https://github.com/doordash/ios/pull/66162), [#66194](https://github.com/doordash/ios/pull/66194) (ios) - all real CI passing, only pullapprove pending
- **BACKLOG:** BL-1 (Barcode detection) **IN PROGRESS** via [#66194](https://github.com/doordash/ios/pull/66194)
- **BACKLOG:** BL-2 (Taulu schema) **IN PROGRESS** via [#105075](https://github.com/doordash/pedregal/pull/105075)
- **BACKLOG:** BL-6 (Local KV store) **IN PROGRESS** on branch feature/diglett-local-store
- Inventory Skills workstream remains STALE
