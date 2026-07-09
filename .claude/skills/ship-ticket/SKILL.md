---
name: ship-ticket
description: "Commit, push, and open a PR for a reviewed and documented ticket, checking off its completed task checkboxes, then move its board card to Review. Use for the stage:ship step of the AI factory pipeline."
argument-hint: "<ticket-number>"
user-invocable: true
---

# Ship Ticket

## When to Use
Final pipeline stage (`stage:ship`), after review and docs are done.

## Steps
1. Commit the ticket's changes with a message referencing the ticket (e.g. `feat: add goal CRUD (#12)`).
2. Push the branch and open a PR with `gh pr create`, linking the ticket in the PR body (`Closes #12`).
3. Check off the issue's task checkboxes for whatever was actually completed (see [checklist.md](../../rules/checklist.md)) via `gh issue edit --body`. Leave any task that wasn't really done unchecked and flag it instead of ticking it off.
4. Remove the `stage:ship` label.
5. Move the board card to "Review". If the board has no "Review" status column, create one (between "In Progress" and "Done") and use it from then on.
6. Report the PR URL to the user.

## After merge
Never move a card to "Done" as part of this skill — opening a PR is not enough to call a ticket done. This board has the built-in `Pull request merged` and `Item closed` workflows enabled, so GitHub itself flips the card to Done once a human merges the PR (which also closes the linked issue via `Closes #12`). Leave that transition to GitHub's automation; don't touch the Status field after step 4.

If a card ever ends up in Done without its PR being merged (e.g. moved there by mistake), reopen the linked issue with `gh issue reopen` — GitHub's `Item closed` workflow will have auto-closed it when the status changed, and closing it back out won't happen on its own.

## Goal
Every shipped ticket leaves a clean paper trail: commit → PR (card in Review) → merge → board card in Done.
