# Security Review

This is a read-only Module 5 review. It does not claim production readiness and
did not trigger application changes.

## Findings and grades

| ID | Severity | Finding and evidence | Grade | Decision |
| --- | --- | --- | --- | --- |
| S1 | High outside course scope | `app/main.py` protects no task route with authentication or authorization. | Valid | Intentional learning scope; block any public deployment until access control is designed and tested. |
| S2 | Medium | `description` and `assignee` have no length limit in `app/models.py`, and `app/storage.py` has no task-count/rate bound. | Valid | Add bounded input and request controls in a future hardening change, not during docs-first finalization. |
| S3 | Low in current setup | CORS allows all methods/headers but only four explicit loopback origins and no credentials. | Noise as a current finding | Keep local-only; re-review if deployed or if origins become configurable. |
| S4 | Claimed high | Frontend card rendering allegedly inserts stored values without escaping. | False Positive | `escapeHtml()` covers task-derived values before `innerHTML`; no patch needed. |

## Manual findings

- The tracked-file scan found no secret/token/private-key material. The only
  environment file is `.env.example`, containing non-secret sample values.
- API errors use controlled FastAPI/Pydantic details; the checked routes do not
  deliberately return raw tracebacks.
- The earlier explicit-null bug is now protected by two regression tests and
  storage revalidation; required fields cannot be poisoned through PATCH.
- Docker runs as UID/GID 10001 and its context excludes `.env*`, Git history,
  virtual environments, logs, docs, tests, PDFs, and local text submissions.

## Reconciliation

| Agreement | AI-only | You-only |
| --- | --- | --- |
| No authentication is a real production risk but an intentional course limit. | Unbounded description/assignee and task count deserve a future availability review. | The high-severity CORS framing ignored fixed loopback origins; the XSS claim ignored `escapeHtml()`. |

## Top-three backlog

| Rank | Item | Owner | Next action |
| --- | --- | --- | --- |
| 1 | Authentication and authorization before deployment | Backend/project owner | Write a threat model and access-control acceptance criteria before implementation. |
| 2 | Bound request size and task growth | Backend | Choose description/assignee limits, add rate/request-size controls, and add boundary tests. |
| 3 | Dependency update policy | DevOps/project owner | Add a scheduled dependency review and record upgrade/test evidence; do not auto-merge blindly. |
