# 🏗️ Technical Architecture - AI Research Brief Generator

## System Overview

The AI Research Brief Generator is a production-grade application built using modern software architecture principles, featuring a microservices-style design with clear separation of concerns.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│ Client Layer │
├─────────────────┬─────────────────┬─────────────────┬───────────────┤
│        CLI Tool │        REST API │          Web UI │    PowerShell │
│        (cli.py) │         Clients │         (/docs) │       Scripts │
└─────────────────┴─────────────────┴─────────────────┴───────────────┘
│
┌─────────────────────────────────────────────────────────────────────┐
│ API Gateway Layer │
├─────────────────────────────────────────────────────────────────────┤
│ FastAPI Server (api.py) │
│ ┌─────────────┬─────────────┬─────────────┬─────────────────────┐ │
│ │     Routing │  Validation │  Middleware │      Error Handling │ │
│ │      /brief │    Pydantic │        CORS │      Exception Mgmt │ │
│ │     /health │     Schemas │     Logging │     Response Format │ │
│ │       /docs │ (schemas.py)│             │        Status Codes │ │
│ └─────────────┴─────────────┴─────────────┴─────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────────────────────────────────────────┐
│ Business Logic Layer │
├─────────────────────────────────────────────────────────────────────┤
│ LangGraph Workflow Engine │
│ (advanced_workflow.py) │
│ ┌─────────────┬─────────────┬─────────────┬─────────────────────┐ │
│ │ Planning │ Search │ Summarize │ Synthesis │ │
│ │ Node │ Node │ Node │ Node │ │
│ │ Generate │ DuckDuckGo │ Source │ Final Brief │ │
│ │ Research │ Web Search │ Analysis │ Generation │ │
│ │ Questions │ Integration │ & Scoring │ & Formatting │ │
│ └─────────────┴─────────────┴─────────────┴─────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────────────────────────────────────────┐
│ Integration Layer │
├──────────────┬──────────────┬──────────────┬──────────────┬─────────┤
│    Multi-LLM │   DuckDuckGo │    LangChain │     Pydantic │
│     Provider │   Search API │   Components │   Validation │
│ Google Gemini│    Real-time │  Prompt Mgmt │ Serialization│
│   Cloudflare │   Web Search │    Chain Ops │  Type Safety │
│   OpenRouter │              │              │              │
└──────────────┴──────────────┴──────────────┴──────────────┴─────────┘
│
┌─────────────────────────────────────────────────────────────────────┐
│ Infrastructure Layer │
├─────────────────┬─────────────────┬─────────────────┬───────────────┤
│ Railway │ Docker │ Environment │ Monitoring │
│ Cloud │ Container │ Variables │ Health │
│ Platform │ Runtime │ Config Mgmt │ Checks │
│ Deployment │ Isolation │ Secret Mgmt │ Logging │
└─────────────────┴─────────────────┴─────────────────┴───────────────┘
```


## Component Architecture

### 1. API Gateway Layer (api.py)

**Purpose**: HTTP interface and request orchestration
**Technology**: FastAPI with Uvicorn ASGI server

#### Key Responsibilities:
- **Request Routing**: Map HTTP requests to appropriate handlers
- **Input Validation**: Pydantic schema validation for all requests
- **Authentication**: Future-ready for API key authentication
- **Rate Limiting**: Infrastructure-level rate limiting via Railway
- **Error Handling**: Comprehensive exception handling with user-friendly responses
- **Response Formatting**: Consistent JSON response structure
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

#### Architecture Patterns:

##### Dependency Injection Pattern
```python
@app.post("/brief", response_model=BriefResponse)
async def generate_brief(request: BriefRequest, background_tasks: BackgroundTasks):
    # Request validation happens automatically via Pydantic
    # Business logic is delegated to workflow layer
    pass
```

##### Middleware Pattern
```app.add_middleware(CORSMiddleware, allow_origins=["*"])```

##### Exception Handling Pattern
```python
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})
```


### 2. Business Logic Layer (advanced_workflow.py)

**Purpose**: AI workflow orchestration and state management
**Technology**: LangGraph with custom state management

#### Workflow State Machine:
```
┌─────────────┐     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Planning    │───▶│ Search │───▶│ Summarize │───▶│ Synthesis │
│      Node   │     │ Node │ │ Node │ │ Node │
└─────────────┘     └─────────────┘ └─────────────┘ └─────────────┘
│ │ │ │
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│Research │ │Web │ │Source │ │Final │
│Questions│ │Search │ │Analysis │ │Brief │
│Generated│ │Results │ │Complete │ │Ready │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
```


#### State Management:

```python
class AdvancedResearchState(TypedDict):
    # Input parameters
    topic: str
    depth: int
    user_id: str
    follow_up: bool
    summary_length: Optional[int]

    # Intermediate state
    research_plan: Optional[ResearchPlan]
    raw_search_results: Optional[List[dict]]
    source_summaries: Optional[List[SourceSummary]]

    # Final output
    final_brief: Optional[FinalBrief]

    # Metadata
    start_time: Optional[float]
    errors: Optional[List[str]]
    current_step: str
```

#### Node Architecture:
Each workflow node follows the same pattern:
1. **Input Validation**: Verify required state is present
2. **Processing**: Execute node-specific logic
3. **Error Handling**: Graceful failure with fallback options
4. **State Update**: Return updated state for next node
5. **Logging**: Detailed progress and performance logging

### 3. Data Layer (schemas.py)

**Purpose**: Data validation, serialization, and type safety
**Technology**: Pydantic v2 with comprehensive validation

#### Schema Hierarchy:
```bash
BaseModel (Pydantic)
├── BriefRequest # API input validation
├── BriefResponse # API output format
├── ResearchPlan # Workflow intermediate state
├── SourceSummary # Individual source data
└── FinalBrief # Complete research brief output
```

#### Validation Strategy:
```python
class BriefRequest(BaseModel):
    topic: str = Field(min_length=5, max_length=200)
    depth: int = Field(ge=1, le=5)
    user_id: str = Field(min_length=1)
    summary_length: Optional[int] = Field(default=300, ge=50, le=2000)
    follow_up: bool = Field(default=False)
# Custom validators for business logic
@field_validator('topic')
def validate_topic(cls, v):
    if not v.strip():
        raise ValueError('Topic cannot be empty')
    return v.strip()
```


### 4. Integration Layer

#### Multi-Provider LLM Integration
**Provider Hierarchy:**
1. **Google Gemini (Primary)**: `gemini-2.0-flash-lite` via Google AI Studio
2. **Cloudflare Workers AI (Secondary)**: `llama-3.1-8b-instruct` fallback
3. **OpenRouter (Tertiary)**: `deepseek-chat-v3.1-free` last resort

**Features:**
- **Automatic Failover**: Seamless switching between providers on failure
- **Request Management**: Automatic retry with exponential backoff per provider
- **Token Management**: Dynamic token calculation based on summary length
- **Cost Optimization**: Free-tier providers prioritized
- **Provider Health Tracking**: Emergency fallback system for complete provider failures


#### DuckDuckGo Search Integration
- **Real-time Search**: Live web search without API keys
- **Source Diversity**: Multiple search strategies for comprehensive coverage
- **Quality Filtering**: Relevance and credibility scoring
- **Infinite Retry**: Never fails to find sources

#### LangChain Components
- **Prompt Templates**: Dynamic prompt generation based on parameters
- **Message Management**: Structured conversation handling
- **Chain Operations**: Sequential and parallel LLM operations
- **Memory Management**: Context preservation for follow-up research

#### LLM Provider Architecture

**Initialization Logic:**
```python
def initialize_llm():
    """Multi-provider fallback initialization"""
    global llm, model_name_global
    # Priority 1: Google Gemini
    if os.getenv("GOOGLE_API_KEY"):
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-lite",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.7
            )
            model_name_global = "gemini-2.0-flash-lite"
            return
        except Exception as e:
            print(f"Google Gemini failed: {e}")

    # Priority 2: Cloudflare Workers AI
    if os.getenv("CF_ACCOUNT_ID") and os.getenv("CF_API_TOKEN"):
        try:
            llm = ChatCloudflareWorkersAI(
                account_id=os.getenv("CF_ACCOUNT_ID"),
                api_token=os.getenv("CF_API_TOKEN"),
                model="@cf/meta/llama-3.1-8b-instruct"
            )
            model_name_global = "llama-3.1-8b-instruct"
            return
        except Exception as e:
            print(f"Cloudflare Workers AI failed: {e}")

    # Priority 3: OpenRouter (Fallback)
    if os.getenv("OPENROUTER_API_KEY"):
        llm = ChatOpenAI(
            model="deepseek/deepseek-chat-v3.1-free",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )
        model_name_global = "deepseek-chat-v3.1-free"
        return

    # Emergency fallback
    llm = EmergencyFallback()
    model_name_global = "emergency-fallback"

```

**Fallback Strategy:**
- Providers are tried sequentially based on environment variable availability
- Each provider has independent error handling
- Emergency fallback returns mock responses if all providers fail
- Global `model_name_global` variable tracks active provider

### 5. Infrastructure Layer

#### Railway Cloud Platform
```railway.json```
```json
{
    "build": {
        "builder": "Dockerfile"
    },
    "deploy": {
        "start": "uvicorn api:app --host 0.0.0.0 --port $PORT",
        "healthcheck": "/health"
    }
}
```

#### Docker Containerization
```docker
FROM python:3.11
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Data Flow Architecture

### Request Processing Flow:
- HTTP Request → FastAPI Router

- Pydantic Validation → BriefRequest schema

- Business Logic → LangGraph workflow initialization

- State Management → AdvancedResearchState creation

- Node Execution → Sequential workflow processing
    - a. Planning Node → Research question generation
    - b. Search Node → Web search and source collection
    - c. Summarization Node → Source analysis and scoring
    - d. Synthesis Node → Final brief compilation

- Response Formatting → BriefResponse schema

- HTTP Response → JSON with comprehensive data

### Error Flow Architecture:
```bash
                +-------------------+
                |  Error Detected   |
                +--------+----------+
                         |
         +---------------+------------------+
         |               |                  |
+--------v-----+  +------v-------+   +------v-------+
| Validation   |  | Processing   |   | External API |
| Error        |  | Error        |   | Error        |
+-------+------+  +------+-------+   +------+-------+
        |                |                  |
  +-----v-----+    +-----v-----+      +-----v-----+
  | 422       |    | Fallback  |      | Retry     |
  | Response  |    | Strategy  |      | Logic     |
  +-----------+    +-----+-----+      +-----+-----+
                        |                  |
                 +------v-----+      +-----v------+
                 | 500        |      | Graceful   |
                 | Response   |      | Degradation|
                 | (last      |      +------------+
                 |  resort)   |
                 +------------+
```

## Security Architecture

### Input Security:
- **Schema Validation**: Strict Pydantic validation prevents injection
- **Length Limits**: All text fields have maximum length restrictions  
- **Type Safety**: Strong typing prevents type confusion attacks
- **Sanitization**: Input sanitization for external API calls

### API Security:
- **CORS Policy**: Configurable cross-origin resource sharing
- **Rate Limiting**: Infrastructure-level protection via Railway
- **Error Information**: Minimal error disclosure to prevent information leakage
- **Health Checks**: Non-sensitive system status information only

### Environment Security:
- **Secret Management**: Multiple provider API keys via environment variables
  - `GOOGLE_API_KEY` for Google Gemini
  - `CF_ACCOUNT_ID` + `CF_API_TOKEN` for Cloudflare
  - `OPENROUTER_API_KEY` for OpenRouter
- **Provider Isolation**: Each provider has independent credential management
- **Container Isolation**: Docker containerization for process isolation
- **HTTPS Enforcement**: Automatic SSL/TLS via Railway infrastructure
- **Logging Security**: No API keys or sensitive data in logs
- **Fallback Security**: Emergency fallback doesn't expose provider failures


## Performance Architecture

### Response Time Optimization:
- **Async Processing**: FastAPI async/await for concurrent operations
- **Parallel Requests**: Concurrent LLM calls where possible
- **Caching Strategy**: State-based caching within workflow
- **Resource Management**: Memory and CPU optimization

### Scalability Design:
- **Stateless Architecture**: No server-side session storage
- **Horizontal Scaling**: Railway auto-scaling based on demand
- **Resource Efficiency**: Optimized memory usage and garbage collection
- **Connection Pooling**: Efficient HTTP client connection management

### Monitoring & Observability:
#### Provider Tracking
Active LLM provider is stored in `model_name_global` for:
- Performance metrics per provider
- Error tracking and debugging
- Cost attribution
- API response logging

#### Performance tracking at each workflow node
```python
start_time = time.time()

# ... processing ...
processing_time = time.time() - start_time
print(f"Node {node_name} completed in {processing_time:.2f}s")
```

## Testing Architecture

### Test Strategy:
```bash
Unit Tests (test_api.py)
├── Health Endpoint Tests
├── Brief Generation Tests
├── Validation Tests
├── Error Handling Tests
└── Status Monitoring Tests

Integration Tests (test_deployed_api.py)
├── Live API Testing
├── End-to-End Workflow Tests
├── Performance Benchmarking
└── Error Recovery Testing```
```

### Test Patterns:
- **Mock Strategy**: Mock external APIs for consistent testing
- **Fixture Management**: Reusable test data and configurations
- **Edge Case Testing**: Boundary conditions and error scenarios
- **Performance Testing**: Response time and resource usage validation

## Deployment Architecture

### CI/CD Pipeline:
Local Development → Git Push → Railway Detection →
Docker Build → Container Deploy → Health Check →
Live Traffic → Monitoring


### Environment Management:
- **Development**: Local development with test APIs
- **Staging**: Railway review apps for testing
- **Production**: Railway production deployment with monitoring

### Configuration Management:
```python
# Environment-based configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Multi-provider LLM configuration (priority order)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Primary
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")    # Secondary
CF_API_TOKEN = os.getenv("CF_API_TOKEN")      # Secondary
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Tertiary

# At least one provider must be configured
if not any([GOOGLE_API_KEY, (CF_ACCOUNT_ID and CF_API_TOKEN), OPENROUTER_API_KEY]):
    raise ValueError("At least one LLM provider must be configured")

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

```

## Future Architecture Considerations

### Scalability Enhancements:
- **Database Integration**: User research history and preferences
- **Caching Layer**: Redis for frequently requested research topics
- **API Gateway**: Kong or similar for advanced rate limiting and analytics
- **Message Queue**: Async processing for long-running research tasks

### LLM Provider Enhancements:
- **Provider Pool Management**: Dynamic load balancing across multiple providers
- **Cost Analytics**: Track token usage and cost per provider
- **Provider Health Monitoring**: Real-time availability checks
- **Smart Routing**: AI-driven provider selection based on task complexity
- **Regional Failover**: Geographic provider distribution for latency optimization
- **Custom Provider Support**: Plugin architecture for new LLM providers

### Feature Extensions:
- **Multi-tenant Architecture**: Separate namespaces per organization
- **Authentication Service**: JWT-based authentication and authorization
- **Analytics Platform**: Usage metrics and research insights
- **WebSocket Support**: Real-time progress updates for long-running requests

---

**Architecture Documentation Version**: 1.0.0  
**Last Updated**: October 17, 2025  
**System Version**: 1.0.0
