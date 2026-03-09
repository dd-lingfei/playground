# Feature Development Report
_Last updated: 2026-03-09 (morning run)_

---

## Diglett iOS App
**Goal:** Build the Diglett iOS app - photo capture, session management, store ID entry, and item comparison views
**Repos:** doordash/ios
**Status:** ACTIVE - 4 open PRs, 1 approved and ready to merge

### Open PRs
| # | Repo | Title | CI | Review | Mergeable | +/- | Updated |
|---|------|-------|----|--------|-----------|-----|---------|
| [#66194](https://github.com/doordash/ios/pull/66194) | ios | Add barcode detection guardrail to Diglett photo review | PASSING | APPROVED | YES | +219/-18 | ~8 hrs ago |
| [#66259](https://github.com/doordash/ios/pull/66259) | ios | Invoke Diglett gRPC backend for photo processing | PASSING | PENDING | YES | +1425/-41 | just now |
| [#66162](https://github.com/doordash/ios/pull/66162) | ios | Use sequential photo IDs for Diglett captures | PASSING | PENDING | YES | +13/-1 | ~1 day ago |
| [#66161](https://github.com/doordash/ios/pull/66161) | ios | Add Diglett session management with store ID entry and photo persistence | PASSING | PENDING | UNKNOWN | +374/-52 | ~2 days ago |

### Recently Closed/Merged
| # | Repo | Title | State | Updated |
|---|------|-------|-------|---------|
| [#66158](https://github.com/doordash/ios/pull/66158) | ios | Add Diglett photo upload flow | MERGED | 2026-03-07 |
| [#65950](https://github.com/doordash/ios/pull/65950) | ios | Add Diglett item detail comparison view | MERGED | 2026-03-06 |
| [#65948](https://github.com/doordash/ios/pull/65948) | ios | Add simulator sample images | MERGED | 2026-03-07 |
| [#65946](https://github.com/doordash/ios/pull/65946) | ios | Add Diglett photo capture tool | MERGED | 2026-03-06 |

---

## Diglett Backend
**Goal:** Build the Diglett backend - Pedregal graph scaffolding, infra, Vault, GenAI, Snowflake, S3, and Taulu integrations
**Repos:** doordash/pedregal, doordash/tf_account_dash_management
**Status:** ACTIVE - 4 open PRs, 1 approved and ready to merge

### Open PRs
| # | Repo | Title | CI | Review | Mergeable | +/- | Updated |
|---|------|-------|----|--------|-----------|-----|---------|
| [#2039](https://github.com/doordash/tf_account_dash_management/pull/2039) | tf_account_dash_management | Register diglett staging service with Vault | PASSING | APPROVED | YES | +16/-0 | ~2 days ago |
| [#105244](https://github.com/doordash/pedregal/pull/105244) | pedregal | Add catalog store with S3 cache and enrich Diglett Get API | PASSING | PENDING | YES | +1481/-43 | ~3 hrs ago |
| [#105109](https://github.com/doordash/pedregal/pull/105109) | pedregal | Add async job processor for Diglett pipeline | PASSING | PENDING | YES | +487/-350 | just now |
| [#105075](https://github.com/doordash/pedregal/pull/105075) | pedregal | Scaffold Diglett graph with GenAI, Snowflake, and Taulu | PENDING (aviator) | REVIEW_REQUIRED | UNKNOWN | +1389/-0 | ~1 day ago |

### Recently Closed/Merged
| # | Repo | Title | State | Updated |
|---|------|-------|-------|---------|
| [#105103](https://github.com/doordash/pedregal/pull/105103) | pedregal | Add in-memory job store for local development | MERGED | 2026-03-07 |
| [#105035](https://github.com/doordash/pedregal/pull/105035) | pedregal | Scaffold Diglett graph v1 | CLOSED | 2026-03-07 |

---

## Developer Workflow (Playground)
**Goal:** Improve personal developer workflow with skills, PR tracking, and automation tooling
**Repos:** dd-lingfei/playground
**Status:** STALE - no open PRs

_No open PRs. Last activity: [#27](https://github.com/dd-lingfei/playground/pull/27) Update BL-4: connect with production UG endpoint (MERGED today)_

---

## Inventory Skills
**Goal:** Build and maintain inventory investigation skills (telescope, microscope, weather-report)
**Repos:** doordash/inventory-skills
**Status:** STALE - no open PRs since 2026-02-27

_No open PRs. Last activity: [#35](https://github.com/doordash/inventory-skills/pull/35) Restore MCP server configuration documentation (MERGED 2026-02-27)_

---

## Action Items
- **MERGE NOW:** PR [#66194](https://github.com/doordash/ios/pull/66194) (barcode guardrail) is **APPROVED**, all CI passing - ready to merge!
- **MERGE NOW:** PR [#2039](https://github.com/doordash/tf_account_dash_management/pull/2039) (Vault registration) is **APPROVED**, all CI passing
- **REQUEST REVIEW:** PR [#66259](https://github.com/doordash/ios/pull/66259) (gRPC backend invocation) - CI now all PASSING, needs code review (+1425/-41, 7 files)
- **REQUEST REVIEW:** PR [#105244](https://github.com/doordash/pedregal/pull/105244) (catalog store + S3 cache) - CI all green, needs reviewer (+1481/-43, 12 files)
- **REQUEST REVIEW:** PR [#105109](https://github.com/doordash/pedregal/pull/105109) (async job processor) - CI passing, needs reviewer (+487/-350, 8 files)
- **REQUEST REVIEW:** PR [#105075](https://github.com/doordash/pedregal/pull/105075) (graph scaffold) - CI passing (aviator pending), needs reviewer (+1389/-0, 26 files)
- **REQUEST REVIEW:** PRs [#66161](https://github.com/doordash/ios/pull/66161), [#66162](https://github.com/doordash/ios/pull/66162) (ios) - all real CI passing, only pullapprove pending
- Inventory Skills workstream remains STALE (last activity 2026-02-27)

**Changes since last report:**
- ios#66259 CI completed successfully (was PENDING, now all PASSING)
