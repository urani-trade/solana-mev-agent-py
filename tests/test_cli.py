# tests/test_cli.py

import subprocess
import pytest

def run_cli_command(command):
    """Run a CLI command and return its output and exit code."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout, result.stderr, result.returncode

@pytest.mark.order(1)
def test_mcli_help():
    """Test that the `mcli -h` command returns the help message."""
    stdout, stderr, returncode = run_cli_command("poetry run mcli -h")
    assert returncode == 0
    assert "usage:" in stdout.lower()  # Adjust based on your help message content

@pytest.mark.order(2)
def test_mcli_liquidities():
    """Test that the `mcli -l` command executes successfully."""
    stdout, stderr, returncode = run_cli_command("poetry run mcli -l")
    assert returncode == 0
    # Add assertions based on expected output for the list command

@pytest.mark.order(3)
def test_mcli_agents():
    """Test that the `mcli -a` command executes successfully."""
    stdout, stderr, returncode = run_cli_command("poetry run mcli -a")
    assert returncode == 0
    # Add assertions based on expected output for the add command

@pytest.mark.order(4)
def test_mcli_oracles():
    """Test that the `mcli -o` command executes successfully."""
    stdout, stderr, returncode = run_cli_command("poetry run mcli -o")
    assert returncode == 0
    # Add assertions based on expected output for the other command
