# test_api.py - Enhanced with summary_length and follow_up coverage

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.api import app
from app.schemas import FinalBrief, SourceSummary

client = TestClient(app)

class TestHealthEndpoints:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert "timestamp" in data
        assert "version" in data
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

class TestBriefGeneration:
    def create_mock_brief(self, topic="artificial intelligence in healthcare", depth=3, user_id="test_user_123", follow_up=False):
        source1 = SourceSummary(
            url="https://example.com/ai-healthcare-diagnosis",
            title="AI Revolutionizes Medical Diagnosis",
            summary="This comprehensive study examines how artificial intelligence technologies are transforming medical diagnostic procedures with improved accuracy and efficiency across healthcare institutions.",
            key_points=[
                "AI reduces diagnostic errors by 40%",
                "Machine learning algorithms can detect diseases earlier than human physicians"
            ],
            relevance_score=0.9,
            credibility_score=0.85,
            source_type="web"
        )
        source2 = SourceSummary(
            url="https://example.com/ai-healthcare-implementation",
            title="Challenges in Healthcare AI Implementation",
            summary="An in-depth analysis covering regulatory, technical, and cultural challenges faced by healthcare institutions during the implementation of AI-powered tools.",
            key_points=[
                "Data privacy regulations create significant hurdles",
                "Healthcare professionals require extensive training on AI systems"
            ],
            relevance_score=0.8,
            credibility_score=0.9,
            source_type="web"
        )
        final_brief = FinalBrief(
            topic=topic,
            depth=depth,
            user_id=user_id,
            follow_up=follow_up,
            executive_summary=(
                "Artificial intelligence is fundamentally transforming healthcare by enhancing "
                "diagnostic accuracy, enabling personalized treatment plans, and driving greater operational efficiencies, "
                "ultimately improving patient outcomes on a global scale."
            ),
            research_questions=[
                "How does AI improve diagnostic accuracy?",
                "What are key challenges in AI-powered healthcare implementations?"
            ],
            key_findings=[
                "AI reduces diagnostic errors by 40% compared to traditional methods",
                "Machine learning algorithms can detect diseases earlier than human physicians",
                "Regulatory and training barriers remain significant challenges for adoption"
            ],
            detailed_analysis=(
                "This research brief explores the transformative potential of artificial intelligence "
                "in healthcare settings. AI-powered diagnostic systems show increased accuracy and speed, "
                "reducing human error and expediting patient care. While benefits are clear, adoption is "
                "hindered by data privacy concerns, need for regulatory compliance, and the requirement for "
                "specialized training for healthcare providers, necessitating a coordinated approach to deployment."
            ),
            sources=[source1, source2],
            processing_time_seconds=10.5
        )
        return final_brief

    def test_valid_brief_request(self):
        request_data = {
            "topic": "artificial intelligence in healthcare",
            "depth": 3,
            "follow_up": False,
            "user_id": "test_user_123"
        }
        with patch('api.create_advanced_workflow') as mock_workflow:
            mock_app = MagicMock()
            mock_workflow.return_value = mock_app
            mock_app.invoke.return_value = {"final_brief": self.create_mock_brief(), "errors": None}
            
            response = client.post("/brief", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "brief_id" in data
            assert data["brief"]["topic"] == "artificial intelligence in healthcare"
            assert len(data["brief"]["key_findings"]) >= 3
            assert len(data["brief"]["sources"]) == 2
            assert "processing_time" in data

    def test_valid_brief_request_with_summary_length(self):
        request_data = {
            "topic": "renewable energy storage",
            "depth": 3,
            "user_id": "test_summary",
            "follow_up": False,
            "summary_length": 500
        }
        with patch('api.create_advanced_workflow') as mock_workflow:
            mock_app = MagicMock()
            mock_workflow.return_value = mock_app
            mock_app.invoke.return_value = {"final_brief": self.create_mock_brief(topic="renewable energy storage"), "errors": None}
            
            response = client.post("/brief", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["brief"]["topic"] == "renewable energy storage"

    def test_valid_brief_follow_up(self):
        request_data = {
            "topic": "AI healthcare follow-up",
            "depth": 3,
            "user_id": "test_user_123",
            "follow_up": True,
            "summary_length": 300
        }
        with patch('api.create_advanced_workflow') as mock_workflow:
            mock_app = MagicMock()
            mock_workflow.return_value = mock_app
            mock_app.invoke.return_value = {"final_brief": self.create_mock_brief(follow_up=True), "errors": None}
            
            response = client.post("/brief", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["brief"]["follow_up"] is True

    def test_invalid_brief_request(self):
        invalid_request = {
            "topic": "",
            "depth": 10,
            "user_id": ""
        }
        response = client.post("/brief", json=invalid_request)
        assert response.status_code == 422

    def test_invalid_summary_length_too_low(self):
        invalid_request = {
            "topic": "Valid topic string",
            "depth": 3,
            "user_id": "test_user",
            "summary_length": 10
        }
        response = client.post("/brief", json=invalid_request)
        assert response.status_code == 422

    def test_invalid_summary_length_too_high(self):
        invalid_request = {
            "topic": "Valid topic string",
            "depth": 3,
            "user_id": "test_user",
            "summary_length": 3000
        }
        response = client.post("/brief", json=invalid_request)
        assert response.status_code == 422

    def test_topic_too_short(self):
        invalid_request = {
            "topic": "abc",
            "depth": 3,
            "user_id": "test_user",
            "summary_length": 300
        }
        response = client.post("/brief", json=invalid_request)
        assert response.status_code == 422

    def test_workflow_error_handling(self):
        request_data = {
            "topic": "test topic",
            "depth": 2,
            "follow_up": False,
            "user_id": "test_user"
        }
        with patch('api.create_advanced_workflow') as mock_workflow:
            mock_app = MagicMock()
            mock_workflow.return_value = mock_app
            mock_app.invoke.side_effect = Exception("Simulated internal error")
            response = client.post("/brief", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert "error" in data
            assert "Simulated internal error" in data["error"]

class TestStatusEndpoints:
    def test_get_active_requests(self):
        response = client.get("/active")
        assert response.status_code == 200
        data = response.json()
        assert "active_count" in data
        assert "requests" in data
        assert isinstance(data["active_count"], int)

if __name__ == "__main__":
    print("Running enhanced API tests...")
    pytest.main([__file__, "-v"])
