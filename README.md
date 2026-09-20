# Codex Kilo Delegation

Let Codex make the decisions and verify the result while Kilo handles substantial implementation, tests and corrections.

This Codex skill uses **Kilo Auto Efficient**, which chooses underlying models automatically. It aims to save Codex usage by handing off work Codex can check more cheaply than it can perform. Kilo usage is billed separately; lower total cost is not guaranteed.

## What it does

- Gives a worker a bounded assignment in an isolated Git worktree.
- Preserves normal Kilo tools and configured permissions for implementation, including running tests.
- Saves the result and queues one completion message to Codex. No model-driven polling loop.
- Keeps acceptance and integration with Codex. Nothing is automatically merged or pushed.

Good assignments include settled features, reproducible repairs, refactors and substantial test batches. Keep tiny edits, deterministic scripts and unresolved requirements local. Read-only exploration and review use a restricted tool profile.

## Install

Requires Codex, Python 3.10+, Git and an authenticated Kilo CLI account with authorized billing. The tested Kilo version is **7.7.5**; the wrapper checks the version and stops on a mismatch. Windows is the live-tested platform. Other platforms are not qualified.

Clone into your Codex skills directory (normally `~/.codex/skills`):

```powershell
git clone https://github.com/Concrete333/Codex-Kilo-Delegation.git "$env:USERPROFILE/.codex/skills/kilo-delegator"
python "$env:USERPROFILE/.codex/skills/kilo-delegator/scripts/kilo_delegate.py" doctor
```

If that directory already exists, update or reconcile it instead of overwriting it. For a custom Codex home, use its skills directory. Authentication stays with Kilo; do not put credentials in this repository.

## Use

Ask Codex:

> Use $kilo-delegator for suitable implementation work. Let Kilo implement, test and correct it; verify the result before integration.

Automatic discovery is enabled. Explicit invocation is useful when starting out; the skill does not grant permission to transmit code or spend money by itself.

The default in `settings.json` is `kilo/kilo-auto/efficient`, with no fixed reasoning variant. Codex retains decisions about requirements, consequential domain behavior and acceptance. Workers receive the assignment and relevant evidence, not the whole conversation.

Completion wake-up requires a native Codex executable supporting `queue --thread --message`. Delivery is armed, not guaranteed. If unavailable, Codex tells you to check back instead of repeatedly polling. Safe reruns after verified mechanical fixes are allowed within existing authorization; uncertain delivery is not automatically retried.

## Limits and verification

Implementation starts from a clean committed revision; uncommitted changes are not copied. Worktrees prevent ordinary edit collisions, **not malicious access**. Use trusted repositories and inspect inherited Kilo configuration. Existing permissions apply, and interactive approval can block a detached run.

The default limits are 30 steps and one hour, not a dollar cap. A timeout or incomplete handoff is not accepted as success. Logs may contain source code; keep them private.

The Auto Efficient smoke test completed a small Python implementation, ran and corrected its tests, and passed independent checks: 15 unit tests plus 3,375 interval combinations. Worker-reported cost was $0.0157, excluding Codex preparation and review. One small run confirms operation, not general savings.

Run offline tests:

```powershell
python -B -m unittest discover -s tests -q
```

Operational details: [task contract](references/task-contract.md), [runtime](references/runtime.md).
Related project: [Codex Agent Deployment](https://github.com/Concrete333/Codex-Agent-Deployment).
Routing documentation: [Kilo Auto Model](https://kilo.ai/docs/code-with-ai/agents/auto-model).
