# Contributing

Thanks for your interest in improving the AI Financial Coach Agent.

## Getting set up

Follow the [Getting Started](README.md#getting-started) steps in the README to install dependencies and run the app locally.

## Project layout

- `src/` — Next.js frontend (UI, CopilotKit integration, tool-rendered cards)
- `agent/` — Python ADK agent (budget, savings, and debt-reduction tools)
- `scripts/` — setup/run helpers for the Python agent
- `docker/` — Dockerfiles for the app and agent services

## Making changes

1. Create a branch off `main` for your change.
2. Keep pull requests focused — one logical change per PR.
3. Match the existing code style (TypeScript/React conventions in `src/`, Python conventions in `agent/`).
4. Run the app locally (`npm run dev`) and verify the affected flow (budget, savings, or debt-reduction) before opening a PR.

## Submitting a pull request

1. Push your branch and open a PR against `main`.
2. Describe what changed and why, and how you tested it.
3. Link any related issues.

## Reporting bugs

Open a GitHub issue with steps to reproduce, what you expected, and what happened instead. Include relevant logs from the UI or agent server (`npm run dev:debug` enables debug logging).

## Security issues

Please do not open a public issue for security vulnerabilities — see [SECURITY.md](SECURITY.md).
