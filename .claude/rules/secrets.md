# Secrets Rule

The OpenAI API key, and any other credential, is only ever read from the framework's idiomatic env/credentials mechanism (see [framework-conventions.md](framework-conventions.md)). It is never written as a literal string in source, tests, fixtures, migrations, or commit history.

`review-ticket` greps the diff for common key-shaped literals (e.g. `sk-...`) before approving a ticket.
