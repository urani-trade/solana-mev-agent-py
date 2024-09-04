# tests/test_aleph.py

import os
import pytest
import requests
import subprocess
from src.utils.config import load_config


def run_command(command):
    """Run a command and return its output and exit code."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout, result.stderr, result.returncode


@pytest.fixture(scope="module", autouse=True)
def manage_server():
    """Fixture to start and stop the server before and after tests."""
    # Start the server
    start_cmd = "poetry run start_server"
    stdout, stderr, returncode = run_command(start_cmd)
    assert returncode == 0, f"Server failed to start. {stderr}"

    yield
    
    # Stop the server
    stop_cmd = "poetry run stop_server"
    stdout, stderr, returncode = run_command(stop_cmd)
    assert returncode == 0, f"Server failed to stop. {stderr}"
    
    # Clean up the batch file
    batch_file_to_delete = "src/protocol_server/orderbook/batches/batch.json"
    if os.path.exists(batch_file_to_delete):
        os.remove(batch_file_to_delete)
    else:
        pytest.fail(f"Batch file not found for deletion: {batch_file_to_delete}")

    # Clean up the solution file
    solution_file_to_delete = "src/protocol_server/orderbook/solutions/solution.json"
    if os.path.exists(solution_file_to_delete):
        os.remove(solution_file_to_delete)
    else:
        pytest.fail(f"Solution file not found for deletion: {solution_file_to_delete}")


def post_data():
    """Test posting data to the server."""
    config = load_config()
    url = config["URANI_ORDERBOOK_HTTPS_URL"] + 'batches'
    test_json_path = "orders_templates/example_batch.json"

    # Check if the server is running
    try:
        response = requests.get(url)
        assert response.status_code in [200, 404], f"Server GET request failed with status: {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Server GET request failed: {e}")
    
    # Proceed with POST request if server is running
    if response.status_code in [200, 404]:
        try:
            with open(test_json_path, "r") as file:
                data = file.read()
                response = requests.post(url, headers={"Content-Type": "application/json"}, data=data)
            assert response.status_code == 201, f"POST request failed with status code {response.status_code} and response: {response.text}"
        except requests.RequestException as e:
            pytest.fail(f"POST request failed: {e}")


def run_aleph():
    """Test running the CLI command."""
    cli_cmd = "poetry run mcli -d aleph"
    stdout, stderr, returncode = run_command(cli_cmd)
    assert returncode == 0, f"CLI command failed with error: {stderr}"


@pytest.mark.order(7)
def test_aleph():
    """Test aleph interacting with the orderbook"""
    post_data()
    run_aleph()
