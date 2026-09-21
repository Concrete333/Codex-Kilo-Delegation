# Local runtime

Use absolute paths. Python standard library only; Git and installed Kilo are required.

```powershell
python <skill-dir>/scripts/kilo_delegate.py doctor
python <skill-dir>/scripts/kilo_delegate.py start --repo C:/path/repo --task-file C:/path/task.json --notify-thread CURRENT-TASK-UUID --notify-codex C:/path/to/codex.exe
python <skill-dir>/scripts/kilo_delegate.py status --run-dir C:/path/returned-run
```

`start --dry-run` prepares the candidate and verifies the installed CLI profile
without inference. It retains the worktree and logs. A real start is a separate
explicit command. Optional flags: `--model provider/model`, `--variant NAME`,
`--base-ref REF`, `--steps N`, `--timeout-seconds N`. A variant is provider-specific;
do not invent one. Default to `kilo/xiaomi/mimo-v2.6-pro` with variant `thinking`;
use another configuration only for an explicit user choice. Record the effective
model and variant when exposed; do not substitute another model if unavailable.

For a bounded correction, use `start --candidate <previous-run-dir>` with the
same repo and a new task file. Only a finished implementation candidate may be
reused; its full diff remains subject to scope checks. This starts a fresh Kilo
session with the candidate files, not a replay of the earlier conversation.

Runs live under `%LOCALAPPDATA%/KiloDelegator/runs/`. `receipt.json` is the compact
status; `handoff.json`, `events.jsonl`, `stderr.log`, `changes.patch`,
`changed-files.json` and `manifest.json` retain evidence. New-file contents remain
in the worktree; Git's patch alone does not include untracked files.
The hidden supervisor enforces a process-tree timeout and preserves partial work.
If its terminal receipt is missing, do not assume the job finished or relaunch it.

Supply both notification flags to arm a single completion follow-up. Use the
confirmed current task UUID (for example, `CODEX_THREAD_ID`) and native executable;
CLI support is checked before launch. Omit both when unavailable and ask the user
to check back. Dry runs send no notification. Keep the host available.

After saving a terminal receipt and releasing ownership where safe, the supervisor
calls `codex queue` once, including on failure. `receipt.notification.json` records
delivery; `notification-supervisor.log` retains helper errors. Queued means the
message was submitted, not that work passed verification. An existing notification
record suppresses repeat delivery. Do not retry uncertain delivery automatically.
The helper returns nonzero unless delivery is recorded as queued;
`notification-helper.json` records its outcome separately from the worker result.
If delivery fails, inspect the saved result when the user checks back. No scheduled
automation, recurring check or extra acceptance session is required.

If `ownership_check_required` is true, resolve the recorded process/cleanup issue
before testing, editing or integrating the candidate. `termination_unconfirmed`
means the worker may still run; use the retained PIDs and keep its lock until
termination is confirmed. A cleanup error does not authorize transferring ownership.

Implementation uses normal Kilo configuration, tools, skills, plugins and MCP
integrations, with the requested worker model and step limit checked before launch.
The wrapper does not add a tool denylist or auto-approve permission requests.
Existing permissions still apply; a detached run needing interactive approval may
block or fail. Assign implementation, tests and corrections together. Read/write
paths are assignment boundaries and post-run checks, not shell isolation.
Review inherited project configuration before using a trusted checkout. Additional
delegation, paid services and consequential external actions need task authorization.

For explore/review, the wrapper verifies Kilo's exact tested version and resolved worker permissions
before inference. Per-run config isolates global/project Kilo configuration,
disables external plugins/skills and denies tools by default; scoped reads and edits
are the exceptions. Existing Kilo authentication is reused by Kilo itself, never
copied into the skill. Provider calls still send supplied code off-machine.
No `--auto`, API-key discovery, auth changes or model substitution is used.

In explore/review only, shell, LSP, MCP tools, web tools, agent management and task delegation are denied.
Grep/glob/list are disabled: grep's permission pattern is the search expression,
not a path restriction. Use scoped directory reads for discovery and give workers
useful entry points. Kilo appends an external-directory allowance for its internal
truncated-output files; scoped read rules still deny those files. Other external
directory access is denied. Git worktrees share Git metadata: they prevent ordinary
edit collisions, not malicious access. Project AGENTS instructions may still be
loaded by Kilo. Only use trusted repositories and review their instructions first.
Sensitive/configuration paths and symlinks are rejected conservatively.

Kilo `steps` requests a final text-only response; the wrapper also rejects runs
that reach the cap. Timeout and malformed output preserve artifacts, not success.
Usage is recorded from observed step events; missing cost/usage stays unknown.
It excludes Codex preparation/review and is not an accepted-result savings claim.

To inspect a candidate: `git -C <worktree> status --short` and
`git -C <worktree> diff <base-commit>`, then inspect new files and run the agreed
checks. Cleanup and integration are deliberately manual. Retain logs only as long
as needed; they may contain source code and are not loaded on ordinary skill use.
