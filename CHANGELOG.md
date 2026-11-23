# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Initial project documentation: CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, CHANGELOG.md.
- Persistent sessions via SQLite (`DatabaseSessionService`); financial profile stored per user and kept across chat threads and reloads.
- Browser-generated user ID sent to the agent as a CopilotKit property, validated server-side.
- CORS middleware on the agent, configurable with `ALLOWED_ORIGINS`.

### Changed

- Next.js bumped to 16.3.5 and all `@copilotkit/*` packages pinned to 1.71.2 (fixes a duplicate `react-core` that broke the app).
- Removed blanket `ignoreBuildErrors`; the one known upstream type mismatch is suppressed on its line only.

## [0.1.0] - 2026-09-13

### Added

- Initial commit: AI financial coach agent — multi-agent budget, savings, and debt-reduction coach built with CopilotKit, AG-UI, and Google's ADK on top of Next.js.
