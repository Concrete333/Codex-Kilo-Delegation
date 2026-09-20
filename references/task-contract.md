# Task contract

Create a UTF-8 JSON file in the project's existing task/planning folder, or a
task-specific temporary directory. Do not include credentials. Schema:

```json
{
  "mode": "implement",
  "objective": "One bounded outcome",
  "context": "Relevant project instructions, entry points and settled decisions",
  "read_paths": ["src", "tests", "AGENTS.md"],
  "write_paths": ["src/component.py", "tests/test_component.py"],
  "acceptance": ["Concrete behavior and failure cases; checks the worker must run"],
  "constraints": ["No public API change or unrelated cleanup"],
  "judgment_calls": ["Any unresolved choice to report rather than silently decide"]
}
```

Paths are literal repository-relative files or directories, not globs. Include
only necessary read paths. Write scope must be inside read scope. Use empty
`write_paths` for `explore` and `review`. Read-only review needs relevant source
and any prepared diff artifact in read scope; shell access is unavailable.
Supply known exceptions as input → expected behavior, reusing existing tests.
Include shared-state ownership and whether a new requirement changes an earlier
contract. Checks must target correctness, not merely formatting or worker claims.

The wrapper asks for a JSON handoff with `status` (`complete`, `partial`,
`blocked`), `summary`, `files_changed`, `checks`, `judgment_calls`, and `blockers`.
Every list contains strings. Checks are worker-reported, not independently
verified. No handoff, malformed JSON, errors, scope drift, configuration mismatch
or a step/time limit prevents an acceptance-ready receipt. Codex still owns acceptance.
