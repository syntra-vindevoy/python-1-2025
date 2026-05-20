"""Spin up the Shiny app once per test session for Playwright UI tests."""

import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))

        return s.getsockname()[1]


def _wait_ready(url: str, timeout: float = 30.0):
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
            return
        except Exception:
            time.sleep(0.3)

    raise RuntimeError(f"App did not become ready at {url} within {timeout}s")


@pytest.fixture(scope="session")
def shiny_app():
    project_root = Path(__file__).resolve().parents[2]
    port = _free_port()
    env = {**os.environ, "PYTHONPATH": str(project_root / "src")}

    proc = subprocess.Popen(
        [sys.executable, "-m", "shiny", "run", "src/energy/main.py", "--host", "127.0.0.1", "--port", str(port)],
        cwd=project_root,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    url = f"http://127.0.0.1:{port}"

    try:
        _wait_ready(url)

        yield url
    finally:
        proc.terminate()

        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
