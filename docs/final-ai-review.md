# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes.
- Docs-first/read-first guardrail included: yes.
- Unexpected `app/`/`frontend/` edits rule included: yes.
- Business rules, verification expectations, and secret/destructive-action
  boundaries included: yes.

## AI code review mini-log

Review target: the final-project release diff, especially
`.github/workflows/ci.yml`, `Dockerfile`, and `.dockerignore`.

| AI comment | Grade | Reason | Verification or decision |
| --- | --- | --- | --- |
| Limit the workflow token to read-only repository contents. | Useful | CI only checks out code and runs tests; it does not need write permissions. | Added `permissions: contents: read` and inspected the YAML. |
| Test a matrix of several Python versions. | Noise | Multiple versions add time and are outside the brief; the course asks for one explicit version rather than a vague version. | Kept Python 3.11, then retained the local 3.10.11 result as separate evidence. |
| Unit coverage of `/health` makes a container runtime check unnecessary. | Wrong | A unit test cannot prove the built image starts, publishes port 8000, or runs as the intended user. | Kept the CI Docker build/run, HTTP check, and `whoami` assertion. |

## AI security mini-review

| Finding | File evidence | Grade | Reason | Next action |
| --- | --- | --- | --- | --- |
| Task endpoints have no authentication or authorization. | `app/main.py` exposes CRUD and bulk routes without an auth dependency. | Valid | Intentional for the course, but unsafe if exposed as a production service. | Keep it documented as a scope limit; design auth before deployment. |
| Description, assignee, and total in-memory task count are unbounded. | `app/models.py` has no length limits for description/assignee; `app/storage.py` stores tasks in a process-wide dict. | Valid | A client can consume memory with oversized or repeated requests. | Backlog bounded fields/rate limits; do not expand app scope during finalization. |
| Wildcard CORS methods and headers are automatically a high-severity exposure. | `app/main.py` uses fixed loopback origins, `allow_credentials=False`, and wildcard methods/headers. | Noise | The statement ignores the local-only origin allowlist and course context. It becomes relevant only if deployment assumptions change. | Retain the local-only README warning; re-evaluate before deployment. |
| Dynamic card HTML creates stored XSS. | `frontend/index.html` uses `escapeHtml()` for task-derived title, description, assignee, tags, IDs, and priority before insertion. | False Positive | The first-pass claim did not inspect the escaping helper or trusted enum fields. | No code change; keep escaping in future UI edits. |

## Manual security check

I scanned tracked filenames for `.env`, token, secret, credential, private-key,
and certificate patterns. Only the non-secret `.env.example` is tracked; `.env`
itself is ignored. I also checked every frontend `innerHTML` path that renders
task or saved-view input and confirmed values are escaped before insertion.
Finally, I checked the final Docker build context: application code and installed
dependencies are copied, while Git history, local environments, logs, docs,
tests, PDFs, text submissions, and `.env*` are excluded.

## One AI output I rejected or corrected

I rejected the idea of writing “Docker verified locally” when the `docker`
command was not installed on this workstation. The honest correction is to
record that limitation and make the GitHub Actions container job execute the
actual build, run, `/health`, and non-root checks. I also rejected failure-
swallowing cleanup patterns such as `|| true`; cleanup uses an explicit
container-existence check instead.

## Three AI usage rules

1. Never paste `.env` values, credentials, tokens, private keys, production
   logs, or real customer/personal data into an AI tool.
2. Always verify the boundary cases AI omitted—notably omitted versus explicit
   null—then run focused checks and the full behavior contract.
3. Record AI contributions through the reviewed diff, the evidence command and
   result, and any suggestion I rejected or corrected.

## Ownership statement

I am comfortable submitting this repository because I can trace the application
rules, the facilitator-feedback fix, the test evidence, and every final release
artifact to real files and commands. I inspected the final diff and did not let
release work alter the product code. Where this workstation lacked Docker, I
recorded the limitation instead of inventing evidence and moved the runtime
check into CI. The remaining security findings are explicit scope decisions or
backlog items, not risks hidden behind a claim of production readiness.
