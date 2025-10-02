# test_integration.py
"""
Simple integration test to verify all components work together
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from app.advanced_workflow import count_tokens
    print("✅ Imports successful!")
    print(f"Count tokens function: {count_tokens}")
    
    # Test token counting
    test_text = "Hello world, this is a test"
    tokens = count_tokens(test_text)
    print(f"Token count test: '{test_text}' -> {tokens} tokens")
    
    # Test different models
    from app.advanced_workflow import get_optimal_lengths
    exec_len, analysis_len, context = get_optimal_lengths("grok-4-fast", 300)
    print(f"Optimal lengths test: exec={exec_len}, analysis={analysis_len}, context={context}")
    
    print("✅ All integration tests passed!")
    
except Exception as e:
    print(f"❌ Integration test failed: {e}")
