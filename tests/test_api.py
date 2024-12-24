"""Test pyn8n REST API."""

import httpx
from fastapi.testclient import TestClient

from pyn8n.api import app

client = TestClient(app)


def test_read_root() -> None:
    """Test that reading the root is successful."""
    response = client.get("/compute", params={"n": 7})
    assert httpx.codes.is_success(response.status_code)


def test_factorial_default_endpoint():
    response = client.post("/actions/factorial", json={"number": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 120}


def test_factorial_explicit_endpoint():
    response = client.post("/actions/compute_factorial", json={"number": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 120}
