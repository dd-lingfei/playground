# Development Report — Persistent Changelog

## Metadata
- **last_run_date:** 2026-03-22
- **github_username:** dd-lingfei
- **tracked_repos:** doordash/ios, doordash/pedregal, doordash/tf_account_dash_management, dd-lingfei/playground, doordash/inventory-skills
- **jira_project:** DIGLETT

## Workstreams (reference)

### Diglett iOS App
- **Goal:** Build the Diglett iOS app — photo capture, session management, store ID entry, and item comparison views
- **Repos:** doordash/ios

### Diglett Backend
- **Goal:** Build the Diglett backend — Pedregal graph scaffolding, infra, Vault, GenAI, Snowflake, S3, and Taulu integrations
- **Repos:** doordash/pedregal, doordash/tf_account_dash_management

### Developer Workflow (Playground)
- **Goal:** Improve personal developer workflow with skills, PR tracking, and automation tooling
- **Repos:** dd-lingfei/playground

### Inventory Skills
- **Goal:** Build and maintain inventory investigation skills (telescope, microscope, weather-report)
- **Repos:** doordash/inventory-skills

## Changelog

<!-- New entries are prepended here, newest first -->

### 2026-03-22
- [doordash/ios] Merged: Auto-prefix Diglett store ID ([#68937](https://github.com/doordash/ios/pull/68937)) — DIGLETT-24
- [doordash/ios] Merged: Fix UI freeze when exiting Diglett ([#68938](https://github.com/doordash/ios/pull/68938)) — DIGLETT-33
- [doordash/ios] Merged: Display newest photos first in capture and list views ([#68928](https://github.com/doordash/ios/pull/68928)) — DIGLETT-28
- [doordash/ios] Merged: Allow user to upload photos from photo library ([#68931](https://github.com/doordash/ios/pull/68931)) — DIGLETT-27
- [dd-lingfei/playground] Merged: Rename feature report skill to development-report ([#40](https://github.com/dd-lingfei/playground/pull/40))
- [doordash/ios] Merged: Diglett upload-only: capture, barcode detect, and upload photos ([#68837](https://github.com/doordash/ios/pull/68837)) — DIGLETT-11
- [dd-lingfei/playground] Merged: Update feature development report for 2026-03-22 ([#39](https://github.com/dd-lingfei/playground/pull/39))
- [dd-lingfei/playground] Merged: Replace MEMORY.md/README.md I/O with JIRA ([#30](https://github.com/dd-lingfei/playground/pull/30))
- JIRA: DIGLETT-30 marked Done — Add the photo-capture based functions
- JIRA: DIGLETT-4 marked Done — Barcode detection for photo quality validation
- JIRA: DIGLETT-6 marked Done — Session management with store ID entry and photo persistence
- JIRA: DIGLETT-7 marked Done — Use sequential photo IDs for Diglett captures
