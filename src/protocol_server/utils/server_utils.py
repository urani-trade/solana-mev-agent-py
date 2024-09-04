# -*- encoding: utf-8 -*-
#!/usr/bin/env python3
# utils/server_utils.py

import os
import sys
import time
import subprocess

from urllib.parse import urlparse
from src.utils.config import load_config


def extract_host_port(url):
    """Extract the host and port from a URL."""
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port
    return host, port


def start_server():
    """Start the FastAPI server."""
    config = load_config()
    url = config["URANI_ORDERBOOK_HTTPS_URL"]
    host, port = extract_host_port(url)
    # Check if the server is already running
    try:
        existing_pids = subprocess.check_output(["lsof", "-i", f":{port}", "-t"], text=True).strip()
        if existing_pids:
            print("Server is already running.")
            return
    except subprocess.CalledProcessError as e:
        # lsof returned non-zero exit status; if there's no process, it's expected
        if e.returncode != 1:
            print(f"Error checking for running server: {e}")
            return

    # Define the command to start the server
    command = [
        "poetry", "run", "uvicorn", "src.protocol_server._server:app",
        "--host", host,
        "--port", str(port),
        "--reload"
    ]
    
    # Start the server
    with open("src/protocol_server/server.log", "w") as log_file:
        process = subprocess.Popen(command, stdout=log_file, stderr=log_file)
    print(f"Server started with PID {process.pid}")
    print(f"Server online at http://{host}:{port}/")

    # Wait for a few seconds to ensure server is up
    time.sleep(2)


def stop_server():
    """Stop the FastAPI server."""
    config = load_config()
    url = config["URANI_ORDERBOOK_HTTPS_URL"]
    host, port = extract_host_port(url)
    try:
        # Find the PID of the server
        pids = subprocess.check_output(["lsof", "-i", f":{port}", "-t"], text=True).strip()
        if not pids:
            print("No server running.")
            return

        # Terminate the server process
        for pid in pids.split('\n'):
            os.kill(int(pid), 9)  # Use signal 9 (SIGKILL) to force stop
        print("Server stopped.")

    except subprocess.CalledProcessError:
        print("Error finding server process.")


def main():
    if len(sys.argv) < 2:
        print("Usage: server_utils.py [start|stop]")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == "start":
        start_server()
    elif command == "stop":
        stop_server()
    else:
        print("Invalid command. Use 'start' or 'stop'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
