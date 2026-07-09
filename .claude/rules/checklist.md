# Checklist Rule

A ticket's task checkboxes (`- [ ] ...` in the issue body) are a record of what was actually done, not just a planning artifact. Every checkbox for a task that has been completed must be checked off (`- [x] ...`) by the time the ticket ships — an issue closed with unchecked boxes is a false paper trail.

`ship-ticket` checks off any remaining completed-task checkboxes in the issue body (via `gh issue edit --body`) before opening the PR. If a listed task was *not* actually done, leave its box unchecked and flag it rather than checking it off to make the ticket look finished.
