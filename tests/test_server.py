# tests/test_server_utils.py

import time
import pytest
import subprocess

from src.utils.config import load_config
from src.protocol_server.server_utils import start_server, stop_server


# Utility functions
def get_server_url():
    """Get the server URL from the config."""
    config = load_config()
    return config["URANI_ORDERBOOK_HTTPS_URL"]


def extract_host_port(url):
    """Extract the host and port from a URL."""
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port
    return host, port


def is_server_running(port):
    """Check if the server is running on the given port."""
    try:
        subprocess.check_output(["lsof", "-i", f":{port}"], text=True)
        return True
    except subprocess.CalledProcessError:
        return False


@pytest.fixture(scope="module", autouse=True)
def manage_server():
    """Fixture to start and stop the server before and after tests."""
    # Start the server
    start_server()
    
    # Wait a bit for the server to start
    time.sleep(1)
    
    yield
    
    # Stop the server
    stop_server()
    
    # Ensure the server is stopped
    time.sleep(1)


@pytest.mark.order(5)
def test_server_is_running():
    """Test that the server is running."""
    url = get_server_url()
    _, port = extract_host_port(url)
    assert is_server_running(port), "Server should be running but isn't."


@pytest.mark.order(6)
def test_server_can_be_stopped():
    """Test that the server can be stopped."""
    url = get_server_url()
    _, port = extract_host_port(url)

    # Ensure server is running before stopping
    assert is_server_running(port), "Server should be running before stop test."
    
    stop_server()
    
    # Ensure the server is stopped
    time.sleep(2)
    assert not is_server_running(port), "Server should be stopped but is still running."
