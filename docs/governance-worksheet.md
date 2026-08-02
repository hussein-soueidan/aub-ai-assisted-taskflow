# Governance Worksheet

## What I shared with AI

| Item shared | Risk | Reason | Safer future version |
| --- | --- | --- | --- |
| Public course Task Tracker code and folder structure | Low | Toy/course code with no secrets or customer data. | Share only the files required for the bounded task. |
| Pytest failures and local HTTP responses | Low | Synthetic tasks and framework output; no production data. | Remove absolute paths and unrelated environment details when they are not needed. |
| Assignment briefs and course notes | Low | Course material used as the source of truth. | Quote only the relevant requirement when a full document is unnecessary. |
| GitHub repository metadata | Low | Public repository and branch names. | Do not include tokens, credential-helper output, or private-repo metadata. |

No `.env` values, credentials, tokens, private keys, production logs, or real
customer data were intentionally shared.

## What I received from AI

| Output | What I accepted | What I corrected or rejected | Verification |
| --- | --- | --- | --- |
| Due-date, tag, bulk, saved-view, and UI changes | Bounded end-to-end implementation | Rejected database/framework expansion. | Focused tests, full suite, browser checks, and break tests. |
| Explicit-null facilitator fix | Schema rejection plus storage revalidation | Corrected the earlier omitted-vs-null oversight. | Two regressions and 42-test suite. |
| CI and Docker release artifacts | Pinned CI, non-root container, runtime smoke test | Rejected swallowed failures and unsupported local-Docker claims. | YAML/Docker review plus GitHub Actions evidence. |
| Security review | File-grounded risks | Downgraded generic CORS advice and rejected unsupported XSS. | Manual source and tracked-secret scan. |

## Line-by-line ownership trace

Trace target: `TaskUpdate.reject_null_for_required_fields` in `app/models.py`.

| Line or construct | What it does | Why it is present | What would break without it |
| --- | --- | --- | --- |
| Multi-field `field_validator` | Applies one rule to every required update field. | PATCH fields must be optional to omit but not nullable when supplied. | Explicit null could enter required task state. |
| `mode="before"` | Sees raw JSON input before enum/string parsing. | Null must be rejected before later validators accept the optional type. | `None` would bypass title cleanup and status parsing. |
| `ValidationInfo` | Supplies the current field name. | The error identifies the actual field. | Validation still could fail, but feedback would be less precise. |
| `if value is None` | Distinguishes explicit null from omission. | Validators run for supplied values; an omitted field keeps its default. | Omitted and null would remain conflated. |
| Return unchanged value | Lets Pydantic and field-specific validators continue. | This validator enforces only nullability. | It could accidentally replace or bypass valid input. |

I own this block because I can explain the Pydantic timing, the PATCH contract,
the prior failure mode, and the tests that demonstrate the difference.
