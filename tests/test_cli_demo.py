from minicodeagent import cli as mini_cli


def test_demo_list_prints_interview_demo_templates(capsys):
    exit_code = mini_cli.main(["demo", "list"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "code-review" in output
    assert "test-fix" in output
    assert "repo-summary" in output


def test_demo_show_prints_prompt_and_replay_steps(capsys):
    exit_code = mini_cli.main(["demo", "show", "test-fix"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Demo: test-fix" in output
    assert "Prompt:" in output
    assert "Replay:" in output
    assert "uv run minicodeagent" in output
    assert "uv run minicodeagent report latest" in output


def test_demo_show_handles_unknown_demo(capsys):
    exit_code = mini_cli.main(["demo", "show", "missing"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Unknown demo: missing" in captured.err
