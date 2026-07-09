---
name: update-docs
description: "Update CLAUDE.md with any new commands or architecture changes introduced by a reviewed ticket. Use for the stage:docs step of the AI factory pipeline."
argument-hint: "<ticket-number>"
user-invocable: true
---

# Update Docs

## When to Use
Fourth pipeline stage (`stage:docs`), after a ticket has passed review.

## Steps
1. Apply [branching.md](../../rules/branching.md): check out this ticket's own branch (it should already exist) before doing anything else.
2. Diff the ticket's branch against main to see what actually changed.
3. If the ticket introduced a new command (setup, migration, test, run), add it to `CLAUDE.md`'s command list.
4. If the ticket introduced a new architectural piece (new entity, new integration, new pipeline stage, new convention), add a short note to `CLAUDE.md`'s architecture section.
5. If nothing doc-worthy changed, say so explicitly rather than padding `CLAUDE.md` with filler.
6. Relabel the ticket from `stage:docs` to `stage:ship`.

## Goal
`CLAUDE.md` stays a truthful, current map of the project — never stale, never bloated.
