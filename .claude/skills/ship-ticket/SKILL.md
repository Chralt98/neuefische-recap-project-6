---
name: ship-ticket
description: "Commit, push, and open a PR for a reviewed and documented ticket, then move its board card to Done. Use for the stage:ship step of the AI factory pipeline."
argument-hint: "<ticket-number>"
user-invocable: true
---

# Ship Ticket

## When to Use
Final pipeline stage (`stage:ship`), after review and docs are done.

## Steps
1. Commit the ticket's changes with a message referencing the ticket (e.g. `feat: add goal CRUD (#12)`).
2. Push the branch and open a PR with `gh pr create`, linking the ticket in the PR body (`Closes #12`).
3. Remove the `stage:ship` label and move the board card to "Review" (or "Done" if the pipeline has no separate human PR-review column).
4. Report the PR URL to the user.

## Goal
Every shipped ticket leaves a clean paper trail: commit → PR → closed issue → board card in the right column.
