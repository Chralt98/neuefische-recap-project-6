---
name: new-ticket
description: "Draft a GitHub issue in the pipeline's Goal/Scope/Tasks/Acceptance Criteria/Notes format from a rough feature idea, present it as a plan for approval, then create it on GitHub once approved. Use when the user wants to create a new ticket/issue for a feature."
argument-hint: "<rough description of the feature or ticket to create>"
user-invocable: true
---

# New Ticket

## When to Use
Whenever the user wants to add a new ticket to the board. This is how tickets enter the pipeline — it runs before `stage:plan` even starts, not one of the `stage:*` stages itself.

## Format
Every issue in this repo follows the same structure:

```
## Goal
<one or two sentences: what this ticket achieves and why>

## Scope
- <bullet list of what's in scope>

## Tasks
- [ ] <concrete, checkable task>
  - [ ] <sub-task, if it helps break the task down>

## Acceptance Criteria
- <bullet list of observable, testable conditions that must hold when this ticket is done>

## Notes
- <anything worth flagging: explicit non-goals, follow-up ideas, constraints>
```

## Steps
1. If the user's description is too vague to write real tasks or acceptance criteria from, ask clarifying questions first — don't invent scope to fill gaps.
2. Enter plan mode.
3. Draft a short, descriptive issue title and the full issue body in the format above. Keep Tasks concrete and independently checkable (each box should be genuinely completable and verifiable — see [checklist.md](../../rules/checklist.md), which governs how these boxes get checked off later).
4. Exit plan mode with the drafted title and body as the plan. This is the "send to GitHub" checkpoint — nothing is created on GitHub until the user approves this plan.
5. Once approved, create the issue: `gh issue create --title "<title>" --body "<body>"`. Do not add a `stage:*` label — `next-ticket` treats a label-less issue as `stage:plan` and will pick it up on its own.
6. Make sure the issue lands in the **Todo** column of the repo's project board, using plain `gh project` subcommands or GraphQL. Don't hardcode an owner/handle or project number; resolve them at runtime, since anyone consuming this skill will have their own:
   - Resolve the owner: `gh repo view --json owner --jq .owner.login`. Find the pipeline's project: `gh project list --owner <owner>` (if more than one exists, ask the user which one).
   - Check whether the new issue is already on the board: `gh project item-list <project-number> --owner <owner> --format json`, looking for its URL. The board's `Auto-add to project` workflow usually adds it automatically.
   - If it's missing, add it: `gh project item-add <project-number> --owner <owner> --url <issue-url>`.
   - If its Status isn't already "Todo", set it: get the Status field/option ids from `gh project field-list <project-number> --owner <owner> --format json`, then `gh project item-edit --id <item-id> --project-id <project-id> --field-id <status-field-id> --single-select-option-id <todo-option-id>`.
7. Report the created issue's URL, number, and confirmed board column.

## Goal
Every ticket enters the pipeline in the exact shape the rest of the pipeline expects, and nothing hits GitHub before a human has seen and approved it.
