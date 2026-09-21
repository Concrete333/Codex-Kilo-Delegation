# Codex Kilo Delegation

Let Kilo handle mechanical edit batches and small, pattern-following implementations while Codex owns decisions and verification.

This Codex skill uses **MiMo-V2.6-Pro through Kilo**, with reasoning enabled. It aims to save Codex usage by handing off work Codex can check more cheaply than it can perform. Kilo usage is billed separately; lower total cost is not guaranteed.

## What it does

- Gives a worker a bounded assignment in an isolated Git worktree.
- Preserves normal Kilo tools and configured permissions for implementation, including running tests.
- Saves the result and queues one completion message to Codex. No model-driven polling loop.
- Keeps acceptance and integration with Codex. Nothing is automatically merged or pushed.

Candidate assignments include repeated edits, a small self-contained utility, or tests for specified cases following an existing example. Supply target files and executable checks. Keep debugging, historical investigation, cross-component changes and stateful safety repairs in Codex. Tiny edits and deterministic scripts usually do not justify delegation. Read-only extraction and checklist review use a restricted tool profile.

## Install

Requires Codex, Python 3.10+, Git and an authenticated Kilo CLI account with authorized billing. The configuration-checked Kilo version is **7.7.6**; the wrapper checks the version and stops on a mismatch. All three worker profiles were checked without inference. Windows is the live-tested platform for the earlier workflow; MiMo implementation is not yet live-tested. Other platforms are not qualified.

Clone into your Codex skills directory (normally `~/.codex/skills`):

```powershell
git clone https://github.com/Concrete333/Codex-Kilo-Delegation.git "$env:USERPROFILE/.codex/skills/kilo-delegator"
python "$env:USERPROFILE/.codex/skills/kilo-delegator/scripts/kilo_delegate.py" doctor
```

If that directory already exists, update or reconcile it instead of overwriting it. For a custom Codex home, use its skills directory. Authentication stays with Kilo; do not put credentials in this repository.

## Use

Ask Codex:

> Use $kilo-delegator if this task has a mechanical or pattern-following batch worth delegating. Supply explicit checks and verify the result before integration.

Automatic discovery is enabled. Explicit invocation is useful when starting out; the skill does not grant permission to transmit code or spend money by itself.

The default in `settings.json` is `kilo/xiaomi/mimo-v2.6-pro`, with variant `thinking`. Codex retains decisions about requirements, consequential domain behavior and acceptance. Workers receive the assignment and relevant evidence, not the whole conversation.

Completion wake-up requires a native Codex executable supporting `queue --thread --message`. Delivery is armed, not guaranteed. If unavailable, Codex tells you to check back instead of repeatedly polling. Safe reruns after verified mechanical fixes are allowed within existing authorization; uncertain delivery is not automatically retried.

## Limits and verification

Implementation starts from a clean committed revision; uncommitted changes are not copied. Worktrees prevent ordinary edit collisions, **not malicious access**. Use trusted repositories and inspect inherited Kilo configuration. Existing permissions apply, and interactive approval can block a detached run.

The default limits are 30 steps and one hour, not a dollar cap. A timeout or incomplete handoff is not accepted as success. Logs may contain source code; keep them private.

A historical Auto Efficient smoke test completed a small Python implementation, ran and corrected its tests, and passed independent checks: 15 unit tests plus 3,375 interval combinations. Worker-reported cost was $0.0157, excluding Codex preparation and review. That run does not validate the current MiMo default or establish general savings. MiMo's catalog availability and configuration have been checked; a paid implementation test remains outstanding.

Run offline tests:

```powershell
python -B -m unittest discover -s tests -q
```

Operational details: [task contract](references/task-contract.md), [runtime](references/runtime.md).
Related project: [Codex Agent Deployment](https://github.com/Concrete333/Codex-Agent-Deployment).
Model benchmarks: [Artificial Analysis: MiMo-V2.6-Pro](https://artificialanalysis.ai/models/mimo-v2-6-pro).
