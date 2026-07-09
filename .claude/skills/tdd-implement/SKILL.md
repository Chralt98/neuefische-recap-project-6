---
name: tdd-implement
description: "Implement a planned ticket strictly test-first: red, then green, then refactor. Use for the stage:implement step of the AI factory pipeline."
argument-hint: "<ticket-number>"
user-invocable: true
---

# TDD Implement

## When to Use
Second pipeline stage (`stage:implement`). The ticket already carries a checklist from `plan-ticket`.

## Steps
1. Read the ticket's checklist comment via `gh issue view <ticket-number> --comments`.
2. For each checklist item, in order:
   a. Write a failing test using the framework's test runner named in [framework-conventions.md](../../rules/framework-conventions.md).
   b. Run it and confirm it fails for the expected reason (red).
   c. Write the minimum implementation to pass it (green).
   d. Refactor if needed, keeping the suite green.
3. Follow [tdd.md](../../rules/tdd.md) throughout — no implementation code without a preceding failing test.
4. When all checklist items are green, relabel the ticket from `stage:implement` to `stage:review`.

## Goal
Every line of production code exists because a test demanded it.
