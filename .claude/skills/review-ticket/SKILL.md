---
name: review-ticket
description: "Run the full test suite and linter, verify a ticket's acceptance criteria one by one, and check cross-cutting rules (secrets). Use for the stage:review step of the AI factory pipeline."
argument-hint: "<ticket-number>"
user-invocable: true
---

# Review Ticket

## When to Use
Third pipeline stage (`stage:review`), after implementation is green.

## Steps
1. Run the framework's full test suite and linter (commands from [framework-conventions.md](../../rules/framework-conventions.md)). Both must pass before continuing.
2. Re-read the ticket's original acceptance criteria and confirm each one is actually met — don't just trust the checklist, exercise the feature (curl the endpoint, hit the page, run the query).
3. If anything fails: report exactly what's wrong and relabel back to `stage:implement` instead of advancing.
4. If everything passes: relabel the ticket from `stage:review` to `stage:docs`.

## Goal
Nothing reaches the docs/ship stages that hasn't been independently verified against its own acceptance criteria.
