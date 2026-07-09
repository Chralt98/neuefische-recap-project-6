# Branching Rule

Every ticket gets its own branch, for every pipeline stage — including `stage:plan`, since planning can still edit repo files (e.g. appending a finding to `framework-conventions.md`). Never run a pipeline skill for one ticket while checked out on a *different* ticket's branch.

- Branch name: `ticket-<number>-<kebab-case-slug-of-title>` (e.g. `ticket-2-user-authentication-and-profile-management`).
- Before doing any work for a ticket, check `git branch --show-current`:
  - If it already matches this ticket's branch, proceed as-is.
  - Else if this ticket's branch already exists (local or remote), check it out (fetch first if it's remote-only).
  - Else create it fresh off the latest `main` (`git checkout main && git pull && git checkout -b ticket-<n>-<slug>`).
- Leaving a previous ticket's branch mid-work is fine — it's parked, not lost. Check it back out next time that ticket comes up.
- If there are uncommitted changes on the current branch that belong to the ticket being switched away from, commit or stash (`git stash -u`) them first rather than discarding them.

Every pipeline skill (`plan-ticket`, `tdd-implement`, `review-ticket`, `update-docs`, `ship-ticket`) applies this rule at the start of its own run, since each is user-invocable directly and can't rely on `next-ticket` having done it first.
