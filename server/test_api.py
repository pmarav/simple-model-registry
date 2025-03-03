import pytest
from fastapi.testclient import TestClient
from app import app
import os

client = TestClient(app)

# Test uploading a valid .pkl model file
@pytest.fixture
def sample_model_file():
    file_path = "test_model.pkl"
    with open(file_path, "wb") as f:
        f.write(b"Fake pickle content")
    yield file_path
    os.remove(file_path)  # Cleanup after test

def test_upload_model(sample_model_file):
    with open(sample_model_file, "rb") as f:
        response = client.post(
            "/models",
            files={"file": f},
            data={"name": "testmodel", "version": "1.0", "accuracy": "0.95"},
        )
    assert response.status_code == 200
    assert response.json()["message"] == "Model uploaded successfully"

# Test fetching all models (Assumes at least 1 model exists)
def test_get_models():
    response = client.get("/models")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test fetching a specific model
def test_get_model():
    response = client.get("/models/testmodel")
    assert response.status_code == 200
    assert response.json()["name"] == "testmodel"
