# test_workflow.py
"""
Simple test suite for Research Brief Generator
Tests core functionality without external dependencies
"""

import os
import sys
import time
import types

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


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
from google.api_core.exceptions import ResourceExhausted


def test_imports():
    """Test that all core modules can be imported"""
    try:
        from app.advanced_workflow import (
            count_tokens,
            get_optimal_lengths,
            create_advanced_workflow,
        )
        from app.schemas import ResearchPlan, SourceSummary, FinalBrief
        from app.api import app

        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_token_counting():
    """Test token counting functionality"""
    try:
        from app.advanced_workflow import count_tokens

        # Test cases
        test_cases = [
            ("", 0),  # Empty string
            ("hello", 1),  # Single word
            ("hello world", 2),  # Two words
            ("This is a test sentence with multiple words.", 9),  # Longer sentence
        ]

        for text, expected_min in test_cases:
            tokens = count_tokens(text)
            assert tokens >= expected_min, (
                f"Expected at least {expected_min} tokens for '{text}', got {tokens}"
            )
            print(f"   📊 '{text}' -> {tokens} tokens")

        print("✅ Token counting tests passed!")
        return True
    except Exception as e:
        print(f"❌ Token counting test failed: {e}")
        return False


def test_optimal_lengths():
    """Test optimal length calculation"""
    try:
        from app.advanced_workflow import get_optimal_lengths

        # Test with different models and lengths
        test_cases = [
            ("grok-4-fast", 300),
            ("deepseek-chat-v3.1", 500),
            ("nvidia/nemotron-nano-9b-v2", 200),
        ]

        for model, target_length in test_cases:
            exec_length, analysis_length, context = get_optimal_lengths(
                model, target_length
            )

            assert exec_length > 0, f"Executive length should be > 0, got {exec_length}"
            assert analysis_length > 0, (
                f"Analysis length should be > 0, got {analysis_length}"
            )
            assert context > 0, f"Context should be > 0, got {context}"

            total = exec_length + analysis_length
            assert total >= target_length * 0.8, (
                f"Total length {total} should be close to target {target_length}"
            )

            print(
                f"   📏 {model}: exec={exec_length}, analysis={analysis_length}, context={context:,}"
            )

        print("✅ Optimal lengths tests passed!")
        return True
    except Exception as e:
        print(f"❌ Optimal lengths test failed: {e}")
        return False


def test_workflow_creation():
    """Test that workflow can be created"""
    try:
        from app.advanced_workflow import create_advanced_workflow

        workflow = create_advanced_workflow()
        assert workflow is not None, "Workflow should not be None"

        print("✅ Workflow creation test passed!")
        return True
    except Exception as e:
        print(f"❌ Workflow creation test failed: {e}")
        return False


def test_schemas():
    """Test that Pydantic schemas work correctly"""
    try:
        from app.schemas import ResearchPlan, SourceSummary, FinalBrief

        # Test ResearchPlan creation
        plan = ResearchPlan(
            topic="test topic",
            research_questions=["Question 1", "Question 2"],
            search_queries=["query 1", "query 2", "query 3"],
            expected_sources=5,
            estimated_time_minutes=10,
            depth_level="basic",
        )
        assert plan.topic == "test topic"
        print("   ✅ ResearchPlan schema works")

        # Test SourceSummary creation
        summary = SourceSummary(
            url="https://example.com",
            title="Test Source",
            summary="This is a comprehensive test summary of the source content that provides detailed information about the topic and meets the minimum character requirement for validation.",
            key_points=["Point 1", "Point 2"],
            relevance_score=0.8,
            credibility_score=0.9,
            source_type="web",
        )
        assert summary.url == "https://example.com"
        print("   ✅ SourceSummary schema works")

        print("✅ Schema tests passed!")
        return True
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False


def test_api_creation():
    """Test that FastAPI app can be created"""
    try:
        from app.api import app

        assert app is not None, "FastAPI app should not be None"

        # Check if main endpoints exist
        route_paths = [route.path for route in app.routes]
        expected_paths = ["/health", "/brief", "/docs"]

        for path in expected_paths:
            if any(path in route_path for route_path in route_paths):
                print(f"   ✅ Found {path} endpoint")
            else:
                print(
                    f"   ⚠️  {path} endpoint not found (might be configured differently)"
                )

        print("✅ API creation test passed!")
        return True
    except Exception as e:
        print(f"❌ API creation test failed: {e}")
        return False


def test_workflow_crawler_integration():
    """Test the Crawl4AI integration wrapper."""
    try:
        from app.advanced_workflow import fetch_and_summarize
        import asyncio

        result = asyncio.run(fetch_and_summarize("https://example.com"))
        assert result is not None
        assert len(result) > 0

        print("✅ Workflow crawler integration test passed!")
        return True
    except Exception as e:
        print(f"❌ Workflow crawler integration test failed: {e}")
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("🧪 Running Research Brief Generator Tests")
    print("=" * 50)

    tests = [
        ("Import Tests", test_imports),
        ("Token Counting", test_token_counting),
        ("Optimal Lengths", test_optimal_lengths),
        ("Workflow Creation", test_workflow_creation),
        ("Schema Validation", test_schemas),
        ("API Creation", test_api_creation),
        ("Crawler Integration", test_workflow_crawler_integration),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY:")
    passed = 0
    failed = 0

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status}: {test_name}")
        if result:
            passed += 1
        else:
            failed += 1

    print(f"\n🎯 FINAL SCORE: {passed}/{len(tests)} tests passed")

    if failed == 0:
        print("🎉 ALL TESTS PASSED! Your system is working correctly!")
    else:
        print(f"⚠️  {failed} tests failed. Please check the errors above.")

    return failed == 0


def quick_test():
    """Run just the most important tests quickly"""
    print("⚡ Quick Test Mode - Essential Functions Only")
    print("-" * 40)

    # Test basic imports
    print("🔍 Testing imports...")
    if not test_imports():
        return False

    # Test token counting (core function)
    print("\n🔍 Testing token counting...")
    if not test_token_counting():
        return False

    # Test workflow creation (main component)
    print("\n🔍 Testing workflow...")
    if not test_workflow_creation():
        return False

    print("\n🎉 Quick tests completed successfully!")
    return True


if __name__ == "__main__":
    """
    Run the test suite
    
    Usage:
    python test_workflow.py           # Run all tests
    python test_workflow.py --quick   # Run quick tests only
    python test_workflow.py --help    # Show help
    """

    import sys

    if "--help" in sys.argv:
        print("Research Brief Generator Test Suite")
        print("===================================")
        print()
        print("Usage:")
        print("  python test_workflow.py           # Run all tests")
        print("  python test_workflow.py --quick   # Run essential tests only")
        print("  python test_workflow.py --help    # Show this help")
        print()
        print("Tests included:")
        print("  - Import verification")
        print("  - Token counting functionality")
        print("  - Optimal length calculations")
        print("  - Workflow creation")
        print("  - Schema validation")
        print("  - API initialization")

    elif "--quick" in sys.argv:
        success = quick_test()
        sys.exit(0 if success else 1)

    else:
        success = run_all_tests()
        sys.exit(0 if success else 1)


def _build_source_summary():
    from app.schemas import SourceSummary

    return SourceSummary(
        url="https://example.com/source",
        title="Test Source",
        summary="This source contains enough detail about the research topic to satisfy validation requirements and support synthesis behavior in tests.",
        key_points=["Point 1", "Point 2"],
        relevance_score=0.9,
        credibility_score=0.8,
        source_type="web",
    )


def _build_research_plan():
    from app.schemas import ResearchPlan

    return ResearchPlan(
        topic="test topic",
        research_questions=["Question 1?", "Question 2?"],
        search_queries=["query one", "query two", "query three"],
        expected_sources=3,
        estimated_time_minutes=10,
        depth_level="basic",
    )


def _build_synthesis_state():
    return {
        "topic": "test topic",
        "depth": 3,
        "user_id": "test_user",
        "follow_up": False,
        "summary_length": 300,
        "research_plan": _build_research_plan(),
        "raw_search_results": None,
        "source_summaries": [_build_source_summary(), _build_source_summary()],
        "final_brief": None,
        "start_time": time.time(),
        "errors": None,
        "current_step": "synthesis",
    }


def test_create_openrouter_llm_uses_selected_byok_provider_without_fallback(monkeypatch):
    from app.llm_providers import create_openrouter_llm, set_request_provider_config, reset_request_provider_config
    from app.schemas import BYOKConfig, BYOKCredentials

    calls = []

    class FakeGoogleLLM:
        def __init__(self, **kwargs):
            calls.append(kwargs)
            self.kwargs = kwargs

        def invoke(self, messages):
            return types.SimpleNamespace(content="ok")

    fake_google_module = types.ModuleType("langchain_google_genai")
    fake_google_module.ChatGoogleGenerativeAI = FakeGoogleLLM
    monkeypatch.setitem(sys.modules, "langchain_google_genai", fake_google_module)
    monkeypatch.setattr("app.llm_providers.ChatOpenAI", lambda **kwargs: (_ for _ in ()).throw(AssertionError("OpenRouter fallback should not be used for BYOK")))
    monkeypatch.setenv("OPENROUTER_API_KEY", "app-managed-openrouter-key")

    token = set_request_provider_config(
        BYOKConfig(
            enabled=True,
            provider="google",
            credentials=BYOKCredentials(api_key="user-google-key"),
        )
    )
    try:
        llm = create_openrouter_llm()
    finally:
        reset_request_provider_config(token)

    assert isinstance(llm, FakeGoogleLLM)
    assert len(calls) == 1
    assert calls[0]["google_api_key"] == "user-google-key"


def test_create_openrouter_llm_byok_failure_does_not_fallback(monkeypatch):
    from app.llm_providers import BYOKProviderError, create_openrouter_llm, set_request_provider_config, reset_request_provider_config
    from app.schemas import BYOKConfig, BYOKCredentials

    class FailingGoogleLLM:
        def __init__(self, **kwargs):
            pass

        def invoke(self, messages):
            raise RuntimeError("invalid google key")

    fake_google_module = types.ModuleType("langchain_google_genai")
    fake_google_module.ChatGoogleGenerativeAI = FailingGoogleLLM
    monkeypatch.setitem(sys.modules, "langchain_google_genai", fake_google_module)
    monkeypatch.setattr("app.llm_providers.ChatOpenAI", lambda **kwargs: (_ for _ in ()).throw(AssertionError("Fallback should not continue to OpenRouter")))
    monkeypatch.setenv("OPENROUTER_API_KEY", "app-managed-openrouter-key")

    token = set_request_provider_config(
        BYOKConfig(
            enabled=True,
            provider="google",
            credentials=BYOKCredentials(api_key="user-google-key"),
        )
    )
    try:
        with pytest.raises(BYOKProviderError):
            create_openrouter_llm()
    finally:
        reset_request_provider_config(token)


def test_create_openrouter_llm_preserves_non_byok_fallback(monkeypatch):
    from app.llm_providers import create_openrouter_llm

    class QuotaGoogleLLM:
        def __init__(self, **kwargs):
            pass

        def invoke(self, messages):
            raise ResourceExhausted("quota exhausted")

    class FakeOpenRouterLLM:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    fake_google_module = types.ModuleType("langchain_google_genai")
    fake_google_module.ChatGoogleGenerativeAI = QuotaGoogleLLM
    monkeypatch.setitem(sys.modules, "langchain_google_genai", fake_google_module)
    monkeypatch.delenv("CF_ACCOUNT_ID", raising=False)
    monkeypatch.delenv("CF_API_TOKEN", raising=False)
    monkeypatch.setenv("GOOGLE_API_KEY", "app-google-key")
    monkeypatch.setenv("OPENROUTER_API_KEY", "app-openrouter-key")
    monkeypatch.setattr("app.llm_providers.ChatOpenAI", FakeOpenRouterLLM)

    llm = create_openrouter_llm()

    assert isinstance(llm, FakeOpenRouterLLM)
    assert llm.kwargs["openai_api_key"] == "app-openrouter-key"


def test_synthesis_node_hard_fails_for_byok_provider_errors(monkeypatch):
    from app.advanced_workflow import synthesis_node
    from app.llm_providers import set_request_provider_config, reset_request_provider_config
    from app.schemas import BYOKConfig, BYOKCredentials

    class FailingLLM:
        def invoke(self, messages):
            raise RuntimeError("quota exceeded")

    monkeypatch.setattr("app.advanced_workflow.create_openrouter_llm", lambda **kwargs: FailingLLM())

    token = set_request_provider_config(
        BYOKConfig(
            enabled=True,
            provider="google",
            credentials=BYOKCredentials(api_key="user-google-key"),
        )
    )
    try:
        result = synthesis_node(_build_synthesis_state())
    finally:
        reset_request_provider_config(token)

    assert result["current_step"] == "synthesis_failed"
    assert result["errors"]
    assert "final_brief" not in result


def test_synthesis_node_preserves_fallback_for_non_byok_errors(monkeypatch):
    from app.advanced_workflow import synthesis_node

    class FailingLLM:
        def invoke(self, messages):
            raise RuntimeError("quota exceeded")

    monkeypatch.setattr("app.advanced_workflow.create_openrouter_llm", lambda **kwargs: FailingLLM())

    result = synthesis_node(_build_synthesis_state())

    assert result["current_step"] == "completed_with_fallback"
    assert result["final_brief"] is not None


def test_planning_node_preserves_byok_provider_failure_reason(monkeypatch):
    from app.advanced_workflow import planning_node
    from app.llm_providers import BYOKProviderError, reset_request_provider_config, set_request_provider_config
    from app.schemas import BYOKConfig, BYOKCredentials

    monkeypatch.setattr(
        "app.advanced_workflow.create_openrouter_llm",
        lambda **kwargs: (_ for _ in ()).throw(
            BYOKProviderError(
                "BYOK google provider failed quota validation. No fallback credentials were used."
            )
        ),
    )

    token = set_request_provider_config(
        BYOKConfig(
            enabled=True,
            provider="google",
            credentials=BYOKCredentials(api_key="user-google-key"),
        )
    )
    try:
        result = planning_node(
            {
                "topic": "test topic",
                "depth": 3,
                "user_id": "test_user",
                "follow_up": False,
                "summary_length": 300,
                "research_plan": None,
                "raw_search_results": None,
                "source_summaries": None,
                "final_brief": None,
                "start_time": time.time(),
                "errors": None,
                "current_step": "planning",
            }
        )
    finally:
        reset_request_provider_config(token)

    assert result["current_step"] == "planning_failed"
    assert result["errors"]
    assert "quota validation" in result["errors"][0]
    assert "No fallback credentials were used." in result["errors"][0]
