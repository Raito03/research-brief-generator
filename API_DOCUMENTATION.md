# 📚 API Documentation - AI Research Brief Generator

## Overview

The AI Research Brief Generator provides a RESTful API for generating comprehensive research briefs using advanced AI workflows. This document provides detailed information about all endpoints, request/response formats, and usage examples.

- **Base URL**: `https://ai-research-assistant-production-1ef8.up.railway.app`
- **API Version**: 1.0.0
- **Content-Type**: `application/json`

## Authentication

Currently, no authentication is required for public endpoints. API usage is rate-limited by Railway's infrastructure.

## Endpoints

### 1. Generate Research Brief

**Endpoint**: `POST /brief`

Generate a comprehensive research brief on any topic using AI-powered web search and analysis.

#### Request Format
```json
{
    "topic": "string", // Required: Research subject (5-200 characters)
    "depth": 1-5, // Optional: Research thoroughness (default: 3)
    "user_id": "string", // Required: Unique user identifier (min 1 character)
    "summary_length": 50-2000, // Optional: Desired word count (default: 300)
    "follow_up": boolean // Optional: Build on previous research (default: false)
}
```

#### Field Descriptions

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `topic` | string | Yes | 5-200 chars | Research subject or question |
| `depth` | integer | No | 1-5 | Research thoroughness level |
| `user_id` | string | Yes | min 1 char | Unique identifier for user tracking |
| `summary_length` | integer | No | 50-2000 | Target word count for summary sections |
| `follow_up` | boolean | No | true/false | Whether to build on previous research context |

#### Depth Levels
- **1 (Basic)**: Quick overview with 2-3 sources
- **2 (Light)**: Standard research with 3-4 sources  
- **3 (Medium)**: Balanced analysis with 4-6 sources
- **4 (Detailed)**: Comprehensive research with 6-8 sources
- **5 (Comprehensive)**: Exhaustive analysis with 8-10 sources

#### Response Format
```json
{
    "success": boolean,
    "brief_id": "string",
    "brief": {
        "topic": "string",
        "depth": integer,
        "user_id": "string",
        "follow_up": boolean,
        "executive_summary": "string",
        "research_questions": ["string"],
        "key_findings": ["string"],
        "detailed_analysis": "string",
        "sources": [
            {
            "url": "string",
            "title": "string",
            "summary": "string",
            "key_points": ["string"],
            "relevance_score": 0.0-1.0,
            "credibility_score": 0.0-1.0,
            "source_type": "web"
            }
        ],
        "created_at": "ISO 8601 timestamp",
        "processing_time_seconds": float
    },
    "processing_time": float,
    "created_at": "ISO 8601 timestamp",
    "error": "string or null"
}
```

#### Example Requests

**Basic Research Brief:**
```
curl -X POST https://ai-research-assistant-production-1ef8.up.railway.app/brief
-H "Content-Type: application/json"
-d '{
    "topic": "renewable energy trends 2025",
    "depth": 3,
    "user_id": "researcher_123"
}'
```

**Custom Length Research:**
```
curl -X POST https://ai-research-assistant-production-1ef8.up.railway.app/brief
-H "Content-Type: application/json"
-d '{
    "topic": "artificial intelligence in healthcare",
    "depth": 4,
    "user_id": "medical_student",
    "summary_length": 800
}'
```

**Follow-up Research:**
```
curl -X POST https://ai-research-assistant-production-1ef8.up.railway.app/brief
-H "Content-Type: application/json"
-d '{
"topic": "AI healthcare implementation challenges",
"depth": 3,
"user_id": "medical_student",
"summary_length": 600,
"follow_up": true
}'
```

#### PowerShell Examples

**Windows PowerShell:**
```powershell
$headers = @{"Content-Type" = "application/json"}
$body = @{
topic = "quantum computing applications"
depth = 3
user_id = "tech_researcher"
summary_length = 500
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://ai-research-assistant-production-1ef8.up.railway.app/brief" `
-Method POST -Headers $headers -Body $body
```

#### Python Examples

**Using requests library:**
```python
import requests

url = "https://ai-research-assistant-production-1ef8.up.railway.app/brief"

payload = {
    "topic": "sustainable transportation technologies",
    "depth": 4,
    "user_id": "sustainability_researcher",
    "summary_length": 700,
    "follow_up": False
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    data = response.json()
if data['success']:
    brief = data['brief']
    print(f"Generated brief: {brief['topic']}")
    print(f"Executive summary: {brief['executive_summary']}")
    print(f"Key findings: {len(brief['key_findings'])} points")
    print(f"Sources: {len(brief['sources'])} references")
else:
    print(f"Error: {data.get('error')}")
else:
    print(f"HTTP Error: {response.status_code}")
```

### 2. Health Check

**Endpoint**: `GET /health`

Check the service health and availability.

#### Response Format
```
{
    "status": "healthy" | "unhealthy",
    "timestamp": "ISO 8601 timestamp",
    "version": "string"
}
```

#### Example Request
```
curl https://ai-research-assistant-production-1ef8.up.railway.app/health
```


### 3. Interactive Documentation

**Endpoint**: `GET /docs`

Access the interactive API documentation (Swagger UI).

**URL**: https://ai-research-assistant-production-1ef8.up.railway.app/docs

Features:
- Interactive request testing
- Automatic request/response examples
- Schema validation
- Response format documentation

### 4. Alternative Documentation

**Endpoint**: `GET /redoc`

Access alternative API documentation (ReDoc UI).

**URL**: https://ai-research-assistant-production-1ef8.up.railway.app/redoc

### 5. Active Requests Monitor

**Endpoint**: `GET /active`

View currently processing requests (for monitoring).

#### Response Format
```json
{
    "active_count": integer,
    "requests": {
        "brief_id": {
            "status": "processing",
            "started_at": "ISO 8601 timestamp",
            "topic": "string"
        }
    }
}
```

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

### Error Response Format
```json
{
    "success": false,
    "error": "Error description",
    "detail": [
        {
            "type": "validation_error",
            "loc": ["field_name"],
            "msg": "Error message",
            "input": "invalid_input"
        }
    ]
}
```

### Common Error Examples

**Topic Too Short:**
```
{
    "detail": [
        {
            "type": "string_too_short",
            "loc": ["body", "topic"],
            "msg": "String should have at least 5 characters",
            "input": "AI"
        }
    ]
}
```

**Invalid Depth:**
```
{
    "detail": [
        {
            "type": "less_than_equal",
            "loc": ["body", "depth"],
            "msg": "Input should be less than or equal to 5",
            "input": 10
        }
    ]
}
```


## Rate Limiting

Currently implemented at the Railway infrastructure level:
- No explicit rate limits on individual endpoints
- Fair usage policy applies
- Heavy usage may be throttled automatically

## Response Times

Typical response times vary by research depth:
- **Depth 1**: 15-30 seconds
- **Depth 2**: 25-40 seconds  
- **Depth 3**: 35-50 seconds
- **Depth 4**: 45-70 seconds
- **Depth 5**: 60-90 seconds

Times may vary based on:
- Topic complexity
- Source availability
- Current system load
- Network conditions

## Best Practices

### Request Optimization
1. **Use appropriate depth**: Don't request depth 5 for simple queries
2. **Reasonable summary length**: 300-600 words is usually optimal
3. **Meaningful user IDs**: Use consistent identifiers for follow-up research
4. **Specific topics**: More specific topics yield better results

### Error Handling
```python
import requests
import time

def generate_research_brief(topic, depth=3, user_id="default", max_retries=3):
    url = "https://ai-research-assistant-production-1ef8.up.railway.app/brief"
    payload = {
        "topic": topic,
        "depth": depth,
        "user_id": user_id
    }
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data
                else:
                    print(f"API Error: {data.get('error')}")
                    return None
            elif response.status_code == 422:
                print("Validation error:", response.json())
                return None
            else:
                print(f"HTTP {response.status_code}: Retrying...")
                
        except requests.Timeout:
            print(f"Timeout on attempt {attempt + 1}")
        except requests.RequestException as e:
            print(f"Request error: {e}")
            
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff

    return None

```

### Follow-up Research Pattern
Initial research
```python
initial = generate_research_brief(
topic="renewable energy storage",
depth=3,
user_id="energy_researcher"
)

if initial and initial['success']:
# Follow-up research with same user_id
    followup = generate_research_brief(
    topic="battery storage economics",
    depth=3,
    user_id="energy_researcher", # Same user ID
    follow_up=True # Enable follow-up mode
    )
```

## SDK and Client Libraries

### Command Line Interface
The project includes a CLI tool for easy API interaction:

#### Basic usage
```
python cli.py --topic "AI ethics" --depth 3 --user researcher
```

#### With custom length
```
python cli.py --topic "blockchain" --depth 4 --user student --length 600
```

#### Interactive mode
```
python cli.py --interactive
```

### Python Integration
```python
from cli import generate_research_brief_api

### Use the built-in API client
result = generate_research_brief_api(
topic="machine learning trends",
depth=3,
user_id="ml_student",
summary_length=400
)
```

## Support and Contact

For technical support or questions about the API:
- **Interactive Docs**: https://ai-research-assistant-production-1ef8.up.railway.app/docs
- **Health Monitor**: https://ai-research-assistant-production-1ef8.up.railway.app/health
- **GitHub Issues**: 
- **Developer**: Anugraha Nayak (aka Raito)

---

- **Last Updated**: September 25, 2025
- **API Version**: 1.0.0
- **Documentation Version**: 1.0.0
