# Contributing to Research Brief Generator

Thank you for your interest in contributing to the Research Brief Generator! This guide will help you get started with development, testing, and submitting contributions.

## 🚀 **Quick Start for Contributors**

### Prerequisites
- Python 3.11+ (3.12 recommended)
- Git
- OpenRouter API key
- Basic knowledge of LangChain and LangGraph

### Development Setup

1. **Clone and Setup**
    ```git
    git clone https://github.com/your-username/research-brief-generator.git
    cd research-brief-generator
    ```
    Create virtual environment
    ```powershell
    python -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate
    ```
    Install dependencies
    ```powershell
    pip install -r requirements.txt
    pip install -r requirements-dev.txt # Development dependencies
    ```


2. **Environment Configuration**

    Copy environment template
    ```powershell
    cp .env.example .env
    ```

    - Edit .env with your API keys
    - Required: OPENROUTER_API_KEY
    - Optional: LANGSMITH_API_KEY (for tracing)


3. **Verify Installation**
```powershell
# Run tests
pytest test_workflow.py -v

# Start development server
python api.py

# Test CLI
python cli.py --topic "test" --depth 1 --dry-run
```

## 📋 **Development Guidelines**

### **Code Style & Standards**

#### **Python Code Standards**
```python
# Use type hints for all functions
def process_research_data(topic: str, depth: int) -> Dict[str, Any]:
    """
    Process research data with proper typing.
    Args:
        topic: Research topic string
        depth: Research depth level (1-5)
        
    Returns:
        Processed research data dictionary
    """
    pass

# Use descriptive variable names
research_plan = create_research_plan(topic) # Good
rp = create_plan(t) # Bad

# Follow PEP 8 formatting
class ResearchProcessor:
    """Process research requests with monitoring."""
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.token_tracker = TokenTracker()
```

#### **Code Formatting Tools**

Format code with Black
- ```black .```

Sort imports with isort
- ```isort .```

Lint with flake8
- ```flake8 .```

Type checking with mypy
```pip 
mypy advanced_workflow.py api.py schemas.py
```

#### **Documentation Standards**
- All public functions must have docstrings
- Use Google-style docstring format
- Include type hints for parameters and return values
- Add inline comments for complex logic
- Update README.md for new features

### **Testing Requirements**

#### **Test Coverage Standards**
Minimum 80% code coverage required
```pip 
pytest test_workflow.py --cov=. --cov-report=term-missing --cov-fail-under=80
```

Test categories required:
1. Unit tests for individual functions
2. Integration tests for workflow nodes
3. End-to-end tests for complete workflows
4. Performance benchmarks for critical paths


#### **Writing Tests**
```python
class TestNewFeature:
"""Test new feature functionality."""
@pytest.fixture
def sample_data(self):
    """Provide test data."""
    return {"topic": "test", "depth": 2}

def test_feature_success_case(self, sample_data):
    """Test successful feature execution."""
    result = new_feature_function(sample_data)
    
    # Assert expected behavior
    assert result["status"] == "success"
    assert "data" in result
    
    # Verify monitoring integration
    stats = token_tracker.get_current_stats()
    assert stats["total_tokens"] > 0

def test_feature_error_handling(self):
    """Test feature error handling."""
    with pytest.raises(ValueError):
        new_feature_function(invalid_data)

@pytest.mark.performance
def test_feature_performance(self):
    """Test feature performance benchmark."""
    start_time = time.time()
    result = new_feature_function(large_dataset)
    duration = time.time() - start_time
    
    # Assert performance requirements
    assert duration < 5.0  # Must complete within 5 seconds
    assert result["efficiency"] > 0.8  # Must be 80%+ efficient
```

### **Monitoring Integration**

All new features must include monitoring integration:

```python
def new_workflow_node(state: AdvancedResearchState):
"""New workflow node with monitoring."""
node_start_time = time.time() # Start timing

try:
    # Your feature logic here
    input_tokens = count_tokens(input_data)
    result = process_data(input_data)
    output_tokens = count_tokens(result)
    
    # Record successful monitoring
    node_duration = time.time() - node_start_time
    performance_monitor.record_node_performance("new_node", node_duration, True)
    token_tracker.track_usage(model_name, "new_node", input_tokens, output_tokens)
    
    return {"result": result, "current_step": "new_node_completed"}
    
except Exception as e:
    # Record failed monitoring
    node_duration = time.time() - node_start_time
    performance_monitor.record_node_performance("new_node", node_duration, False)
    
    return {"errors": [str(e)], "current_step": "new_node_failed"}

```
## 🔄 **Contribution Workflow**

### **Branching Strategy**

```text
main # Production-ready code
├─ develop # Integration branch for features
├─ feature/* # Feature development branches
├─ bugfix/* # Bug fix branches
├─ hotfix/* # Critical production fixes
└─ release/* # Release preparation branches
```
### **Pull Request Process**

1. **Create Feature Branch**
```git
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

2. **Development Cycle**

Make changes
```git
git add .
git commit -m "feat: add new research optimization feature"
```
Follow conventional commit format:
- feat: new feature
- fix: bug fix
- docs: documentation changes
- style: formatting changes
- refactor: code refactoring
- test: adding tests
- perf: performance improvements


3. **Pre-submission Checklist**
- [ ] All tests pass: `pytest test_workflow.py -v`
- [ ] Code coverage ≥ 80%: `pytest --cov=. --cov-report=term-missing`
- [ ] Code formatted: `black . && isort .`
- [ ] Linting clean: `flake8 .`
- [ ] Type checking passes: `mypy *.py --ignore-missing-imports`
- [ ] Documentation updated
- [ ] Monitoring integration added
- [ ] Performance benchmarks included

4. **Submit Pull Request**

    Pull Request Template
    🎯 What does this PR do?
    Brief description of changes and motivation

    **🧪 Testing**
    - Unit tests added/updated

    - Integration tests pass

    - Performance benchmarks included

    -  Manual testing completed

    **📊 Monitoring**
    - Token tracking integrated

    - Performance monitoring added

    - Error handling implemented

    - Metrics endpoint updated

    **📚 Documentation**
    - Code documentation updated

    - README.md updated (if needed)

    - API documentation updated (if needed)

    **🔍 Review Checklist**
    - Code follows style guidelines

    - Test cover new functionality

    - No breaking changes (or properly documented)

    - Performance impact assessed


### **Code Review Guidelines**

#### **For Contributors**
- Respond to feedback promptly and constructively
- Make requested changes in separate commits
- Ask questions if feedback is unclear
- Test thoroughly after making changes

#### **For Reviewers**
- Focus on code quality, performance, and maintainability
- Provide specific, actionable feedback
- Suggest improvements rather than just pointing out issues
- Test the changes locally when possible

## 🎯 **Areas for Contribution**

### **High Priority**
1. **Performance Optimization**
   - Async processing implementation
   - Caching strategies
   - Memory optimization
   - Token usage optimization

2. **Enhanced Monitoring**
   - Advanced metrics collection
   - Real-time dashboards
   - Alert system integration
   - Custom monitoring plugins

3. **Model Integration**
   - New LLM model support
   - Model performance comparison
   - Dynamic model selection
   - Cost optimization strategies

### **Medium Priority**
1. **User Experience**
   - Web UI development
   - CLI improvements
   - Configuration management
   - Error message improvements

2. **API Enhancements**
   - Rate limiting improvements
   - Authentication systems
   - API versioning
   - Response format options

3. **Documentation**
   - Tutorial creation
   - Video guides
   - API reference expansion
   - Troubleshooting guides

### **Good First Issues**
- Fix typos in documentation
- Add more test cases
- Improve error messages
- Add configuration validation
- Create example scripts
- Update dependency versions

## 📊 **Performance Benchmarks**

### **Required Benchmarks for New Features**
```python
class TestYourFeaturePerformance:
"""Performance benchmarks for new feature."""
@pytest.mark.benchmark
def test_feature_latency(self):
    """Benchmark feature response time."""
    # Target: < 5 seconds for typical usage
    start_time = time.time()
    result = your_feature()
    duration = time.time() - start_time
    
    assert duration < 5.0
    print(f"Feature latency: {duration:.2f}s")

@pytest.mark.benchmark  
def test_feature_throughput(self):
    """Benchmark feature throughput."""
    # Target: > 10 operations per minute
    start_time = time.time()
    for _ in range(10):
        your_feature()
    duration = time.time() - start_time
    
    throughput = 10 / (duration / 60)  # operations per minute
    assert throughput > 10
    print(f"Feature throughput: {throughput:.2f} ops/min")

@pytest.mark.benchmark
def test_memory_usage(self):
    """Benchmark memory usage."""
    import psutil, os
    
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / 1024 / 1024  # MB
    
    result = your_feature()
    
    memory_after = process.memory_info().rss / 1024 / 1024  # MB
    memory_delta = memory_after - memory_before
    
    # Target: < 100MB memory increase
    assert memory_delta < 100
    print(f"Memory usage: {memory_delta:.2f}MB")
```


### **Performance Targets**
| Component | Target | Current | Status |
|-----------|--------|---------|--------|
| Planning Node | < 5s | 3-5s | ✅ |
| Search Node | < 30s | 10-30s | ✅ |
| Summarization | < 15s | 5-15s | ✅ |
| Synthesis | < 20s | 8-20s | ✅ |
| Total Workflow | < 60s |
