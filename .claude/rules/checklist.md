# Checklist Rule

A ticket's task checkboxes (`- [ ] ...` in the issue body) are a record of what was actually done, not just a planning artifact. Every checkbox for a task that has been completed must be checked off (`- [x] ...`) *at the point it's actually completed* — via `gh issue edit --body` — not deferred to a later pipeline stage. An issue sitting at `stage:review` or `stage:docs` with unchecked boxes for work that's already done is a false paper trail, same as one closed that way.

- `tdd-implement` is where most task checkboxes get checked off, since that's the stage where implementation work (and any non-test tasks like README updates or manual verification) actually happens — check a box off as soon as its task is done, not in a batch at the end.
- `ship-ticket` does a final sweep before opening the PR, catching anything genuinely missed earlier — it should rarely find unchecked-but-done boxes if earlier stages kept up.
- If a listed task was *not* actually done, leave its box unchecked and flag it rather than checking it off to make the ticket look finished.
