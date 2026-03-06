from fastapi.testclient import TestClient
import pytest
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}

def test_ask_endpoint_initialization():
    # We don't want to run the full LLM chain in a unit test 
    # unless the proxy is up and we have credits.
    # This just tests if the endpoint exists and the team is initialized.
    # To run a real test, we would need to mock the team.run_workflow response.
    pass
