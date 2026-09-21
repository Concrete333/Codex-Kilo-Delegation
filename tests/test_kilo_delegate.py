import argparse
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock

spec = importlib.util.spec_from_file_location("kilo_delegate", Path(__file__).parents[1] / "scripts/kilo_delegate.py")
kd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kd)


def contract(mode="implement"):
    return {"mode": mode, "objective": "Add one behavior", "context": "Use existing patterns",
            "read_paths": ["src", "tests"], "write_paths": ["src/thing.py"] if mode == "implement" else [],
            "acceptance": ["Returns the specified result"], "constraints": [], "judgment_calls": []}


def handoff(**extra):
    return {"status": "complete", "summary": "Candidate ready", "files_changed": [],
            "checks": [], "judgment_calls": [], "blockers": [], **extra}


class UnitTests(unittest.TestCase):
    def test_configured_default_reaches_worker_profile(self):
        settings = kd.read_json(kd.SKILL / "settings.json")
        self.assertEqual(settings["model"], "kilo/xiaomi/mimo-v2.6-pro")
        self.assertEqual(settings["variant"], "thinking")
        for mode in ("implement", "explore", "review"):
            with self.subTest(mode=mode):
                config = kd.make_config(contract(mode), settings["model"],
                                        settings["variant"], settings["steps"])
                worker = config["agent"]["codex-worker"]
                self.assertEqual(worker["model"], settings["model"])
                self.assertEqual(worker["variant"], settings["variant"])

    def test_contract(self):
        self.assertEqual(kd.validate_contract(contract())["mode"], "implement")

    def test_unsafe_scope(self):
        for value in ("../secret", "/tmp", "C:/x", "src/*", ".", ".git/config", "src/.env", "src/key.pem", "src/NUL.txt", "src/.git./config"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                kd.clean_path(value)

    def test_readonly_cannot_write(self):
        task = contract("review")
        task["write_paths"] = ["src/x"]
        with self.assertRaises(ValueError):
            kd.validate_contract(task)

    def test_write_inside_read(self):
        task = contract()
        task["write_paths"] = ["other"]
        with self.assertRaises(ValueError):
            kd.validate_contract(task)

    def test_permission_policy(self):
        conf = kd.make_config(contract("review"), "kilo/test", None, 30)
        perms = conf["permission"]
        for tool in ("*", "bash", "task", "skill", "external_directory", "grep", "glob", "agent_manager"):
            self.assertEqual(perms[tool], "deny")
        self.assertEqual(perms["edit"]["*"], "deny")
        self.assertEqual(perms["edit"]["*/.git/*"], "deny")

    def test_no_inherited_overrides(self):
        with patch.dict(os.environ, {"KILO_PERMISSION": '{"*":"allow"}', "KILO_CONFIG": "bad"}):
            env = kd.child_env(Path("test-run"), kd.make_config(contract("review"), "kilo/test", None, 30))
        self.assertNotIn("KILO_PERMISSION", env)
        self.assertNotIn("KILO_CONFIG", env)
        self.assertEqual(env["KILO_DISABLE_PROJECT_CONFIG"], "true")

    def test_implementation_preserves_normal_capabilities(self):
        config = kd.make_config(contract(), "kilo/test", None, 30)
        for key in ("permission", "plugin", "mcp", "lsp", "formatter"):
            self.assertNotIn(key, config)
        self.assertNotIn("permission", config["agent"]["codex-worker"])
        with patch.dict(os.environ, {"KILO_CONFIG": "personal.json",
                "KILO_CONFIG_CONTENT": '{"permission":{"bash":"ask"},"agent":{"personal":{}}}'}):
            env = kd.child_env(Path("test-run"), config)
        self.assertEqual(env["KILO_CONFIG"], "personal.json")
        merged = json.loads(env["KILO_CONFIG_CONTENT"])
        self.assertEqual(merged["permission"]["bash"], "ask")
        self.assertIn("personal", merged["agent"])
        self.assertIn("codex-worker", merged["agent"])

    def test_handoff_rejects_status_only(self):
        with self.assertRaises(ValueError):
            kd.handoff_from_text('{"status":"complete"}')

    def test_handoff_accepts_fence(self):
        self.assertEqual(kd.handoff_from_text("```json\n" + json.dumps(handoff()) + "\n```"), handoff())

    def test_handoff_accepts_prose_and_final_fence(self):
        for newline in ("\n", "\r\n"):
            text = 'Implemented `batches`. Tests not run.' + newline + '```json' + newline + json.dumps(handoff()) + newline + '```'
            self.assertEqual(kd.handoff_from_text(text), handoff())

    def test_handoff_rejects_ambiguous_or_invalid_wrapping(self):
        block = '```json\n' + json.dumps(handoff()) + '\n```'
        for text in (block + '\nActually blocked', block + '\n' + block,
                     '```python\nx = 1\n```\n' + block,
                     '{"status":"blocked"}\n' + block,
                     'Done\n```json\n{"status":"complete"}\n```',
                     'Done\n' + json.dumps(handoff()),
                     'Done\n```json\nnot JSON\n```'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                kd.handoff_from_text(text)

    def test_events_deduplicate_and_unknown_cost(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "events.jsonl"
            step = {"type": "step_finish", "part": {"id": "s", "cost": 0.1}}
            file.write_text("\n".join(json.dumps(x) for x in [step, step, {"type": "text", "part": {"text": json.dumps(handoff())}}]))
            data = kd.parse_events(file)
            self.assertEqual(data["steps"], 1)
            self.assertEqual(data["reported_cost"], 0.1)
            file.write_text('{"type":"step_finish","part":{"id":"x"}}\n')
            self.assertIsNone(kd.parse_events(file)["reported_cost"])

    def test_profile_rejects_different_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            with patch.object(kd, "command", return_value=json.dumps({"permission": []})):
                with self.assertRaises(ValueError):
                    kd.resolved_profile("fake", run, {}, run, kd.make_config(contract(), "kilo/test", None, 30))


class GitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="kilo-delegator-test-")
        self.root = Path(self.tmp.name) / "repo"
        self.root.mkdir()
        (self.root / "src").mkdir()
        (self.root / "src/thing.py").write_text("VALUE = 1\n")
        kd.git(self.root, "init", "-q")
        kd.git(self.root, "add", ".")
        kd.git(self.root, "-c", "user.name=Offline Fixture", "-c", "user.email=fixture@invalid", "commit", "-qm", "fixture")
        self.base = kd.git(self.root, "rev-parse", "HEAD").strip()

    def tearDown(self):
        # Git worktrees are retained by runtime; disposable fixtures alone are cleaned here.
        import shutil
        for name in kd.git(self.root, "worktree", "list", "--porcelain").splitlines():
            if name.startswith("worktree ") and Path(name[9:]).resolve() != self.root.resolve():
                self.assertTrue(Path(name[9:]).resolve().is_relative_to(Path(self.tmp.name).resolve()))
                kd.git(self.root, "worktree", "remove", "--force", name[9:])
        def writable_remove(fn, path, exc):
            os.chmod(path, 0o700)
            fn(path)
        shutil.rmtree(self.tmp.name, onerror=writable_remove)
        self.tmp.cleanup()

    def test_new_files_and_changes(self):
        (self.root / "src/thing.py").write_text("VALUE = 2\n")
        (self.root / "src/new.py").write_text("NEW = 1\n")
        self.assertEqual(kd.changed_files(self.root, self.base), ["src/new.py", "src/thing.py"])

    def test_fingerprint_catches_already_dirty_change(self):
        (self.root / "src/thing.py").write_text("VALUE = 2\n")
        before = kd.checkout_fingerprint(self.root)
        (self.root / "src/thing.py").write_text("VALUE = 3\n")
        self.assertNotEqual(before, kd.checkout_fingerprint(self.root))

    def test_dry_run_isolates_parent_without_model(self):
        task = Path(self.tmp.name) / "task.json"
        task.write_text(json.dumps(contract()))
        args = argparse.Namespace(repo=str(self.root), task_file=str(task), model=None, variant=None,
                                  steps=None, timeout_seconds=None, candidate=None, base_ref=None, dry_run=True)
        with patch.object(kd, "RUNS", Path(self.tmp.name) / "runs"), patch.object(kd, "kilo_executable", return_value=sys.executable), patch.object(kd, "resolved_profile"):
            real_command = kd.command
            def mock_command(argv, **kw):
                return "7.7.6\n" if argv[1:] == ["--version"] else real_command(argv, **kw)
            with patch.object(kd, "command", side_effect=mock_command):
                result = kd.start(args)
        self.assertEqual(result["status"], "prepared")
        self.assertNotEqual(Path(result["worktree"]), self.root)
        self.assertEqual(kd.git(self.root, "status", "--porcelain"), "")

    def test_dirty_parent_rejected(self):
        task = Path(self.tmp.name) / "task.json"
        task.write_text(json.dumps(contract()))
        (self.root / "src/thing.py").write_text("VALUE = 2\n")
        args = argparse.Namespace(repo=str(self.root), task_file=str(task), model=None, variant=None,
                                  steps=None, timeout_seconds=None, candidate=None, base_ref=None, dry_run=True)
        real_command = kd.command
        with patch.object(kd, "kilo_executable", return_value=sys.executable), patch.object(kd, "command", side_effect=lambda argv, **kw: "7.7.6\n" if argv[1:] == ["--version"] else real_command(argv, **kw)):
            with self.assertRaisesRegex(ValueError, "clean"):
                kd.start(args)

    def run_fixture(self, scenario, mode="implement", notification=False, cleanup_failure=False, delivery_exit=0):
        run = Path(self.tmp.name) / "run"
        run.mkdir()
        lock = run / "worker-owner.lock"
        lock.write_text("owned")
        kd.save(run / "task.json", contract(mode))
        kd.save(run / "worker-config.json", kd.make_config(contract(mode), "kilo/test", None, 3))
        kd.save(run / "manifest.json", {"worktree": str(self.root), "binary": sys.executable,
            "model": "kilo/test", "variant": None, "timeout_seconds": 1 if scenario == "timeout" else 10,
            "base_commit": self.base, "mode": mode, "steps": 3,
            "initial_fingerprint": kd.checkout_fingerprint(self.root),
            "notify_thread": "00000000-0000-4000-8000-000000000001" if notification else None,
            "notify_codex": "fake-codex", "lock": str(lock)})
        real_popen = subprocess.Popen
        def launch(argv, **kw):
            if "notify" in argv:
                self.assertIn(kd.read_json(run / "receipt.json")["status"], ("candidate", "failed"))
                argv = [sys.executable, "-c", f"print('notification fixture'); raise SystemExit({delivery_exit})"]
            if "run" in argv:
                argv = [sys.executable, str(Path(__file__).with_name("fake_worker.py"))]
                kw["env"]["KILO_DELEGATOR_TEST_SCENARIO"] = scenario
            return real_popen(argv, **kw)
        real_unlink = Path.unlink
        def unlink(path, *args, **kw):
            if cleanup_failure and path == lock:
                raise PermissionError("lock busy")
            return real_unlink(path, *args, **kw)
        with patch.object(kd, "resolved_profile"), patch.object(kd.subprocess, "Popen", side_effect=launch), patch.object(Path, "unlink", unlink):
            kd.execute(run)
        return kd.read_json(run / "receipt.json")

    def test_candidate_receipt(self):
        value = self.run_fixture("complete")
        self.assertEqual(value["status"], "candidate")
        self.assertEqual(value["files_changed"], ["src/thing.py"])
        self.assertEqual(value["validation"], "not independently verified")

    def test_notification_after_success(self):
        self.assertEqual(self.run_fixture("complete", notification=True)["status"], "candidate")
        self.assertIn("notification fixture", (Path(self.tmp.name) / "run/notification-supervisor.log").read_text())

    def test_notification_after_failure(self):
        self.assertEqual(self.run_fixture("error", notification=True)["status"], "failed")
        self.assertIn("notification fixture", (Path(self.tmp.name) / "run/notification-supervisor.log").read_text())

    def test_cleanup_failure_still_notifies(self):
        state = self.run_fixture("complete", notification=True, cleanup_failure=True)
        self.assertTrue(state["ownership_check_required"])
        self.assertFalse(state["termination_unconfirmed"])
        self.assertEqual(state["cleanup_error"], "lock busy")
        self.assertTrue((Path(self.tmp.name) / "run/worker-owner.lock").exists())
        self.assertIn("notification fixture", (Path(self.tmp.name) / "run/notification-supervisor.log").read_text())

    def test_delivery_failure_separate_from_worker_result(self):
        state = self.run_fixture("complete", notification=True, delivery_exit=1)
        self.assertEqual(state["status"], "candidate")
        delivery = kd.read_json(Path(self.tmp.name) / "run/notification-helper.json")
        self.assertEqual(delivery["exit_code"], 1)
        self.assertEqual(delivery["status"], "delivery_unconfirmed")

    def test_unconfirmed_termination_preserves_pid_and_lock(self):
        run = Path(self.tmp.name) / "unconfirmed"
        run.mkdir()
        lock = run / "worker-owner.lock"
        lock.write_text("owned")
        kd.save(run / "manifest.json", {"worktree": str(self.root), "binary": "fake",
            "model": "fake/model", "variant": None, "timeout_seconds": 1, "lock": str(lock),
            "notify_thread": "00000000-0000-4000-8000-000000000001", "notify_codex": "fake"})
        kd.save(run / "task.json", {})
        kd.save(run / "worker-config.json", {})
        proc = Mock(pid=12345)
        proc.wait.side_effect = [subprocess.TimeoutExpired("worker", 1), subprocess.TimeoutExpired("worker", 30)]
        proc.poll.return_value = None
        def command(argv, **kw):
            if "notify" in argv:
                saved = kd.read_json(run / "receipt.json")
                self.assertEqual(saved["status"], "termination_unconfirmed")
                self.assertTrue(saved["ownership_check_required"])
            return subprocess.CompletedProcess(argv, 1)
        with patch.object(kd, "resolved_profile"), patch.object(kd, "child_env", return_value={}), patch.object(kd.subprocess, "Popen", return_value=proc), patch.object(kd.subprocess, "run", side_effect=command) as calls:
            kd.execute(run)
        state = kd.read_json(run / "receipt.json")
        self.assertEqual(state["worker_pid"], 12345)
        self.assertEqual(state["supervisor_pid"], os.getpid())
        self.assertTrue(state["termination_unconfirmed"])
        self.assertTrue(lock.exists())
        self.assertEqual(sum("notify" in call.args[0] for call in calls.call_args_list), 1)

    def test_missing_handoff_never_success(self):
        self.assertEqual(self.run_fixture("missing")["status"], "failed")

    def test_scope_violation_never_success(self):
        self.assertEqual(self.run_fixture("out_of_scope")["status"], "failed")

    def test_step_cap_never_success(self):
        self.assertEqual(self.run_fixture("steps")["status"], "failed")

    def test_provider_error_never_success(self):
        value = self.run_fixture("error")
        self.assertEqual(value["status"], "failed")
        self.assertEqual(value["exit_code"], 2)

    def test_timeout_never_success(self):
        value = self.run_fixture("timeout")
        self.assertEqual(value["status"], "failed")
        self.assertTrue(any("timeout" in s for s in value["issues"]))

    def test_blocker_beats_complete_claim(self):
        self.assertEqual(self.run_fixture("blocked")["status"], "blocked")

    def test_readonly_mutation_detected(self):
        self.assertEqual(self.run_fixture("complete", "review")["status"], "failed")


if __name__ == "__main__":
    unittest.main()
