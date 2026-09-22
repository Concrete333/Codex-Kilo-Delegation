# Codex Kilo Delegation

Let Kilo handle mechanical edit batches and small, pattern-following implementations while Codex owns decisions and verification.

This Codex skill uses **DeepSeek V4.1 Flash Max through Kilo**. It aims to save Codex usage by handing off work Codex can check more cheaply than it can perform. Kilo usage is billed separately; lower total cost is not guaranteed.

## What it does

- Gives a worker a bounded assignment in an isolated Git worktree.
- Preserves normal Kilo tools and configured permissions for implementation, including running tests.
- Saves the result and queues one completion message to Codex. No model-driven polling loop.
- Keeps acceptance and integration with Codex. Nothing is automatically merged or pushed.

Candidate assignments include repeated edits, a small self-contained utility, or tests for specified cases following an existing example. Supply target files and executable checks. Keep debugging, historical investigation, cross-component changes and stateful safety repairs in Codex. Tiny edits and deterministic scripts usually do not justify delegation. Read-only extraction and checklist review use a restricted tool profile.

## Install

Requires Codex, Python 3.10+, Git and an authenticated Kilo CLI account with authorized billing. The configuration-checked Kilo version is **7.7.7**; the wrapper checks the version and stops on a mismatch. All three worker profiles passed no-inference configuration checks, and 53 offline tests passed. Windows is the live-tested platform. Other platforms are not qualified.

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

The default in `settings.json` is `kilo/deepseek/deepseek-v4.1-flash`, with variant `max`. You can explicitly choose another supported model and its variant. Codex retains decisions about requirements, consequential domain behavior and acceptance. Workers receive the assignment and relevant evidence, not the whole conversation.

Completion wake-up requires a native Codex executable supporting `queue --thread --message`. Delivery is armed, not guaranteed. If unavailable, Codex tells you to check back instead of repeatedly polling. Safe reruns after verified mechanical fixes are allowed within existing authorization; uncertain delivery is not automatically retried.

## Limits and verification

Implementation starts from a clean committed revision; uncommitted changes are not copied. Worktrees prevent ordinary edit collisions, **not malicious access**. Use trusted repositories and inspect inherited Kilo configuration. Existing permissions apply, and interactive approval can block a detached run.

There is no step cap by default; the one-hour timeout remains. Neither is a dollar budget. Set an optional iteration limit with `--steps N`, or use `--steps 0` for no cap. A timeout or incomplete handoff is not accepted as success. Logs may contain source code; keep them private.

## Measured results

In a 22 September 2026 inventory-component test, both DeepSeek V4.1 Flash Max and GLM 5.3 Flash Max passed all 27 independent test methods before review. Astra High added acceptance tests without changing either implementation.

| Worker | Worker cost | Including Astra High acceptance |
| --- | ---: | ---: |
| DeepSeek V4.1 Flash Max | $0.046 | **$0.584** |
| GLM 5.3 Flash Max | $0.072 | **$0.728** |

DeepSeek's pipeline cost 22.7% less than the earlier same-task Astra solo run ($0.756), and 14.4% less than Luna + Astra ($0.683). These are one run per route, with historical—not simultaneous—solo/Luna controls. Acceptance was 92% of DeepSeek's total. Costs combine Kilo-reported spending and API-equivalent Codex estimates, exclude shared setup and analysis, and do not measure subscription quota savings.

DeepSeek is the default starting candidate, not a proven winner for every task. MiMo's attempt returned an upstream timeout before producing an implementation; that does not establish a coding-capability failure. [Full protocol, results and accounting](https://github.com/Concrete333/Codex-Delegation-Deployment/blob/main/docs/benchmarks/inventory-events/external-workers-results-2026-09-22.md).

The comparison used a per-run 65,536-token output ceiling and 30-minute timeout. Normal skill use leaves Kilo's output ceiling unchanged and retains the one-hour timeout.

Run offline tests:

```powershell
python -B -m unittest discover -s tests -q
```

Operational details: [task contract](references/task-contract.md), [runtime](references/runtime.md).
Related project: [Codex Agent Deployment](https://github.com/Concrete333/Codex-Delegation-Deployment).
