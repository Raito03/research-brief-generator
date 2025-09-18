2# test_deployed_api.py - Test your deployed AI research assistant
# WHY: Python script provides better error handling and response formatting
# WHAT: Sends structured request to your deployed API and displays results nicely

import requests
import json
import time

# WHY: Define your deployed API endpoint
# WHAT: This is the URL Railway assigned to your deployed service
API_BASE_URL = 'https://ai-research-assistant-production-1ef8.up.railway.app'
BRIEF_ENDPOINT = f'{API_BASE_URL}/brief'

def test_api_health():
    """
    WHY: Verify API is healthy before making expensive research requests
    WHAT: Quick check that returns immediately if API is responsive
    """
    try:
        # WHY: Send GET request to health endpoint with short timeout
        # WHAT: Health check should respond quickly (under 5 seconds)
        response = requests.get(f'{API_BASE_URL}/health', timeout=5)
        
        if response.status_code == 200:
            print("✅ API is healthy and responsive!")
            return True
        else:
            print(f"❌ API health check failed: Status {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ API health check timed out - server may be slow or down")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API health check failed: {e}")
        return False

def generate_research_brief(topic, depth=3, user_id="test_user"):
    """
    WHY: Generate research brief using your deployed AI assistant
    WHAT: Sends POST request with research parameters and handles response
    """
    
    # WHY: Prepare request payload with all required fields
    # WHAT: Structure matches your API's expected input format
    payload = {
        "topic": topic,              # WHY: Research subject (required, 5-200 chars)
        "depth": depth,              # WHY: Research thoroughness (1-5 scale)
        "user_id": user_id,          # WHY: User tracking (required, min 1 char)
        "follow_up": False           # WHY: Not a follow-up research request
    }
    
    print(f"🎯 Starting research brief generation...")
    print(f"   📝 Topic: '{topic}'")
    print(f"   📊 Depth: {depth}/5")
    print(f"   👤 User: {user_id}")
    print(f"   ⏳ This may take 30-90 seconds...\n")
    
    try:
        # WHY: Record start time to measure total request duration
        # WHAT: Helps understand API performance
        start_time = time.time()
        
        # WHY: Send POST request with JSON payload and long timeout
        # WHAT: Research generation is expensive and can take 1-2 minutes
        response = requests.post(
            BRIEF_ENDPOINT, 
            json=payload, 
            timeout=180,  # WHY: 3-minute timeout for complex AI operations
            headers={'Content-Type': 'application/json'}
        )
        
        # WHY: Calculate total request time including network overhead
        # WHAT: Shows both API processing time and network latency
        total_time = time.time() - start_time
        
        # WHY: Check HTTP status code first
        # WHAT: 200 = success, 4xx = client error, 5xx = server error
        if response.status_code == 200:
            # WHY: Parse JSON response from your API
            # WHAT: Converts JSON string to Python dictionary
            data = response.json()
            
            # WHY: Check if API reports success in response body
            # WHAT: Your API can return 200 but still report internal errors
            if data.get('success'):
                brief = data.get('brief', {})
                
                print("🎉 Research brief generated successfully!")
                print("=" * 60)
                print(f"📋 Brief ID: {data.get('brief_id')}")
                print(f"🎯 Topic: {brief.get('topic')}")
                print(f"📊 Depth: {brief.get('depth')}/5")
                print("\n📝 EXECUTIVE SUMMARY:")
                print(f"   {brief.get('executive_summary', 'No summary')}")
                
                print(f"\n🔍 KEY FINDINGS ({len(brief.get('key_findings', []))}):")
                for i, finding in enumerate(brief.get('key_findings', []), 1):
                    print(f"   {i}. {finding}")
                
                print(f"\n📚 SOURCES ({len(brief.get('sources', []))}):")
                for i, source in enumerate(brief.get('sources', []), 1):
                    print(f"   {i}. {source.get('title', 'Unknown')}")
                    print(f"      🔗 {source.get('url', 'No URL')}")
                
                # WHY: Show performance metrics
                # WHAT: API processing time vs total request time
                api_time = data.get('processing_time', 0)
                network_time = total_time - api_time
                print(f"\n⏱️  Performance:")
                print(f"   API Processing: {api_time}s")
                print(f"   Network Overhead: {network_time:.2f}s")
                print(f"   Total Time: {total_time:.2f}s")
                print("=" * 60)
                
                return data
            else:
                # WHY: Handle API-reported errors gracefully
                # WHAT: Your API returned success=false with error message
                error_msg = data.get('error', 'Unknown API error')
                print(f"❌ API Error: {error_msg}")
                return None
        else:
            # WHY: Handle HTTP errors (validation, server errors, etc.)
            # WHAT: Non-200 status codes indicate request problems
            print(f"❌ HTTP Error: {response.status_code}")
            try:
                # WHY: Try to get detailed error message from response
                # WHAT: APIs often include error details in response body
                error_data = response.json()
                if 'detail' in error_data:
                    print(f"   Details: {error_data['detail']}")
            except:
                # WHY: If JSON parsing fails, show raw response
                # WHAT: Sometimes error responses aren't valid JSON
                print(f"   Response: {response.text[:200]}...")
            return None
            
    except requests.exceptions.Timeout:
        # WHY: Handle timeout errors with helpful message
        # WHAT: 3-minute timeout exceeded - operation took too long
        print(f"❌ Request timed out after 3 minutes")
        print("💡 Try reducing research depth or try again later")
        return None
        
    except requests.exceptions.RequestException as e:
        # WHY: Handle network/connection errors
        # WHAT: DNS issues, connection refused, network problems
        print(f"❌ Request failed: {e}")
        return None
        
    except json.JSONDecodeError:
        # WHY: Handle invalid JSON responses
        # WHAT: API returned non-JSON response (likely an error)
        print("❌ Invalid JSON response from API")
        print(f"   Response: {response.text[:200]}...")
        return None

def main():
    """
    WHY: Main function to run the API test
    WHAT: Coordinates health check and research brief generation
    """
    print("🤖 Testing Deployed AI Research Assistant")
    print("=" * 50)
    
    # WHY: Check API health before expensive operations
    # WHAT: Prevents waiting 3 minutes for a request to a down server
    if not test_api_health():
        print("💡 Fix API deployment issues before generating research briefs")
        return
    
    print()
    
    # WHY: Generate research brief on an interesting topic
    # WHAT: Demonstrates your AI assistant's capabilities
    result = generate_research_brief(
        topic="impact of artificial intelligence on renewable energy",
        depth=3,
        user_id="demo_user_001"
    )
    
    if result:
        print("\n🎉 Test completed successfully!")
        print("📚 View full API documentation at:")
        print(f"   {API_BASE_URL}/docs")
    else:
        print("\n❌ Test failed - check logs and try again")

# WHY: Only run main() when script is executed directly
# WHAT: Allows importing this module without running the test
if __name__ == "__main__":
    main()
