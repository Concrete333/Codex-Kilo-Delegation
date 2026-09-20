---
name: kilo-delegator
description: Prefer Kilo Auto Efficient for substantial implementation, repairs, refactors, test batches and source searches that Codex need not own directly. Use when external delegation is authorized and checking the result costs less Codex work than doing it.
---

# Kilo Delegator

Default to one Kilo worker for substantial work that Codex need not own directly,
when preparation and acceptance cost less Codex work than local execution. The goal is
to reduce Codex usage while preserving correctness; external model spending is
separate. Include preparation, review and repair. Do not add a Codex agent merely
to call Kilo.

## Choose work to outsource

Codex owns requirements, consequential domain decisions, decision-critical evidence,
final acceptance and integration. The worker owns implementation choices within that
contract. Being responsible for accuracy does not require Codex to write the code
or duplicate the worker's investigation. Apply this split to Codex implementers as
well as coordinators; do not add a native agent just to supervise Kilo.

- Use implementation for a settled feature, reproducible bug fix, patterned
  refactor or substantial test batch. Assign implementation, tests and corrections
  together; let the worker navigate and solve local details.
- Use exploration for a bounded source search whose findings replace Codex reading.
  Require source locations and search coverage; inspect decision-critical evidence.
- Keep trivial edits and deterministic scriptable work local. Resolve unsettled
  requirements and cross-component design yourself, then delegate the resulting
  component if useful. Coupled files can share one worker; do not split their ownership.

Do not wait for a native worker to fail before considering Kilo. Once scope and
checks are clear, hand off before implementing or exhaustively investigating it
yourself. Do not outsource if verification requires repeating the whole task.
Honor explicit model/provider choices and existing external-delegation authorization;
ask only when needed authorization is missing. No benchmark comparison or written
cost estimate is required for each assignment.

## Assign

Read [the task contract](references/task-contract.md) before the first launch.
Choose `implement`, `explore` or `review`. Keep shared state and its consumers
with one implementation owner. Supply relevant project instructions, settled
decisions, bounded read paths and concrete acceptance examples; do not pass the
conversation, routing policies or benchmark history. For stateful behavior,
settle status/action/side-effect distinctions rather than having the worker infer
domain meaning from field names. Do not pre-solve the implementation to delegate it.

Use Auto Efficient (`kilo/kilo-auto/efficient`) from `settings.json` unless the
user explicitly selects another model. Leave variant unset; let Kilo route the
underlying model and reasoning configuration. Internal routing is expected;
do not silently replace the selected tier if unavailable. Retain result verification.
External code transmission and the configured provider's billing must be
authorized. CLI steps and wall time are limits, not a guaranteed dollar cap.

## Run

Use `scripts/kilo_delegate.py`, not ad hoc CLI commands. Commands and permission
limits are in [runtime guidance](references/runtime.md). `start` launches a
detached local supervisor and returns a run directory; it does not mean success.
Arm completion delivery with `--notify-thread <current-task-UUID>` and
`--notify-codex <absolute-native-codex-path>`. The supervisor saves the receipt,
then attempts one queued follow-up on success or failure. Keep notification controls
outside worker write scope. Do independent work or end the turn; report the receipt
path, pending verification, rough remaining time (or unknown) and that notification
is armed. Do not prequeue checks, poll or retry uncertain delivery.

If notification is unavailable, tell the user to check back because you will not
automatically resume. On wake-up or return, inspect the receipt once and verify
the result; a queued message is not proof of completion.

Implementation starts from an explicit clean Git revision in its own retained
worktree. It does not include uncommitted source changes. Read-only modes inspect
the supplied checkout; do not run them while its relevant files are changing.
Implementation uses Kilo's normal tools, skills, integrations and configured
permissions. Let the worker run tests and correct failures. Permission prompts
may block detached execution; report the blocker rather than bypassing approval.
Explore/review retain a restricted read-only profile. Worktrees are not a sandbox;
use trusted repositories and keep consequential external actions explicitly authorized.

## Accept

On return, read the compact receipt and handoff. Process exit, `complete` and
self-reported checks are not acceptance. Inspect actual changed files and the
complete relevant diff (including new files), scope violations and judgment calls.
Run contract-derived checks in the candidate worktree after inspecting runnable
code; do not weaken tests to fit the result or duplicate the implementation.
Resolve consequential ambiguity yourself. A clean review is not proof of
correctness; use review mode only for a named benefit, not as a standing second agent.

After confirmed termination, a verified mechanical fix permits a safe rerun within existing scope and budget without renewed permission. Preserve failure evidence and announce the retry. Reassess repeated failures; ask before material extra spending or actions outside existing authority. Never retry with uncertain ownership or duplicate side effects.

Return bounded defects to the same worktree with a new explicit repair contract
using `--candidate`; do not dispatch over an active owner. New domain decisions
stay local. Distinguish changed requirements from worker failures. A stalled or
failed core approach needs reassessment, not automatic retries or effort escalation.
Integrate only after acceptance and checking the parent has not diverged. Never
auto-merge, push, delete a worktree or claim savings without comparable outcomes.
