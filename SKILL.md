---
name: kilo-delegator
description: Delegate mechanical edit batches, small pattern-following implementations and known-file extraction to Kilo Auto Efficient when authorized and cheaply verifiable. Not for open-ended debugging, domain decisions or broad implementation.
---

# Kilo Delegator

Consider one Kilo worker when preparation, verification and likely repair cost less
Codex work than local execution. Preserve correctness; count external spending
separately. Do not add a Codex agent merely to call or supervise Kilo.

## Choose work to outsource

Codex owns requirements, consequential decisions, evidence checks, acceptance and
integration. The worker owns implementation choices within that contract. Apply
this split to Codex implementers and coordinators; do not duplicate delegated work.

- Use implementation for mechanical edit batches, small self-contained utilities,
  or code and tests following a named existing pattern. Supply target files,
  expected behavior and a runnable check; assign implementation and tests together.
- Use exploration for extraction from known files with an explicit output format.
  Require source locations and coverage. Use a local script for deterministic extraction.
- Keep open-ended debugging, historical reconstruction, cross-component changes,
  stateful safety repairs and acceptance decisions in Codex. A short task description
  does not make those tasks mechanical.
- Keep tiny edits local. Delegate only when the batch is large enough to offset
  preparation and review, without requiring the worker to discover the task.

Hand off once scope and checks are clear, before solving the assignment yourself;
no prior native-worker failure is required. Stay local if checking repeats the
whole task. Honor user choices and existing authorization; no per-task benchmark
or written cost estimate is required.

## Assign

Read [the task contract](references/task-contract.md) before the first launch.
Choose `implement`, `explore` or `review`. Give key entry points, project instructions,
settled decisions, shell/test commands and acceptance examples; leave local
navigation to the worker. For stateful behavior, specify status, allowed actions
and side effects rather than relying on field names.

If the worker needs missing evidence or a new domain decision, require it to
return the blocker and partial artifacts. Resolve that work in Codex; do not
turn the assignment into an investigation.

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
automatically resume. On wake-up or return, honor newer stop, pause or scope changes;
correlate the receipt with its run and handle each terminal result once.
Verify the result; a queued message is not proof of completion.

Implementation starts from an explicit clean Git revision in its own retained
worktree. It does not include uncommitted source changes. Read-only modes inspect
the supplied checkout; do not run them while its relevant files are changing.
Implementation uses Kilo's normal tools, skills, integrations and configured
permissions. Let the worker run tests and correct failures. Permission prompts
may block detached execution; report the blocker rather than bypassing approval.
Explore/review retain a restricted read-only profile. Worktrees are not a sandbox;
use trusted repositories and keep consequential external actions explicitly authorized.

## Accept

Review completed handoffs or agreed stable checkpoints, not unfinished writes.
Batch findings into one correction assignment. Intervene early only for a concrete
blocker, conflicting writes, an authorization issue or a user change.

Read the receipt and handoff, then the complete relevant diff (including new files),
test results, scope violations and judgment calls. Inspect supporting source where
needed; do not retrace the investigation. Run contract-derived checks after
inspecting runnable code. Do not weaken assertions to fit the result.
Resolve consequential ambiguity; process exit and worker approval are not acceptance.
Use review mode only for explicit checklist checks, not independent acceptance.

After confirmed termination, a verified mechanical fix permits a safe rerun within existing scope and budget without renewed permission. Preserve failure evidence and announce the retry. Reassess repeated failures; ask before material extra spending or actions outside existing authority. Never retry with uncertain ownership or duplicate side effects.

Return bounded defects to the same worktree with a new explicit repair contract
using `--candidate`; do not dispatch over an active owner. New domain decisions
stay local. Preserve partial edits/tests, exact commands/results and open questions.
After an attempt yields no usable artifact, finish locally or report the blocker.
Retry only for a verified mechanical or runtime failure, not stalled reasoning.
A longer briefing or larger budget alone is insufficient.
Distinguish provider/session errors, changed requirements and implementation failures.
Integrate only after acceptance and checking the parent has not diverged. Never
auto-merge, push, delete a worktree or claim savings without comparable outcomes.
