import requests
import time
import json

API_BASE_URL = 'https://ai-research-assistant-production-1ef8.up.railway.app'
BRIEF_ENDPOINT = f'{API_BASE_URL}/brief/stream'

def test_api_health():
    try:
        response = requests.get(f'{API_BASE_URL}/health', timeout=5)
        if response.status_code == 200:
            print("✅ API is healthy and responsive!")
            return True
        else:
            print(f"❌ API health check failed: Status {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print("❌ API health check timed out")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API health check failed: {e}")
        return False

def generate_research_brief(topic, depth=3, user_id="test_user", summary_length=300, follow_up=False):
    payload = {
        "topic": topic,
        "depth": depth,
        "user_id": user_id,
        "summary_length": summary_length,
        "follow_up": follow_up
    }

    print(f"🎯 Generating research brief for topic '{topic}' (depth={depth}, summary_length={summary_length})...")
    try:
        start_time = time.time()
        response = requests.post(
            BRIEF_ENDPOINT,
            json=payload,
            timeout=180,
            headers={'Content-Type': 'application/json'}
        )
        total_time = time.time() - start_time
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                brief = data.get('brief', {})
                print("🎉 Research brief generated successfully!")
                print("="*60)
                print(f"📋 Brief ID: {data.get('brief_id')}")
                print(f"🎯 Topic: {brief.get('topic')}")
                print(f"📊 Depth: {brief.get('depth')}/5")
                print(f"\n📝 EXECUTIVE SUMMARY:\n   {brief.get('executive_summary', 'No summary')}")
                print(f"\n🔍 KEY FINDINGS ({len(brief.get('key_findings', []))}):")
                for i, finding in enumerate(brief.get('key_findings', []), 1):
                    print(f"   {i}. {finding}")
                print(f"\n📚 SOURCES ({len(brief.get('sources', []))}):")
                for i, source in enumerate(brief.get('sources', []), 1):
                    print(f"   {i}. {source.get('title', 'Unknown')}")
                    print(f"       🔗 {source.get('url', 'No URL')}")
                api_time = data.get('processing_time', 0)
                network_time = total_time - api_time
                print(f"\n⏱️ Performance:")
                print(f"   API Processing: {api_time}s")
                print(f"   Network Overhead: {network_time:.2f}s")
                print(f"   Total Time: {total_time:.2f}s")
                print("="*60)
                return data
            else:
                print(f"❌ API Error: {data.get('error')}")
                return None
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            try:
                error_data = response.json()
                if 'detail' in error_data:
                    print(f" Details: {error_data['detail']}")
            except:
                print(f" Response Content: {response.text[:200]}...")
            return None
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 3 minutes")
        print("💡 Try reducing research depth or try again later")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None
    except json.JSONDecodeError:
        print("❌ Invalid JSON response")
        return None

def main():
    print("🤖 Testing deployed AI Research Assistant")
    print("="*50)
    if not test_api_health():
        print("💡 Fix API deployment issues first")
        return

    # Valid brief generation
    generate_research_brief(
        topic="impact of artificial intelligence on renewable energy",
        depth=3,
        user_id="demo_user_001",
        summary_length=300,
        follow_up=False
    )

    # Follow-up research test
    generate_research_brief(
        topic="blockchain scalability challenges",
        depth=3,
        user_id="demo_user_001",
        summary_length=400,
        follow_up=True
    )

    # Testing invalid input scenario
    print("\nTesting invalid topic length...")
    generate_research_brief(
        topic="abc",
        depth=2,
        user_id="demo_invalid",
        summary_length=300,
        follow_up=False
    )


if __name__ == "__main__":
    main()
