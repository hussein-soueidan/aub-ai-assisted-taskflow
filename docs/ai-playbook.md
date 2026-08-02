# My AI Coding Playbook

## When I reach for AI first

- I use AI to turn a bounded requirement into an end-to-end checklist. That
  helped keep due dates and tags consistent across models, routes, tests, and UI.
- I use a repo-aware agent for CI, Docker, and evidence only after it reads the
  relevant source and project instructions.
- I ask AI for boundary-test ideas, then choose and run the cases myself.

## When I do not reach for AI first

- I inspect the code and exact failure before asking AI to debug. The null-update
  defect showed that a green suite can still miss a contract boundary.
- I do not use AI first when the task contains secrets, production data, unclear
  authorization, or an irreversible external action.
- I slow down when I cannot explain the relevant framework rule; generated code
  I cannot defend is not mine.

## My non-negotiables

- Never paste `.env` contents, API keys, tokens, credentials, private keys,
  production logs, or real customer/personal data.
- Never accept a multi-file diff without reading every changed file.
- Never call work verified without command output or a specific manual check.
  Environment limits belong in the evidence log.

## My review rules

- For APIs, distinguish omitted, null, blank, malformed, valid, and boundary
  values; add a regression test for each confirmed bug.
- Run the narrow test first, then `python -m pytest tests -v`; for UI claims,
  open the app; for containers, build, run, call `/health`, and check the user.
- Grade findings before acting, using cited files or runtime behavior.
- Record what AI proposed, what I rejected or changed, and the evidence.

## What I am still figuring out

- How much infrastructure verification belongs locally versus in CI.
- How a team should record AI contribution without excessive paperwork.
- When a context summary helps and when targeted files are safer.

## Decision Card

- For a new feature I reach for: a repo-aware loop after I write acceptance
  criteria and boundary cases.
- For a code review I reach for: Codex for broad first-pass coverage, followed
  by my own diff, tests, and file-evidence review.
- For debugging I reach for: the exact failing test, response, and traceback,
  then an AI hypothesis I can disprove or confirm.
- For infrastructure I reach for: a repo agent with plan-first edits,
  conservative permissions, and real runtime evidence.
- I will never paste `.env` values, credentials, tokens, private keys,
  production logs, or real customer data into an AI tool.
- My one rule is: AI proposes; I inspect, verify, reject or revise, and own.

Re-read commitment: 2026-09-01 (30 days after final-project evidence).
