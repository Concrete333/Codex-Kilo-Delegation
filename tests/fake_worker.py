"""Offline CLI event fixture. Never calls a provider."""
import json
import os
from pathlib import Path
import sys
import time

scenario = os.environ.get("KILO_DELEGATOR_TEST_SCENARIO", "complete")
json.load(sys.stdin)
if scenario == "timeout":
    time.sleep(30)
    sys.exit(0)
changed = []
if scenario in ("complete", "out_of_scope", "steps", "many_steps", "error", "blocked"):
    file = Path("outside.py" if scenario == "out_of_scope" else "src/thing.py")
    file.write_text("VALUE = 2\n")
    changed = [file.as_posix()]
if scenario != "missing":
    result = {"status": "complete", "summary": "Offline candidate", "files_changed": changed,
              "checks": ["Not run"], "judgment_calls": [], "blockers": ["Need decision"] if scenario == "blocked" else []}
    print(json.dumps({"type": "text", "sessionID": "fixture-session", "part": {"text": json.dumps(result)}}))
for i in range(40 if scenario == "many_steps" else 3 if scenario == "steps" else 1):
    print(json.dumps({"type": "step_finish", "part": {"id": str(i), "cost": 0.01,
        "reason": "length" if scenario == "length" else "stop", "tokens": {"input": 10, "output": 4}}}))
if scenario == "error":
    print(json.dumps({"type": "error", "error": "fixture provider error"}))
    sys.exit(2)
