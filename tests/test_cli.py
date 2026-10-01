import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"


def run_cli(*args):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_cli_ok():
    result = run_cli("calc", "1 + 2 * 3")
    assert result.returncode == 0
    assert result.stdout.strip() == "7"


def test_cli_help():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "calc" in result.stdout
    assert "convert" in result.stdout


def test_cli_error():
    result = run_cli("convert", "1", "--from", "m", "--to", "kg")
    assert result.returncode == 2
    assert result.stderr.strip() != ""
    assert result.stdout.strip() == ""