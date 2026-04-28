# test_api.py - Enhanced with summary_length and follow_up coverage

import os
import sys
import types
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def install_test_dependency_stubs():
    if "google.api_core.exceptions" not in sys.modules:
        google_module = sys.modules.setdefault("google", types.ModuleType("google"))
        api_core_module = types.ModuleType("google.api_core")
        exceptions_module = types.ModuleType("google.api_core.exceptions")

        class ResourceExhausted(Exception):
            pass

        exceptions_module.ResourceExhausted = ResourceExhausted
        api_core_module.exceptions = exceptions_module
        google_module.api_core = api_core_module
        sys.modules["google.api_core"] = api_core_module
        sys.modules["google.api_core.exceptions"] = exceptions_module

    if "langgraph.graph" not in sys.modules:
        langgraph_module = types.ModuleType("langgraph")
        graph_module = types.ModuleType("langgraph.graph")

        class StateGraph:
            def __init__(self, state_type):
                self.state_type = state_type
                self.nodes = {}
                self.edges = []
                self.entry_point = None

            def add_node(self, name, node):
                self.nodes[name] = node

            def set_entry_point(self, name):
                self.entry_point = name

            def add_edge(self, start, end):
                self.edges.append((start, end))

            def compile(self):
                class CompiledWorkflow:
                    def invoke(self, state):
                        return state

                return CompiledWorkflow()

        graph_module.StateGraph = StateGraph
        graph_module.END = "END"
        langgraph_module.graph = graph_module
        sys.modules["langgraph"] = langgraph_module
        sys.modules["langgraph.graph"] = graph_module

    if "langchain_openai" not in sys.modules:
        langchain_openai_module = types.ModuleType("langchain_openai")

        class ChatOpenAI:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

            def invoke(self, messages):
                return types.SimpleNamespace(content="stubbed response")

        langchain_openai_module.ChatOpenAI = ChatOpenAI
        sys.modules["langchain_openai"] = langchain_openai_module

    if "langchain_core.messages" not in sys.modules:
        messages_module = types.ModuleType("langchain_core.messages")

        class BaseMessage:
            def __init__(self, content="", type="human"):
                self.content = content
                self.type = type

        class HumanMessage(BaseMessage):
            def __init__(self, content=""):
                super().__init__(content=content, type="human")

        messages_module.BaseMessage = BaseMessage
        messages_module.HumanMessage = HumanMessage
        sys.modules["langchain_core.messages"] = messages_module

    if "langchain_core.language_models.chat_models" not in sys.modules:
        chat_models_module = types.ModuleType("langchain_core.language_models.chat_models")

        class SimpleChatModel:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            def invoke(self, messages):
                result = self._call(messages)
                return types.SimpleNamespace(content=result)

        chat_models_module.SimpleChatModel = SimpleChatModel
        sys.modules["langchain_core.language_models.chat_models"] = chat_models_module

    if "langchain_core.output_parsers" not in sys.modules:
        output_parsers_module = types.ModuleType("langchain_core.output_parsers")

        class PydanticOutputParser:
            def __init__(self, pydantic_object):
                self.pydantic_object = pydantic_object

            def get_format_instructions(self):
                return "stubbed format"

            def __ror__(self, other):
                return self

        output_parsers_module.PydanticOutputParser = PydanticOutputParser
        sys.modules["langchain_core.output_parsers"] = output_parsers_module

    if "langchain_core.prompts" not in sys.modules:
        prompts_module = types.ModuleType("langchain_core.prompts")

        class _FakeChain:
            def __or__(self, other):
                return self

            def invoke(self, values):
                return values

        class ChatPromptTemplate:
            @classmethod
            def from_messages(cls, messages):
                return _FakeChain()

        prompts_module.ChatPromptTemplate = ChatPromptTemplate
        sys.modules["langchain_core.prompts"] = prompts_module

    if "ddgs" not in sys.modules:
        ddgs_module = types.ModuleType("ddgs")

        class DDGS:
            def text(self, **kwargs):
                return []

        ddgs_module.DDGS = DDGS
        sys.modules["ddgs"] = ddgs_module

    if "crawl4ai" not in sys.modules:
        crawl4ai_module = types.ModuleType("crawl4ai")

        class AsyncWebCrawler:
            pass

        crawl4ai_module.AsyncWebCrawler = AsyncWebCrawler
        sys.modules["crawl4ai"] = crawl4ai_module


install_test_dependency_stubs()

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.api import app
from app.schemas import FinalBrief, SourceSummary, BriefRequest

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
        with patch('app.api.create_advanced_workflow') as mock_workflow:
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
        with patch('app.api.create_advanced_workflow') as mock_workflow:
            mock_app = MagicMock()
            mock_workflow.return_value = mock_app
            mock_app.invoke.return_value = {"final_brief": self.create_mock_brief(topic="renewable energy storage"), "errors": None}
            
            response = client.post("/brief", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["brief"]["topic"] == "renewable energy storage"

    def test_valid_brief_request_with_byok_uses_request_scoped_provider_context(self):
        from app.llm_providers import get_request_provider_config

        request_data = {
            "topic": "renewable energy storage",
            "depth": 3,
            "user_id": "test_byok",
            "follow_up": False,
            "summary_length": 500,
            "byok": {
                "enabled": True,
                "provider": "google",
                "credentials": {"api_key": "user-google-key"}
            }
        }
        mock_brief = self.create_mock_brief(topic="renewable energy storage", user_id="test_byok")
        captured = {}

        class FakeWorkflow:
            def invoke(self, state):
                captured["state"] = state
                captured["provider_config"] = get_request_provider_config()
                return {"final_brief": mock_brief, "errors": None}

        with patch('app.api.create_advanced_workflow', return_value=FakeWorkflow()):
            response = client.post("/brief", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert captured["state"]["topic"] == request_data["topic"]
        assert "byok" not in captured["state"]
        assert captured["provider_config"] is not None
        assert captured["provider_config"].enabled is True
        assert captured["provider_config"].provider == "google"
        assert captured["provider_config"].credentials.api_key == "user-google-key"

    def test_non_byok_request_does_not_inherit_prior_byok_context(self):
        from app.llm_providers import get_request_provider_config

        captured_configs = []
        mock_brief = self.create_mock_brief(topic="request isolation topic", user_id="request_isolation")

        class FakeWorkflow:
            def invoke(self, state):
                captured_configs.append(get_request_provider_config())
                return {"final_brief": mock_brief, "errors": None}

        with patch('app.api.create_advanced_workflow', return_value=FakeWorkflow()):
            first_response = client.post(
                "/brief",
                json={
                    "topic": "request isolation topic",
                    "depth": 3,
                    "user_id": "request_isolation",
                    "byok": {
                        "enabled": True,
                        "provider": "google",
                        "credentials": {"api_key": "user-google-key"}
                    }
                },
            )
            second_response = client.post(
                "/brief",
                json={
                    "topic": "request isolation topic",
                    "depth": 3,
                    "user_id": "request_isolation"
                },
            )

        assert first_response.status_code == 200
        assert second_response.status_code == 200
        assert len(captured_configs) == 2
        assert captured_configs[0] is not None
        assert captured_configs[1] is None

    def test_disabled_byok_request_does_not_propagate_provider_context(self):
        from app.llm_providers import get_request_provider_config

        captured = {}
        mock_brief = self.create_mock_brief(topic="disabled byok topic", user_id="disabled_byok")

        class FakeWorkflow:
            def invoke(self, state):
                captured["provider_config"] = get_request_provider_config()
                return {"final_brief": mock_brief, "errors": None}

        with patch('app.api.create_advanced_workflow', return_value=FakeWorkflow()):
            response = client.post(
                "/brief",
                json={
                    "topic": "disabled byok topic",
                    "depth": 3,
                    "user_id": "disabled_byok",
                    "byok": {
                        "enabled": False,
                        "provider": "google",
                        "credentials": {"api_key": "user-google-key"}
                    }
                },
            )

        assert response.status_code == 200
        assert captured["provider_config"] is None


    def test_valid_brief_follow_up(self):
        request_data = {
            "topic": "AI healthcare follow-up",
            "depth": 3,
            "user_id": "test_user_123",
            "follow_up": True,
            "summary_length": 300
        }
        with patch('app.api.create_advanced_workflow') as mock_workflow:
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

    def test_invalid_byok_request_missing_required_credentials(self):
        invalid_request = {
            "topic": "Valid topic string",
            "depth": 3,
            "user_id": "test_user",
            "byok": {
                "enabled": True,
                "provider": "google",
                "credentials": {}
            }
        }
        response = client.post("/brief", json=invalid_request)
        assert response.status_code == 422

    def test_invalid_byok_request_requires_full_envelope_shape(self):
        invalid_request = {
            "topic": "Valid topic string",
            "depth": 3,
            "user_id": "test_user",
            "byok": {
                "enabled": False
            }
        }
        with patch('app.api.create_advanced_workflow') as mock_workflow:
            mock_app = MagicMock()
            mock_workflow.return_value = mock_app
            mock_app.invoke.return_value = {"final_brief": self.create_mock_brief(topic="Valid topic string"), "errors": None}

            response = client.post("/brief", json=invalid_request)

        assert response.status_code == 422


    def test_shared_brief_request_schema_includes_byok_field(self):
        assert "byok" in BriefRequest.model_fields

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
        with patch('app.api.create_advanced_workflow') as mock_workflow:
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
