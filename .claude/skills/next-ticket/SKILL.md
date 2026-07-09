---
name: next-ticket
description: "Pick up the next actionable ticket from the GitHub project board and run the pipeline stage it currently needs. Use when the user says 'next ticket', 'work the board', or wants the AI factory loop advanced by one step."
argument-hint: "[ticket-number] (optional — defaults to the highest-priority ticket in Todo/In Progress)"
user-invocable: true
---

# Next Ticket

## When to Use
Invoked to advance the AI factory pipeline by exactly one stage, for exactly one ticket. This is the loop the pipeline runs on — one call = one stage, then stop for human review.

## Stage labels
Every ticket carries exactly one `stage:*` label at a time, one of:
`stage:plan` → `stage:implement` → `stage:review` → `stage:docs` → `stage:ship` → (label removed, ticket closed/moved to Done).
A newly created ticket with no `stage:*` label is treated as `stage:plan`.

## Steps
1. If an argument was given, look up that ticket via `gh issue view <n>`. Otherwise list open issues with `gh issue list --label stage:plan,stage:implement,stage:review,stage:docs,stage:ship` and pick the one with the highest board priority / lowest position in the "Todo" or "In Progress" column (`gh project item-list`).
2. If the ticket has no `stage:*` label yet, add `stage:plan` and move its board card to "In Progress".
3. Apply [branching.md](../../rules/branching.md) so the correct ticket branch is checked out before invoking the stage skill (each stage skill also applies this rule itself, so this is a belt-and-suspenders check here).
4. Read the ticket's current `stage:*` label and invoke exactly the matching skill via the Skill tool:
   - `stage:plan` → `plan-ticket`
   - `stage:implement` → `tdd-implement`
   - `stage:review` → `review-ticket`
   - `stage:docs` → `update-docs`
   - `stage:ship` → `ship-ticket`
   Pass the ticket number as the skill's argument.
5. Do not chain into the next stage automatically — stop after the invoked skill returns so the user can review its output, per the pipeline's "review and validate each step" rule.
6. Report which ticket and stage ran, which branch it ran on, and what the next stage will be once this one is approved.

## Goal
Keep exactly one ticket moving through the pipeline at a time, on its own branch, with a human checkpoint between every stage.
