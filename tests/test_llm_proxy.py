"""
Tests for LLM Proxy Service
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from services.llm_proxy.app import app


client = TestClient(app)


def test_health_endpoint():
    """Test that health endpoint returns expected data"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["provider"] == "ollama"
    assert "ollama_url" in data
    assert "default_model" in data


def test_chat_endpoint_missing_message():
    """Test that chat endpoint validates required message field"""
    response = client.post("/chat", json={})
    assert response.status_code == 422  # Validation error


def test_chat_endpoint_empty_message():
    """Test that chat endpoint handles empty message"""
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 422


@patch("services.llm_proxy.app.httpx.AsyncClient")
def test_chat_endpoint_success(mock_client):
    """Test successful chat request"""
    # Mock Ollama response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": {
            "role": "assistant",
            "content": "Hello! How can I help you?"
        }
    }
    mock_response.raise_for_status = Mock()
    
    mock_post = Mock(return_value=mock_response)
    mock_client.return_value.__aenter__.return_value.post = mock_post
    
    response = client.post("/chat", json={
        "message": "Hello",
        "model": "llama3.2"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Hello! How can I help you?"
    assert data["model"] == "llama3.2"
    assert "timestamp" in data


@patch("services.llm_proxy.app.httpx.AsyncClient")
def test_chat_endpoint_with_history(mock_client):
    """Test chat request with conversation history"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": {
            "role": "assistant",
            "content": "I'm doing well, thank you!"
        }
    }
    mock_response.raise_for_status = Mock()
    
    mock_post = Mock(return_value=mock_response)
    mock_client.return_value.__aenter__.return_value.post = mock_post
    
    response = client.post("/chat", json={
        "message": "How are you?",
        "conversationHistory": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ],
        "model": "llama3.2"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "I'm doing well, thank you!"


@patch("services.llm_proxy.app.httpx.AsyncClient")
def test_chat_endpoint_ollama_connection_error(mock_client):
    """Test chat endpoint when Ollama is not available"""
    mock_client.return_value.__aenter__.return_value.post.side_effect = Exception("Connection refused")
    
    response = client.post("/chat", json={
        "message": "Hello",
        "model": "llama3.2"
    })
    
    assert response.status_code == 503
    assert "Cannot connect to Ollama" in response.json()["detail"]


@patch("services.llm_proxy.app.httpx.AsyncClient")
def test_chat_endpoint_timeout(mock_client):
    """Test chat endpoint timeout handling"""
    from httpx import TimeoutException
    mock_client.return_value.__aenter__.return_value.post.side_effect = TimeoutException("Timeout")
    
    response = client.post("/chat", json={
        "message": "Hello",
        "model": "llama3.2"
    })
    
    assert response.status_code == 504
    assert "timeout" in response.json()["detail"].lower()


def test_chat_endpoint_temperature_validation():
    """Test that temperature is validated"""
    # Temperature too high
    response = client.post("/chat", json={
        "message": "Hello",
        "temperature": 3.0
    })
    assert response.status_code == 422
    
    # Temperature negative
    response = client.post("/chat", json={
        "message": "Hello",
        "temperature": -0.5
    })
    assert response.status_code == 422
    
    # Valid temperature
    response = client.post("/chat", json={
        "message": "Hello",
        "temperature": 0.7
    })
    # Will fail at Ollama connection, but validates the input
    assert response.status_code != 422


@patch("services.llm_proxy.app.httpx.AsyncClient")
def test_models_endpoint_success(mock_client):
    """Test models endpoint returns available models"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [
            {"name": "llama3.2"},
            {"name": "gemma3"}
        ]
    }
    mock_response.raise_for_status = Mock()
    
    mock_get = Mock(return_value=mock_response)
    mock_client.return_value.__aenter__.return_value.get = mock_get
    
    response = client.get("/models")
    
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert "default" in data
    assert "llama3.2" in data["models"]


@patch("services.llm_proxy.app.httpx.AsyncClient")
def test_models_endpoint_connection_error(mock_client):
    """Test models endpoint when Ollama is not available"""
    mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("Connection refused")
    
    response = client.get("/models")
    
    assert response.status_code == 503
    assert "Cannot list models" in response.json()["detail"]
