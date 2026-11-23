# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A multi-agent financial coach: a Next.js/React frontend (chat sidebar + tool-rendered report cards) talks to a Python ADK agent over AG-UI/CopilotKit. The agent analyzes a user's budget, plans savings, and builds debt-payoff strategies (avalanche & snowball).

## Commands

```bash
npm install              # install JS deps (also runs install:agent via postinstall)
npm run install:agent    # uv sync inside agent/ (installs Python deps into agent/.venv)

npm run dev              # run both UI (Next.js, --turbopack) and agent (FastAPI) concurrently
npm run dev:ui           # UI only, on the default Next.js port
npm run dev:agent        # agent only, on port 8000 (scripts/run-agent.sh -> uv run main.py)
npm run dev:debug        # dev with LOG_LEVEL=debug

npm run build            # next build
npm start                # next start (production)
```

Required env var: `GOOGLE_API_KEY` (Gemini/Makersuite key) — the agent process warns and still boots without it, but LLM calls will fail.

There is no lint or test script configured in `package.json`. `docker-compose.test.yml` runs a Playwright smoke test, but it mounts `../../../showcase/tests` and expects to run from inside the upstream CopilotKit examples monorepo — it will not work standalone in this repo as checked out.

To run/debug the agent directly:

```bash
cd agent
source .venv/bin/activate
uv run main.py            # or: uvicorn main:app --reload --port 8000
curl localhost:8000/health
```

## Architecture

**Two processes, one contract.** The Next.js app never calls Gemini directly — it proxies through [src/app/api/copilotkit/route.ts](src/app/api/copilotkit/route.ts), which registers the ADK backend as a CopilotKit `HttpAgent` under the fixed key `my_agent`, pointed at `AGENT_URL` (default `http://localhost:8000/`). The frontend's `useCoAgent<AgentState>({ name: "my_agent", ... })` in [src/app/page.tsx](src/app/page.tsx) is what ties the two together — the key `my_agent` must match on both sides regardless of what the ADK agent itself is named internally (`FinanceCoachAgent`).

**Users and persistence.** The browser generates a random user ID (stored in localStorage by [src/components/app-providers.tsx](src/components/app-providers.tsx)) and sends it as a CopilotKit `properties.userId`, which arrives in the agent as `forwarded_props`. `agent/main.py` reads it via `_user_id_from_input` (validated) and uses it as the ADK user ID. Sessions persist to SQLite via `DatabaseSessionService` at `SESSION_DB_URL` (default `sqlite+aiosqlite:///./data/sessions.db`). The financial profile is stored under `user:financial_data` (`FINANCIAL_DATA_KEY`), so it survives across chat threads and page reloads; the `user:` prefix is what makes ADK scope it per user. Analysis outputs are session-scoped.

**Shared state is the integration point, not return values.** [agent/main.py](agent/main.py) keeps the `user:financial_data` dict in ADK session state (initialized by `on_before_agent`). Every specialist sub-agent writes its structured output back into that same shared state via `output_key` (`budget_analysis`, `savings_strategy`, `debt_reduction`), and reads what came before it via `before_model_callback` injectors (`_make_state_injector`) that prepend prior results as text into the system instruction. `src/lib/types.ts` mirrors these Pydantic schemas by hand — if you change a schema in `agent/main.py`, update the matching TypeScript type and the card component that renders it.

**Coach agent as a router, not a pipeline.** `coach_agent` (`FinanceCoachAgent`) is the only agent the frontend talks to. It has 5 tools: `update_financial_data` (patches profile fields with merge/append semantics — never overwrites the whole profile) and four `AgentTool`-wrapped agents (`BudgetAnalysisAgent`, `SavingsStrategyAgent`, `DebtReductionAgent`, and `FullAnalysisPipeline`, a `SequentialAgent` running all three in order). All four are `skip_summarization=True` so the coach doesn't re-narrate their JSON output in chat — the UI renders it as a card instead. Routing logic (which tool to call for a given user message) lives entirely in `COACH_INSTRUCTION`'s prompt, not in code.

**Rendering tool calls as UI.** Each tool above has a matching `useCopilotAction({ name, available: "remote", render })` in [src/app/page.tsx](src/app/page.tsx) that renders a `ToolStatusCard` pill in the chat while the tool runs. When state updates with a new `budget_analysis` / `savings_strategy` / `debt_reduction`, the corresponding card (`src/components/*-card.tsx`) renders in the "Report" tab; the UI auto-switches to that tab when a run that was `running` finishes and a report exists.

**Expense category normalization.** User-provided expense keys (from chat, e.g. "rent", "groceries") are normalized to a fixed set of canonical categories (`CANONICAL_EXPENSE_CATEGORIES` in `agent/main.py`, mirrored as `EXPENSE_CATEGORIES` in `src/lib/types.ts`) via `_normalize_category`/`_EXPENSE_ALIASES`. The system prompt also tells the LLM to prefer canonical names directly, so alias matching is a backstop, not the primary path.

## Docker

`docker/Dockerfile.agent` and `docker/Dockerfile.app` build the agent and UI as separate images; `docker-compose.test.yml` wires them together with `ghcr.io/copilotkit/aimock` as a mock LLM fixture server for the UI's own calls (fixtures in `fixtures/default.json`). Note the Google GenAI SDK talks to `generativelanguage.googleapis.com` directly and does not honor a custom endpoint, so aimock cannot intercept the agent's Gemini calls — a real `GOOGLE_API_KEY` is still needed for the agent service even in this test setup.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
