# Reusable Release Safety Checklist

Use this after product tests are green and before calling a branch release-ready.

## Inputs

- Current branch and clean diff.
- `requirements.txt`, workflow, Dockerfile, `.dockerignore`, README, and tests.
- Real test, HTTP, and container outputs.

## Checks

1. Confirm the intended branch and inspect every changed path.
2. Run the exact documented test command; record failures honestly.
3. Search CI for swallowed failures, skipped tests, vague runtimes, excess
   permissions, and deployment scope.
4. Build/run the image, call `/health`, and verify the runtime user.
5. Confirm `.env*`, Git history, local environments, logs, and personal artifacts
   are not in the build context or tracked files.
6. Follow at least three README claims against source or runtime evidence.
7. Grade AI review/security findings before acting; reject unsupported claims.
8. Stop if application/frontend files changed unexpectedly and require a focused
   explanation plus regression test before proceeding.

## Output

Update `docs/release-evidence.md` with commands, results, links, limitations,
and rejected/corrected suggestions. Never replace missing evidence with a claim.
