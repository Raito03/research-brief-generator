# test_workflow.py
"""
Simple test suite for Research Brief Generator
Tests core functionality without external dependencies
"""

import os
import sys
import time

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_imports():
    """Test that all core modules can be imported"""
    try:
        from app.advanced_workflow import count_tokens, get_optimal_lengths, create_advanced_workflow
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
            ("This is a test sentence with multiple words.", 9)  # Longer sentence
        ]
        
        for text, expected_min in test_cases:
            tokens = count_tokens(text)
            assert tokens >= expected_min, f"Expected at least {expected_min} tokens for '{text}', got {tokens}"
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
            ("nvidia/nemotron-nano-9b-v2", 200)
        ]
        
        for model, target_length in test_cases:
            exec_length, analysis_length, context = get_optimal_lengths(model, target_length)
            
            assert exec_length > 0, f"Executive length should be > 0, got {exec_length}"
            assert analysis_length > 0, f"Analysis length should be > 0, got {analysis_length}"
            assert context > 0, f"Context should be > 0, got {context}"
            
            total = exec_length + analysis_length
            assert total >= target_length * 0.8, f"Total length {total} should be close to target {target_length}"
            
            print(f"   📏 {model}: exec={exec_length}, analysis={analysis_length}, context={context:,}")
        
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
            depth_level="basic"
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
            source_type="web"
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
                print(f"   ⚠️  {path} endpoint not found (might be configured differently)")
        
        print("✅ API creation test passed!")
        return True
    except Exception as e:
        print(f"❌ API creation test failed: {e}")
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
        ("API Creation", test_api_creation)
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
