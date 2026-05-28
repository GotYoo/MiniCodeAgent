import json

from minicodeagent import cli as mini_cli


def write_report(root, run_id, payload):
    run_dir = root / ".minicodeagent" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "report.json").write_text(json.dumps(payload), encoding="utf-8")
    return run_dir


def test_report_command_prints_latest_structured_run_report(tmp_path, capsys):
    write_report(
        tmp_path,
        "run_001",
        {
            "run_id": "run_001",
            "status": "completed",
            "stop_reason": "final_answer_returned",
            "final_answer": "Finished.",
            "tools_requested": ["read_file", "patch_file"],
            "tools_used": ["read_file", "patch_file"],
            "risky_tools_requested": ["patch_file"],
            "approval_denied_count": 0,
            "read_only_blocked_count": 0,
            "files_read": ["README.md"],
            "files_modified": ["minicodeagent/cli.py"],
            "active_skill_names": ["test-fix"],
            "tool_status_counts": {"ok": 2},
            "tool_error_code_counts": {},
        },
    )

    exit_code = mini_cli.main(["report", "latest", "--cwd", str(tmp_path)])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Run: run_001" in output
    assert "Status: completed" in output
    assert "Tools requested:" in output
    assert "- patch_file" in output
    assert "Active skills:" in output
    assert "- test-fix" in output
    assert "Files modified:" in output
    assert "- minicodeagent/cli.py" in output


def test_report_command_reads_active_skills_from_prompt_metadata(tmp_path, capsys):
    write_report(
        tmp_path,
        "run_001",
        {
            "run_id": "run_001",
            "status": "completed",
            "stop_reason": "final_answer_returned",
            "prompt_metadata": {"active_skill_names": ["repo-summary"]},
        },
    )

    exit_code = mini_cli.main(["report", "latest", "--cwd", str(tmp_path)])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Active skills:" in output
    assert "- repo-summary" in output


def test_report_command_handles_missing_runs(tmp_path, capsys):
    exit_code = mini_cli.main(["report", "latest", "--cwd", str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "No run reports found" in captured.err


def test_runs_command_lists_available_runs(tmp_path, capsys):
    write_report(tmp_path, "run_001", {"run_id": "run_001", "status": "completed", "stop_reason": "final_answer_returned"})
    write_report(tmp_path, "run_002", {"run_id": "run_002", "status": "stopped", "stop_reason": "step_limit_reached"})

    exit_code = mini_cli.main(["runs", "--cwd", str(tmp_path)])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "run_001 completed final_answer_returned" in output
    assert "run_002 stopped step_limit_reached" in output
