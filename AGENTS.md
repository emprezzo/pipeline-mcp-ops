# Repository guide

## Layout

This is a small Python MCP demonstration with in-memory pipeline data; it does not connect to production pipeline services.

- `src/pipeline_ops_mcp/server.py`: stdio MCP server, tool definitions, Pydantic response model, and sample pipeline records.
- `src/pipeline_ops_mcp/app.py`: separate standard-library HTTP demonstration on port 8000.
- `src/pipeline_ops_mcp/__init__.py`: package initializer, currently empty.
- `src/__init__.py`: contains a greeting `main`; it is outside the installed package.
- `pyproject.toml`: project metadata, dependencies, dev tools, build backend, and console entry point.
- `uv.lock`: exact dependency versions; `.python-version` selects Python 3.12.
- `requirements.txt`: alternative dependency list; the verified workflow uses `pyproject.toml` and `uv.lock`.
- `Dockerfile`: container scaffold with known limitations below. `README.md` is currently empty.
- There is currently no test directory or CI configuration.

## Setup and execution

Run commands from the repository root with Python 3.12 and `uv` available:

```bash
uv sync --frozen
.venv/bin/python -m pipeline_ops_mcp.server
```

The MCP process communicates over stdio and should normally be launched by an MCP client. It is not an HTTP service. Keep protocol stdout free of debug prints; send diagnostics to stderr.

For the independent HTTP demo:

```bash
.venv/bin/python src/pipeline_ops_mcp/app.py
```

From another terminal, `curl --fail http://127.0.0.1:8000` should return JSON with `message` equal to `Hello from Podman!` and `status` equal to `running`. Stop processes you start when they are no longer needed. Neither demo requires credentials.

Known repository defects: the `pipeline-ops-mcp` console entry point imports a missing `pipeline_ops_mcp.main`; use the module command above. The Dockerfile copies nonexistent `src/app.py` and does not install MCP dependencies. Do not assume container execution works. Fix these when relevant to the requested task, and update this guide after verifying the fix.

## Build and checks

```bash
.venv/bin/ruff check src
.venv/bin/mypy src
uv build --out-dir /tmp/pipeline-mcp-ops-dist
```

These checks passed during onboarding. If adding tests under `tests/`, include that directory in applicable lint and type checks. Use `.venv/bin/pytest` to run tests once present; a zero-test run does not demonstrate readiness. Do not invent a passing test count or describe unrun checks as passed.

For changes to MCP behavior, perform a protocol smoke check using `mcp.client.stdio.stdio_client`, `StdioServerParameters`, and `ClientSession` to launch `.venv/bin/python -m pipeline_ops_mcp.server`, then verify:

1. Session initialization succeeds and tool discovery includes `list_pipelines` and `get_pipeline_status`.
2. `list_pipelines` returns the two sample IDs in sorted order.
3. `software_inventory_daily` returns `failed` with `UPSTREAM_TIMEOUT`; `database_performance_daily` returns `success` with 125,000 rows.
4. An unknown well-formed ID returns a tool error, and an invalid ID such as `INVALID` is rejected by validation.

Update expected outcomes deliberately when the requested behavior changes. Direct Python function calls alone do not verify the stdio transport. For HTTP changes, start the demo and verify its actual response, not just an open port.

## Engineering conventions and PR expectations

- Follow the existing Python style: four-space indentation, descriptive snake_case names, type annotations, and concise tool docstrings. Use Pydantic models and `Annotated`/`Field` for structured validation.
- Preserve deterministic tool output, explicit status values, and useful errors. Cover changed success paths, invalid inputs, and missing records with meaningful tests where appropriate.
- Keep changes focused on the requested behavior. Avoid unrelated refactors, new services, and dependency churn.
- Treat `pyproject.toml` and `uv.lock` as the primary dependency workflow. When dependencies must change, update the lockfile intentionally with uv and explain the reason. Do not silently allow `requirements.txt` to contradict the intended installation workflow.
- PR descriptions should state the problem, resulting behavior, relevant validation commands and outcomes, and any remaining limitations. Call out dependency or public tool-schema changes. No repository-specific PR template or commit-message standard is currently defined.

## Constraints and completion

- Use the existing checkout in isolated cloud tasks; create a Git worktree only when explicitly requested.
- Preserve user changes. Do not reset, delete, or overwrite unrelated files, commit generated artifacts or local environments, or expose credentials in files, logs, or PRs.
- Keep TLS, package signatures, and artifact verification enabled. Reuse platform-provided authentication rather than extracting credentials.
- During environment-only setup, leave tracked application code, tests, manifests, and lockfiles unchanged; use local configuration or report required code fixes separately. This restriction does not prohibit code changes explicitly requested in a development task.
- Work is done when the requested behavior is implemented, relevant checks have run successfully (or failures are diagnosed and reported), documentation reflects changed usage, and `git diff`/`git status --short` show only intended changes. Distinguish repository defects from environment failures and disclose skipped or unrun checks.
