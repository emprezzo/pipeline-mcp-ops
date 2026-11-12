---
name: guide-pipeline-mcp-development
description: Guide a developer familiar with Docker through uv, MCP development, tests, GitHub Actions, and container delivery in small verified steps.
---

# Pipeline MCP development guide and ongoing checklist

## Instructions for the guiding agent

The user knows Docker and is learning uv and GitHub Actions. Explain each new concept using this project, then help them do one small step. uv manages Python dependencies and execution; Docker packages the runtime; Actions automates checks and delivery. Keep stdio MCP distinct from the separate HTTP demo.

Read `AGENTS.md` and inspect current files before giving commands. This checklist starts from the repository's initial demonstration; it is a plan, not a claim that steps have passed. Recheck older observations as the code evolves. Do not redo completed work without a reason.

- Work through numbered steps in order. Present the current step, why it matters, exact commands or edits, and its done-check. Default to one step per interaction unless the user asks to batch work.
- Each step targets 5–25 minutes, including verification. These are estimates, not guarantees. At 20 minutes without a clear finish, split the step instead of extending the session.
- If step 23 stalls, keep its original number and add `23a`, `23b`, etc. directly below it. Give every child a narrow action and a done-check; check off the parent only after all children and the parent's check pass. Never renumber later steps.
- When the user pastes a stalled step, ask only for missing context needed to diagnose it: command, sanitized error, and expected versus observed behavior. Split investigation from implementation. Never ask for credentials in chat.
- Ask the user when an actual product choice cannot be inferred, especially which pipeline provider to integrate. Continue independent work while awaiting an answer. Do not invent provider endpoints or permissions.
- Mark `[x]` only with observed evidence or the user's explicit report of that evidence. Record a brief date/result beside completed items. Failed, blocked, skipped, and deferred are distinct from done.
- A dependency blocked by an external action remains unchecked. Record who needs to act and the exact action. Continue only steps that do not depend on it.
- Do not implement this whole plan just because this skill is invoked. Guide the requested step; preserve the user's learning pace. Do not push, publish images, merge, or deploy without authorization for that action.
- Keep changes focused, preserve user edits, and never weaken tests, TLS, or artifact verification to obtain a passing check. Use the existing checkout; do not create worktrees unless requested.
- Finish each session by updating the session notes and naming the next unchecked step. Explain any failed check plainly.

## Progress notes

Current step: 01 (update as work progresses).

Session template: `Date | steps completed | evidence | blocker | next step`.

No steps are checked below solely because setup previously ran in another environment.

## Milestone A: understand and reproduce the current project

- [ ] 01 (5m) Inspect `git status --short` and read `AGENTS.md`. **Done:** existing edits are identified and will be preserved.
- [ ] 02 (10m) Map `server.py`, `app.py`, package initializers, manifests, and Dockerfile. **Done:** explain which file serves MCP and which serves the HTTP demo.
- [ ] 03 (5m) Explain uv versus Docker versus Actions in your own words. **Done:** identify which tool installs packages, isolates the deployed runtime, and runs CI.
- [ ] 04 (10m) Check Python and uv versions against `.python-version`. **Done:** Python 3.12 and uv are usable, or a concrete installation prerequisite is recorded.
- [ ] 05 (10m) Run `uv sync --frozen` from the repository root. **Done:** installation succeeds without changing `uv.lock`.
- [ ] 06 (5m) Run `uv run --frozen python -c "import sys; print(sys.executable)"`. **Done:** it uses the project's virtual environment; explain why activation is optional.
- [ ] 07 (10m) Compare `pyproject.toml`, `uv.lock`, and `requirements.txt`. **Done:** distinguish declared requirements from locked versions and record uv as the primary workflow.
- [ ] 08 (10m) Run `uv run --frozen ruff check src`. **Done:** record its actual exit status and any findings.
- [ ] 09 (10m) Run `uv run --frozen mypy src`. **Done:** record its actual exit status and any findings.
- [ ] 10 (10m) Run `uv build --out-dir /tmp/pipeline-mcp-ops-dist`. **Done:** this run produces a wheel and source archive.
- [ ] 11 (10m) Start the HTTP demo and request it locally. **Done:** receive the expected running JSON and stop the process you started.
- [ ] 12 (10m) Trace the MCP tools and sample records. **Done:** explain the two pipeline results, unknown-ID error, and input constraints.

## Milestone B: make project usage clear

- [ ] 13 (10m) Reproduce the console entry-point failure with `uv run --frozen pipeline-ops-mcp`. **Done:** identify its import target and actual missing callable; if already fixed, verify it instead.
- [ ] 14 (15m) Add a package `main()` that starts the MCP server. **Done:** the console entry point resolves to the real server, not the greeting.
- [ ] 15 (10m) Align module and console startup without duplicate implementations. **Done:** both paths call the intended startup function; protocol verification follows in milestone D.
- [ ] 16 (10m) Review the unrelated greeting in `src/__init__.py`. **Done:** retain or remove it deliberately after checking references and package contents.
- [ ] 17 (15m) Write README purpose, layout, and uv setup instructions. **Done:** a new reader can identify the project and install it.
- [ ] 18 (10m) Document stdio startup separately from the HTTP demo. **Done:** README explains that stdio does not require a published port.
- [ ] 19 (10m) Decide whether `requirements.txt` has a supported consumer. **Done:** retain a documented synchronization method or remove the redundant file intentionally.
- [ ] 20 (10m) Review generated/local file ignores. **Done:** `.venv`, caches, credentials, and build outputs will not be committed accidentally.
- [ ] 21 (15m) Run lint, typing, and build after startup edits. **Done:** checks pass or any failure is diagnosed before continuing dependent work.

## Milestone C: add focused Python tests

- [ ] 22 (10m) Add `tests/` and one test for sorted pipeline IDs. **Done:** `uv run --frozen pytest -q` executes and passes a real test.
- [ ] 23 (10m) Test the successful sample pipeline result. **Done:** assert its ID, status, row count, and absent error code.
- [ ] 24 (10m) Test the failed sample pipeline result. **Done:** assert its failed status and `UPSTREAM_TIMEOUT` code.
- [ ] 25 (10m) Test an unknown well-formed ID. **Done:** assert the intended `ToolError` and useful message.
- [ ] 26 (15m) Test the response model's allowed statuses and optional error field. **Done:** representative valid and invalid model data behave as intended.
- [ ] 27 (10m) Check test independence. **Done:** tests do not leak mutations into shared sample records and pass in repeated runs.
- [ ] 28 (15m) Include tests in lint and applicable typing checks. **Done:** check results cover both implementation and tests without blanket suppressions.
- [ ] 29 (10m) Document the test command and its scope. **Done:** README distinguishes Python tests from protocol tests.

## Milestone D: verify the actual MCP connection

- [ ] 30 (15m) Create an async stdio client test with bounded timeouts and cleanup. **Done:** it launches the server and initializes a real MCP session.
- [ ] 31 (10m) Assert tool discovery through that session. **Done:** both expected tool names appear.
- [ ] 32 (10m) Call `list_pipelines` through MCP. **Done:** assert the returned IDs from the protocol result.
- [ ] 33 (10m) Call the successful pipeline through MCP. **Done:** assert structured response values and no tool error.
- [ ] 34 (10m) Call the failed pipeline through MCP. **Done:** its business status is failed while the tool invocation itself succeeds.
- [ ] 35 (10m) Call an unknown ID through MCP. **Done:** the response is a tool error rather than a crashed server.
- [ ] 36 (10m) Call an invalid ID such as `INVALID`. **Done:** protocol input validation rejects it.
- [ ] 37 (15m) Add boundary cases for empty, too-long, and missing IDs. **Done:** each is rejected at the MCP boundary.
- [ ] 38 (15m) Exercise the console entry point through the client. **Done:** the installed command initializes and completes a tool call.
- [ ] 39 (10m) Repeat the protocol suite and inspect cleanup. **Done:** no server subprocess remains after success or test failure.
- [ ] 40 (10m) Review stdout and logging. **Done:** diagnostics use stderr and startup emits no stray protocol-breaking stdout.

## Milestone E: build a usable development container

- [ ] 41 (10m) Inspect the Dockerfile against actual source paths. **Done:** record the wrong COPY path and missing installation/startup pieces, or verify prior fixes.
- [ ] 42 (10m) Check Docker availability. **Done:** `docker version` reaches a daemon, or its specific external prerequisite is recorded.
- [ ] 43 (10m) Choose and document pinned Python and uv build inputs. **Done:** explain the version policy and update process.
- [ ] 44 (15m) Add a dependency layer using manifest and lockfile first. **Done:** Docker installs locked runtime dependencies without development tools.
- [ ] 45 (15m) Copy and install the package after the dependency layer. **Done:** the image contains an importable installed application.
- [ ] 46 (10m) Set the real MCP startup command and non-root runtime user. **Done:** the final image configuration launches the server as that user.
- [ ] 47 (10m) Review `.dockerignore`. **Done:** credentials, `.git`, local environments, and caches stay outside build context.
- [ ] 48 (20m) Build a local image. **Done:** `docker build -t pipeline-ops-mcp:dev .` succeeds with verification enabled.
- [ ] 49 (10m) Inspect dependencies and identity inside the image. **Done:** runtime imports work and the process user is non-root.
- [ ] 50 (15m) Adapt the protocol client to launch `docker run --rm -i pipeline-ops-mcp:dev`. **Done:** containerized MCP initialization succeeds without a TTY or published port.
- [ ] 51 (10m) Call a pipeline tool through the container. **Done:** its structured result matches the local server.
- [ ] 52 (10m) Verify container exit and cleanup. **Done:** closing the client leaves no running smoke-test container.
- [ ] 53 (15m) Rebuild without changing dependencies. **Done:** inspect build output and explain which dependency layers were reused.
- [ ] 54 (10m) Document image build and client launch commands. **Done:** README describes stdio attachment and separates the HTTP demo.

## Milestone F: learn GitHub Actions with useful CI

- [ ] 55 (10m) Identify repository default branch and Actions settings. **Done:** record actual branch and workflow access; do not assume permissions.
- [ ] 56 (10m) Sketch event → job → step → command. **Done:** map the local checks to one small CI job.
- [ ] 57 (15m) Create `.github/workflows/ci.yml` with PR and default-branch push triggers. **Done:** trigger configuration matches the actual branch.
- [ ] 58 (10m) Add checkout, Python 3.12, and pinned uv setup. **Done:** actions use reviewed immutable revisions with readable version comments.
- [ ] 59 (10m) Add locked dependency installation. **Done:** CI runs `uv sync --frozen` in the correct directory.
- [ ] 60 (10m) Add lint and typing steps. **Done:** CI runs the same source/test checks used locally.
- [ ] 61 (10m) Add tests and package build. **Done:** test failures propagate and the workflow does not accept a zero-test run as coverage.
- [ ] 62 (10m) Add minimal permissions, a job timeout, and cancellation of obsolete runs. **Done:** CI needs read-only repository access and cannot hang indefinitely.
- [ ] 63 (10m) Review workflow YAML and commands locally. **Done:** paths, action inputs, shell commands, and dependency order are consistent.
- [ ] 64 (10m) Prepare a branch and PR description. **Done:** diff contains only intended changes and description states validation and limitations.
- [ ] 65 (10m) With user authorization, push and open the PR. **Done:** GitHub has the expected branch/PR; never count a local workflow file as an executed run.
- [ ] 66 (15m) Read the first Actions run. **Done:** record run URL and real step results; split any debugging into lettered substeps.
- [ ] 67 (15m) Confirm CI detects a controlled test failure on the development branch. **Done:** the test job fails, the temporary failure is reverted, and the next run passes.
- [ ] 68 (15m) Add a separate Docker build check. **Done:** Actions builds the runtime image without publishing it.
- [ ] 69 (15m) Run the existing container protocol smoke check in CI. **Done:** CI verifies a real MCP call inside its built image.
- [ ] 70 (10m) Document CI commands and branch protection recommendations. **Done:** required check names are known; settings changes are only applied with authorization.

## Milestone G: add one real read-only pipeline integration

- [ ] 71 (15m) Ask which provider and one read-only use case to support. **Done:** name the provider, intended user, and exact status question; do not guess.
- [ ] 72 (15m) Read provider documentation for that one operation. **Done:** record endpoint/API method, authentication, response shape, and limits without copying credentials.
- [ ] 73 (10m) Identify network and credential prerequisites. **Done:** check available bindings by name/presence and record any required secure configuration action.
- [ ] 74 (15m) Define a small provider interface around status lookup/listing. **Done:** sample and future real providers have explicit inputs, outputs, and errors.
- [ ] 75 (15m) Wrap existing sample records behind that interface. **Done:** existing tests preserve observable demo behavior.
- [ ] 76 (15m) Add explicit demo/real configuration selection. **Done:** default tests remain offline and missing real configuration yields a clear error.
- [ ] 77 (15m) Add the minimal provider client dependency if needed. **Done:** manifest and lock changes are intentional and tests still collect.
- [ ] 78 (20m) Implement one read-only provider request with an injected client. **Done:** a mocked success response maps to the internal model.
- [ ] 79 (15m) Test provider status mapping. **Done:** known and unexpected statuses have deliberate behavior.
- [ ] 80 (15m) Test missing records and authorization failures. **Done:** user-facing errors are useful and do not expose credentials or raw sensitive bodies.
- [ ] 81 (15m) Set and test connection/request timeouts. **Done:** a simulated timeout terminates within the intended budget with a useful error.
- [ ] 82 (15m) Handle rate limiting according to provider guidance. **Done:** retries, if needed, are bounded and a mocked rate-limit response has a tested outcome.
- [ ] 83 (15m) Wire the provider into MCP tools. **Done:** an offline protocol test exercises the provider boundary and response mapping.
- [ ] 84 (15m) Add configuration examples using placeholders only. **Done:** README explains variables, read-only scopes, and demo mode without secret values.
- [ ] 85 (20m) If prerequisites are available, perform one authorized live read. **Done:** expected status is returned; otherwise record the exact blocker and keep this unchecked.
- [ ] 86 (15m) Review logs and exception messages for the integration. **Done:** tests confirm representative secrets are absent from captured output.
- [ ] 87 (20m) Run local and container regression checks. **Done:** demo remains usable and real-provider tests stay deterministic/offline by default.

## Milestone H: publish a versioned image when wanted

- [ ] 88 (10m) Decide whether image distribution is needed now. **Done:** user explicitly chooses to proceed or records this milestone as deferred, without checking unrun publication steps.
- [ ] 89 (10m) Choose GHCR image name, visibility, and tag policy. **Done:** version tags and commit references identify an exact build; private-image pull requirements are documented.
- [ ] 90 (15m) Create a tag-triggered publishing workflow. **Done:** publishing is separate from untrusted PR checks and build inputs/actions are pinned.
- [ ] 91 (15m) Add minimal GHCR permissions and supported authentication. **Done:** package write access is restricted to the publishing job; no token values are embedded.
- [ ] 92 (15m) Require verification before publishing. **Done:** the workflow dependency graph blocks a publish after failed tests or container checks.
- [ ] 93 (10m) Add source, revision, and version image metadata. **Done:** planned metadata ties an image back to the repository commit.
- [ ] 94 (15m) Review the release diff and prepare release notes. **Done:** exact tag, image target, checks, and known limitations are reviewable before release authorization.
- [ ] 95 (20m) After explicit release authorization, create/push the release tag. **Done:** publishing succeeds and its actual registry digest is recorded.
- [ ] 96 (15m) Pull the published image by digest and smoke-test MCP. **Done:** a real tool call succeeds from the registry artifact.
- [ ] 97 (10m) Document the tested image/client configuration. **Done:** a reader can pull and run that version, including authentication instructions if private.

## Milestone I: consolidate and choose the next increment

- [ ] 98 (15m) Review README, `AGENTS.md`, and this guide against current behavior. **Done:** resolved defects are no longer described as current and commands match the project.
- [ ] 99 (20m) Reproduce setup in a separate clean temporary copy without altering the working checkout. **Done:** locked install and documented checks work without relying on the existing `.venv`.
- [ ] 100 (15m) Review the smallest outstanding reliability issue. **Done:** write one specific next task with a reproducible problem and done-check.
- [ ] 101 (15m) Choose the next feature with the user. **Done:** select one of another read-only tool, improved provider reliability, or remote HTTP transport based on a real need.
- [ ] 102 (15m) Break that feature into lettered or newly appended steps. **Done:** each step has one observable outcome and a target below 30 minutes; existing numbers remain stable.

## Stalled-step template

Copy the relevant checklist item plus:

```text
Step number:
Command or edit attempted:
Expected result:
Actual result / sanitized error:
Time spent:
Please split this into <number>a, <number>b, etc., each under 30 minutes
with a clear done-check. Preserve later step numbers.
```

When a step is too broad, the first child should reproduce or isolate the blocker, the next should make the smallest supported correction, and the last should rerun the original done-check. Add more children as needed; do not squeeze an unknown investigation into a promised time limit.
