import pathlib
import subprocess

ROOT = pathlib.Path(__file__).parents[1]


def test_main_reports_version(capsys):
    from strands.cli import main

    assert main(["--version"]) == 0
    assert "strands" in capsys.readouterr().out


def test_main_unknown_command_returns_2():
    from strands.cli import main

    assert main(["frobnicate"]) == 2


def test_console_script_runs():
    out = subprocess.run(
        ["uv", "run", "strands", "--version"], capture_output=True, text=True, cwd=ROOT
    )
    assert out.returncode == 0


def test_interpreter_is_at_least_3_12():
    import sys

    assert sys.version_info[:2] >= (3, 12)
