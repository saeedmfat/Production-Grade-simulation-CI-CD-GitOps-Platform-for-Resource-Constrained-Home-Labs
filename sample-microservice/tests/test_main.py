import pytest
import os
import sys
import time

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../app'))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Fixtures for reusable test data
@pytest.fixture
def sample_message():
    return "Hello CI/CD!"

@pytest.fixture
def long_message():
    return "x" * 100

class TestAPISmokeTests:
    """Smoke tests for basic API functionality"""
    
    def test_root_endpoint_returns_200(self):
        """Test root endpoint returns successful response"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "service_id" in data
        assert "docs" in data
    
    def test_health_check_returns_healthy(self):
        """Test health check endpoint returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "service_id" in data
        assert "timestamp" in data
    
    def test_service_info_returns_correct_data(self):
        """Test service info endpoint returns correct information"""
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "sample-microservice"
        assert data["version"] == "1.0.0"
        assert "environment" in data
        assert "service_id" in data
        assert "uptime_seconds" in data
        assert isinstance(data["uptime_seconds"], float)

class TestEchoFunctionality:
    """Tests for echo endpoint functionality"""
    
    def test_echo_valid_message(self, sample_message):
        """Test echo with valid message"""
        response = client.post("/echo", json={"message": sample_message})
        assert response.status_code == 200
        data = response.json()
        assert data["echo"] == f"You said: {sample_message}"
        assert "timestamp" in data
        assert "request_id" in data
    
    def test_echo_empty_message(self):
        """Test echo with empty message (should fail validation)"""
        response = client.post("/echo", json={"message": ""})
        assert response.status_code == 422  # Validation error
    
    def test_echo_long_message(self, long_message):
        """Test echo with long message"""
        response = client.post("/echo", json={"message": long_message})
        assert response.status_code == 200
        data = response.json()
        assert data["echo"] == f"You said: {long_message}"
    
    def test_echo_missing_message_field(self):
        """Test echo with missing message field"""
        response = client.post("/echo", json={})
        assert response.status_code == 422  # Validation error
    
    def test_echo_invalid_json(self):
        """Test echo with invalid JSON"""
        response = client.post("/echo", data="invalid json")
        assert response.status_code == 422

class TestPerformanceCharacteristics:
    """Performance and basic load testing"""
    
    def test_response_time_acceptable(self):
        """Test that response times are within acceptable limits"""
        endpoints = ["/", "/health", "/info"]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            assert response.status_code == 200
            response_time = end_time - start_time
            assert response_time < 1.0  # 1 second threshold for CI
    
    def test_multiple_sequential_requests(self):
        """Test handling multiple sequential requests"""
        for i in range(10):
            response = client.get("/health")
            assert response.status_code == 200

class TestErrorHandling:
    """Test error conditions and edge cases"""
    
    def test_nonexistent_endpoint_returns_404(self):
        """Test that nonexistent endpoints return 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_invalid_method_returns_405(self):
        """Test that invalid HTTP methods return 405"""
        response = client.patch("/health")
        assert response.status_code == 405
    
    def test_metrics_endpoint_accessible(self):
        """Test metrics endpoint is accessible"""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "uptime_seconds" in data
        assert "service_id" in data

# Test categories for selective testing
@pytest.mark.smoke
class TestSmokeSuite:
    """Smoke tests for critical functionality"""
    
    def test_service_starts_and_responds(self):
        """Basic smoke test"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.integration
class TestIntegrationScenarios:
    """Integration test scenarios"""
    
    def test_complete_user_flow(self):
        """Test a complete user interaction flow"""
        # Get service info
        info_response = client.get("/info")
        assert info_response.status_code == 200
        
        # Send echo message
        echo_response = client.post("/echo", json={"message": "test flow"})
        assert echo_response.status_code == 200
        
        # Check health
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # Verify all responses have consistent service ID
        info_data = info_response.json()
        echo_data = echo_response.json()
        health_data = health_response.json()
        
        # All responses should reference the same service
        assert info_data["service_id"] == health_data["service_id"]