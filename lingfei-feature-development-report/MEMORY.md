# Local Memory - dd-lingfei Feature Development Report

## Last Updated
2026-03-07 (evening run)

## GitHub Profile
- **Username:** dd-lingfei

## Workstreams

### Diglett iOS App
- **Goal:** Build the Diglett iOS app - photo capture, session management, store ID entry, and item comparison views
- **Repos:** doordash/ios
- **Last Active:** 2026-03-07

### Diglett Backend
- **Goal:** Build the Diglett backend on Pedregal - graph scaffolding with GenAI, Snowflake, S3, and Taulu integrations
- **Repos:** doordash/pedregal
- **Last Active:** 2026-03-07

### Diglett Infra
- **Goal:** Infrastructure and service registration for Diglett - Vault, staging environments
- **Repos:** doordash/tf_account_dash_management
- **Last Active:** 2026-03-07

### Developer Workflow (Playground)
- **Goal:** Improve personal developer workflow with skills, PR tracking, and automation tooling
- **Repos:** dd-lingfei/playground
- **Last Active:** 2026-03-07

### Inventory Skills
- **Goal:** Build and maintain inventory investigation skills (telescope, microscope, weather-report)
- **Repos:** doordash/inventory-skills
- **Last Active:** 2026-02-27

## Open PR Summary (as of 2026-03-07 evening)

### Diglett iOS App
- **doordash/ios#66162** - Sequential photo IDs - CI passing (pullapprove pending), no review yet
- **doordash/ios#66161** - Session management + store ID entry - CI passing (pullapprove pending), no review yet

### Diglett Backend
- **doordash/pedregal#105075** - Diglett graph scaffold v2 - CI FAILING (nodes dir structure check error), review required

### Diglett Infra
- **doordash/tf_account_dash_management#2039** - Vault registration for diglett staging - CI all green, APPROVED, ready to merge

### Developer Workflow (Playground)
- No open PRs

### Inventory Skills
- No open PRs

## Action Items
- PR #105075 (pedregal) has a FAILING CI check (Nodes directory structure check: ERROR) - needs fix
- PR #2039 (tf_account_dash_management) is approved and all checks passing - ready to merge
- PRs #66161 and #66162 (ios) are waiting on pullapprove and code review
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

## Skill Location
- Skill installed at: `~/.claude/skills/lingfei-feature-development-report/SKILL.md`
- Invoke with: `/lingfei-feature-development-report`
