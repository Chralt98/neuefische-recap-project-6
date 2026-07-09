---
name: plan-ticket
description: "Turn a ticket's description into a short, concrete implementation checklist, researching unfamiliar framework mechanics first if needed. Use for the stage:plan step of the AI factory pipeline."
argument-hint: "<ticket-number>"
user-invocable: true
---

# Plan Ticket

## When to Use
First pipeline stage for a ticket (`stage:plan`). Runs before any code is written.

## Steps
1. Read the ticket body via `gh issue view <ticket-number>`.
2. Apply [branching.md](../../rules/branching.md): check out this ticket's own branch (creating it off latest `main` if it doesn't exist yet) before touching any repo files.
3. If the ticket touches framework mechanics not yet documented in [framework-conventions.md](../../rules/framework-conventions.md) (e.g. a new generator command, a new ORM aggregation, a new auth hook), research the framework's own docs and append the finding to that rules file so later tickets don't re-research it.
4. Write a short checklist as a comment on the ticket: the entities/files that will be touched, the test cases that will prove the acceptance criteria, and any open questions.
5. Relabel the ticket from `stage:plan` to `stage:implement`. Leave the board card in "In Progress".

## Guidance
- Keep the checklist short (aim for 3-8 bullet points) — this is a plan, not a spec.
- If the ticket is ambiguous (e.g. missing acceptance criteria), ask the user before relabeling rather than guessing.

## Goal
A ticket that any pipeline stage — including a future session — can pick up with no missing context.
