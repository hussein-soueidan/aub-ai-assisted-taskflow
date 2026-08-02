# Decision: Keep Final Release Engineering Small and Verifiable

## Context

The Task Tracker already contains its required product features and 42 passing
tests. The final project asks for teammate-maintainable release evidence without
turning the course app into a new product or hiding environment limitations.

## Decision

Use one GitHub Actions workflow with separate pytest and container-smoke jobs,
and package only the FastAPI backend in a multi-stage, non-root Docker image.
Keep the static frontend as the existing local-server workflow. Protect `app/`
and `frontend/`; final-project changes belong in release configuration and docs.

## Alternatives considered

- A single CI job: rejected because separating tests from the container smoke
  test makes failures easier to diagnose and proves both contracts independently.
- A development-style one-stage image with `--reload`: rejected because it
  carries unnecessary build state and does not represent a stable runtime.
- Bundling a web server for the frontend: rejected as new delivery scope; the
  final brief requires container health for the app, not a production web stack.
- Claiming local Docker success from static inspection: rejected because Docker
  is not installed on this workstation.

## Trade-offs

The image is small and its responsibility is clear, but a teammate still runs
the frontend separately. GitHub Actions provides reproducible container evidence,
but it does not erase the recorded lack of a local Docker run. Pinned Python and
read-only workflow permissions reduce ambiguity without pretending dependencies
are fully supply-chain hardened.

## Consequences

Every push and pull request runs pytest and a real container smoke check. The
container runs as `app`, exposes only port 8000, and copies no course evidence or
local environment files. README commands distinguish the backend container from
the static frontend.

## Open questions

- Should a future production version serve the frontend from a separate image or
  managed static host?
- Should Python base images and actions be pinned to immutable digests/SHAs under
  a team dependency-update policy?
- What authentication and persistence architecture would be required before any
  deployment beyond local/course use?

I would do this differently in a team environment by confirming the supported
local container runtime at project kickoff, so local and CI Docker evidence can
be collected in the same release cycle.
