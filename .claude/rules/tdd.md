# TDD Rule

No implementation code is written before a failing test exists for it.

For every checklist item in `tdd-implement`: write the test, run it, confirm it fails for the *expected* reason (not a typo or import error), then write the minimum code to make it pass. Refactor only with the suite green.

`review-ticket` rejects a ticket back to `stage:implement` if it finds production code with no corresponding test.
