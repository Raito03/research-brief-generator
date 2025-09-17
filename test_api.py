# test_api.py - FINAL working version with detailed explanations
# WHY: This is the filename - indicates this is the corrected, final version of our API tests
# WHAT: A comprehensive test suite that validates our research brief API functionality

# WHY: Import pytest - the testing framework that discovers and runs our tests
# WHAT: pytest provides assert statements, test discovery, fixtures, and test execution
import pytest

# WHY: Import TestClient from FastAPI - allows testing without starting a real web server
# WHAT: TestClient simulates HTTP requests and responses for our FastAPI application
from fastapi.testclient import TestClient

# WHY: Import patch and MagicMock for mocking external dependencies during tests
# WHAT: patch replaces real functions temporarily, MagicMock creates fake objects with predictable behavior
from unittest.mock import patch, MagicMock

# WHY: Import datetime for creating timestamp data in our test objects
# WHAT: datetime provides current time functionality needed for our test data structures
from datetime import datetime

# WHY: Import our main API application that we want to test
# WHAT: app is the FastAPI instance containing all endpoints and business logic
from api import app

# WHY: Import our Pydantic models to create valid test data structures
# WHAT: These schemas define the exact structure and validation rules for our API data
from schemas import FinalBrief, SourceSummary

# WHY: Create a TestClient instance to simulate HTTP requests to our API
# WHAT: client acts like a web browser or API client, making requests without network calls
client = TestClient(app)

class TestHealthEndpoints:
    """
    WHY: Group health-related tests together for logical organization
    WHAT: Contains tests for basic API connectivity and health monitoring endpoints
    """
    
    def test_root_endpoint(self):
        """
        WHY: Verify the root endpoint works correctly and returns expected data
        WHAT: Tests that GET / returns proper health status information for monitoring
        """
        # WHY: Send a GET request to the root URL of our API
        # WHAT: Simulates accessing http://localhost:8000/ in a web browser
        response = client.get("/")
        
        # WHY: Assert that the HTTP status code is 200 (successful request)
        # WHAT: 200 means "OK" - the request was processed successfully
        assert response.status_code == 200
        
        # WHY: Parse the JSON response body into a Python dictionary
        # WHAT: Converts the HTTP response from JSON string to Python data structure
        data = response.json()
        
        # WHY: Verify the response contains the expected status field with correct value
        # WHAT: Confirms our API correctly reports that it's online and operational
        assert data["status"] == "online"
        
        # WHY: Check that the response includes a timestamp field
        # WHAT: Ensures our API provides timing information for monitoring purposes
        assert "timestamp" in data
        
        # WHY: Verify the response includes version information
        # WHAT: Confirms our API reports its version number for tracking and debugging
        assert "version" in data
    
    def test_health_check(self):
        """
        WHY: Test the dedicated health endpoint used by monitoring systems and load balancers
        WHAT: Verifies that GET /health returns detailed operational status information
        """
        # WHY: Make a GET request to the health check endpoint
        # WHAT: Simulates a monitoring system checking if our API is healthy and responsive
        response = client.get("/health")
        
        # WHY: Confirm the request completed successfully with 200 status
        # WHAT: Ensures the health endpoint is accessible and functioning properly
        assert response.status_code == 200
        
        # WHY: Convert the JSON response to a Python dictionary for inspection
        # WHAT: Allows us to examine individual fields in the health status response
        data = response.json()
        
        # WHY: Verify the health status reports "healthy"
        # WHAT: Confirms our API indicates it's fully operational and ready to serve requests
        assert data["status"] == "healthy"

class TestBriefGeneration:
    """
    WHY: Group all tests related to the core research brief generation functionality
    WHAT: Contains tests for the main business logic - creating AI-powered research briefs
    """
    
    def test_valid_brief_request(self):
        """
        WHY: Test that valid requests successfully generate research briefs
        WHAT: This is our most critical test - validates the core product functionality
        """
        # WHY: Create a dictionary with realistic, valid request data
        # WHAT: Simulates what a real user would send when requesting a research brief
        request_data = {
            # WHY: A realistic research topic that our AI can actually research
            # WHAT: The subject matter the user wants to learn about
            "topic": "artificial intelligence in healthcare",
            
            # WHY: Medium research depth on our 1-5 scale
            # WHAT: Indicates how thorough and detailed the research should be
            "depth": 3,
            
            # WHY: This is not a follow-up to previous research
            # WHAT: Boolean flag that affects how the research pipeline processes the request
            "follow_up": False,
            
            # WHY: Unique identifier for this test user
            # WHAT: Allows tracking and associating requests with specific users
            "user_id": "test_user_123"
        }
        
        # WHY: Use patch to replace the real workflow with a controllable fake version
        # WHAT: Prevents tests from running the actual AI pipeline (slow, expensive, unpredictable)
        with patch('api.create_advanced_workflow') as mock_workflow:
            # WHY: Create a fake workflow application instance
            # WHAT: MagicMock simulates the real workflow with predictable, controllable behavior
            mock_app = MagicMock()
            
            # WHY: Configure our fake workflow creator to return our fake app
            # WHAT: When the API calls create_advanced_workflow(), it gets our controllable fake
            mock_workflow.return_value = mock_app
            
            # WHY: Create the FIRST real SourceSummary object (we need at least 2!)
            # WHAT: Represents a research source with all required fields and proper validation
            source1 = SourceSummary(
                # WHY: URL field must be a valid string representing the source location
                # WHAT: Where this research information originally came from
                url="https://example.com/ai-healthcare-diagnosis",
                
                # WHY: Title field provides a human-readable name for this source
                # WHAT: Brief description of what this source is about
                title="AI Revolutionizes Medical Diagnosis",
                
                # WHY: Summary field must be 50-500 characters to meet schema requirements
                # WHAT: Detailed description of the source content and its relevance
                summary="This comprehensive study examines how artificial intelligence technologies are transforming medical diagnostic procedures, improving accuracy and reducing time to diagnosis.",
                
                # WHY: Key points must be a list with 2-6 items per our schema validation
                # WHAT: Most important insights and findings from this particular source
                key_points=[
                    "AI reduces diagnostic errors by 40% compared to traditional methods",
                    "Machine learning algorithms can detect diseases earlier than human physicians"
                ],
                
                # WHY: Relevance score (0.0-1.0) indicates how closely this relates to the research topic
                # WHAT: 0.9 means this source is highly relevant to "AI in healthcare"
                relevance_score=0.9,
                
                # WHY: Credibility score (0.0-1.0) indicates how trustworthy this source appears
                # WHAT: 0.85 means this is a highly credible and reliable source
                credibility_score=0.85,
                
                # WHY: Source type categorizes where this information originated
                # WHAT: "web" indicates this came from a web search result
                source_type="web"
            )
            
            # WHY: Create the SECOND real SourceSummary object (REQUIRED for schema validation!)
            # WHAT: Our schema requires minimum 2 sources, so we must provide at least 2
            source2 = SourceSummary(
                # WHY: Different URL to represent a second, distinct research source
                # WHAT: Another location where relevant research information was found
                url="https://example.com/ai-healthcare-implementation",
                
                # WHY: Different title to show this is a separate source with different focus
                # WHAT: This source focuses on implementation challenges rather than diagnosis
                title="Challenges in Healthcare AI Implementation",
                
                # WHY: Different summary content while maintaining 50-500 character requirement
                # WHAT: Describes the specific focus and findings of this second source
                summary="An in-depth analysis of barriers and opportunities in implementing AI systems within healthcare institutions, covering regulatory, technical, and cultural challenges.",
                
                # WHY: Different key points to show diverse research findings
                # WHAT: Unique insights from this source that complement the first source
                key_points=[
                    "Data privacy regulations create significant implementation hurdles",
                    "Healthcare professionals require extensive training on AI tools"
                ],
                
                # WHY: Slightly different relevance score to show realistic variation
                # WHAT: 0.8 means this source is also highly relevant but slightly less than source1
                relevance_score=0.8,
                
                # WHY: High credibility score indicating this is also a trustworthy source
                # WHAT: 0.9 means this source has even higher credibility than source1
                credibility_score=0.9,
                
                # WHY: Same source type since both came from web search
                # WHAT: Consistent categorization for sources from the same search method
                source_type="web"
            )
            
            # WHY: Create a real FinalBrief object that passes all schema validation requirements
            # WHAT: Represents the complete research brief that users receive from our API
            real_brief = FinalBrief(
                # WHY: Topic must exactly match what the user requested
                # WHAT: Confirms the AI researched the correct subject matter
                topic="artificial intelligence in healthcare",
                
                # WHY: Depth must match the requested research thoroughness level
                # WHAT: Integer 1-5 indicating how comprehensive the research should be
                depth=3,
                
                # WHY: User ID must match the requester for proper tracking and association
                # WHAT: Links this research brief to the specific user who requested it
                user_id="test_user_123",
                
                # WHY: Follow_up flag indicates whether this builds on previous research
                # WHAT: False means this is a standalone research request, not a continuation
                follow_up=False,
                
                # WHY: Executive summary must be 100-300 characters per schema requirements
                # WHAT: High-level overview that gives users a quick understanding of findings
                executive_summary="AI technologies are revolutionizing healthcare delivery through improved diagnostics, personalized treatment, and operational efficiency enhancements.",
                
                # WHY: Research questions show what specific aspects the AI investigated
                # WHAT: List of focused questions that guided the research methodology
                research_questions=[
                    "How does AI improve diagnostic accuracy in medical practice?",
                    "What are the primary challenges in implementing AI in healthcare settings?"
                ],
                
                # WHY: Key findings must have 3-8 items per our schema validation requirements
                # WHAT: Most important discoveries and insights from the research process
                key_findings=[
                    "AI reduces diagnostic errors by 40% compared to traditional methods",
                    "Machine learning algorithms detect diseases earlier than human physicians",
                    "Data privacy regulations create significant implementation challenges"
                ],
                
                # WHY: Detailed analysis must be 200-1000 characters per schema requirements
                # WHAT: Comprehensive explanation of findings, implications, and insights
                detailed_analysis="The integration of artificial intelligence in healthcare demonstrates transformative potential across multiple domains. Diagnostic accuracy improvements are particularly significant, with AI systems consistently outperforming traditional methods. However, implementation faces substantial regulatory and training challenges that require systematic addressing.",
                
                # WHY: Sources list must contain 2-10 SourceSummary objects per schema (FIXED!)
                # WHAT: Now providing BOTH sources to meet the minimum requirement of 2 sources
                sources=[source1, source2],  # ← FIXED: Now has 2 sources instead of 1!
                
                # WHY: Processing time helps users understand system performance
                # WHAT: How many seconds the AI took to complete this research brief
                processing_time_seconds=10.5
            )
            
            # WHY: Create the mock response data structure that simulates workflow completion
            # WHAT: This represents what the real AI workflow would return upon successful completion
            fake_final_state = {
                # WHY: final_brief key contains the completed research output
                # WHAT: This is the main product that gets returned to users
                "final_brief": real_brief,  # Real Pydantic object, not MagicMock!
                
                # WHY: errors key indicates any problems during processing
                # WHAT: None means the workflow completed successfully without issues
                "errors": None
            }
            
            # WHY: Configure our mock workflow to return our predefined response
            # WHAT: When the API calls mock_app.invoke(), it receives our fake_final_state
            mock_app.invoke.return_value = fake_final_state
            
            # WHY: Execute the actual HTTP POST request to our API endpoint
            # WHAT: Simulates a real user making a research brief request
            response = client.post("/brief", json=request_data)
            
            # WHY: Verify the HTTP request completed successfully
            # WHAT: 200 status code confirms the request was processed without errors
            assert response.status_code == 200
            
            # WHY: Parse the JSON response body into a Python dictionary
            # WHAT: Converts the HTTP response from JSON format to Python data structures
            data = response.json()
            
            # WHY: Confirm the API indicates the operation was successful
            # WHAT: success=True means the research brief was generated successfully
            assert data["success"] is True
            
            # WHY: Verify the response includes a unique identifier for this request
            # WHAT: brief_id allows tracking and referencing this specific research brief
            assert "brief_id" in data
            
            # WHY: Confirm the response contains the actual research brief content
            # WHAT: This is the main deliverable that users requested from our API
            assert data["brief"] is not None
            
            # WHY: Verify the brief contains the correct research topic
            # WHAT: Ensures the AI researched exactly what the user asked for
            assert data["brief"]["topic"] == "artificial intelligence in healthcare"
            
            # WHY: Check that key findings meet our minimum requirement of 3 items
            # WHAT: Our schema validation requires at least 3 key findings
            assert len(data["brief"]["key_findings"]) >= 3
            
            # WHY: Verify that exactly 2 sources are included (our test data)
            # WHAT: Confirms the API properly processed and returned our source data
            assert len(data["brief"]["sources"]) == 2  # ← FIXED: Now expects 2 sources!
            
            # WHY: Confirm performance timing data is included in the response
            # WHAT: processing_time helps users understand system performance characteristics
            assert "processing_time" in data
    
    def test_invalid_brief_request(self):
        """
        WHY: Test that our API properly validates and rejects malformed requests
        WHAT: Ensures input validation works correctly and provides helpful error messages
        """
        # WHY: Create a request with multiple validation violations
        # WHAT: Simulates a user sending incorrectly formatted or incomplete data
        invalid_request = {
            # WHY: Empty topic violates minimum length requirement (needs 5+ characters)
            # WHAT: Tests that our API rejects requests without proper research subjects
            "topic": "",
            
            # WHY: Depth of 10 exceeds our maximum allowed value of 5
            # WHAT: Tests that our API enforces the valid research depth range (1-5)
            "depth": 10,
            
            # WHY: Empty user_id violates minimum length requirement (needs 1+ characters)
            # WHAT: Tests that our API requires proper user identification
            "user_id": ""
        }
        
        # WHY: Send the malformed request to our API endpoint
        # WHAT: Simulates a user making an invalid API call with bad data
        response = client.post("/brief", json=invalid_request)
        
        # WHY: Verify the API returns proper validation error status code
        # WHAT: 422 means "Unprocessable Entity" - the data format/content is invalid
        assert response.status_code == 422  # Validation error
    
    def test_workflow_error_handling(self):
        """
        WHY: Test that our API handles internal processing errors gracefully
        WHAT: Ensures the API doesn't crash when the AI workflow encounters problems
        """
        # WHY: Create valid request data to isolate error handling testing
        # WHAT: We want to test error recovery, not input validation
        request_data = {
            "topic": "test topic", 
            "depth": 2,
            "follow_up": False,
            "user_id": "test_user"
        }
        
        # WHY: Mock the workflow to simulate an internal processing failure
        # WHAT: Tests how our API responds when the AI pipeline encounters errors
        with patch('api.create_advanced_workflow') as mock_workflow:
            # WHY: Create a fake workflow instance for error simulation
            # WHAT: This mock will be configured to throw an exception
            mock_app = MagicMock()
            mock_workflow.return_value = mock_app
            
            # WHY: Configure the fake workflow to raise an exception when invoked
            # WHAT: side_effect makes the mock throw an error instead of returning data
            mock_app.invoke.side_effect = Exception("Simulated internal error")
            
            # WHY: Send a request that will trigger our simulated error condition
            # WHAT: Tests our API's error handling and recovery mechanisms
            response = client.post("/brief", json=request_data)
            
            # WHY: Verify the API doesn't crash (still returns 200, not 500)
            # WHAT: Professional APIs handle internal errors gracefully without crashing
            assert response.status_code == 200
            
            # WHY: Parse the response to examine error handling behavior
            # WHAT: The API should return structured error information, not crash
            data = response.json()
            
            # WHY: Confirm the API correctly reports the operation failed
            # WHAT: success=False indicates something went wrong during processing
            assert data["success"] is False
            
            # WHY: Verify the response includes detailed error information
            # WHAT: Users need to understand what went wrong and why
            assert "error" in data
            
            # WHY: Check that our simulated error message appears in the response
            # WHAT: Confirms error details are properly captured and communicated
            assert "Simulated internal error" in data["error"]

class TestStatusEndpoints:
    """
    WHY: Group tests for administrative and monitoring functionality
    WHAT: Contains tests for endpoints that help administrators monitor system health
    """
    
    def test_get_active_requests(self):
        """
        WHY: Test the endpoint that shows currently processing research requests
        WHAT: Verifies that system administrators can monitor active operations and load
        """
        # WHY: Make a GET request to the active requests monitoring endpoint
        # WHAT: Simulates an administrator checking what requests are currently being processed
        response = client.get("/active")
        
        # WHY: Verify the monitoring request completed successfully
        # WHAT: The administrative endpoint should always be accessible for monitoring
        assert response.status_code == 200
        
        # WHY: Parse the JSON response for detailed inspection
        # WHAT: The response should contain structured data about system activity
        data = response.json()
        
        # WHY: Confirm the response includes a count of currently active requests
        # WHAT: active_count tells administrators how busy the system currently is
        assert "active_count" in data
        
        # WHY: Verify the response includes detailed information about active requests
        # WHAT: requests field contains specifics about each operation in progress
        assert "requests" in data
        
        # WHY: Ensure the active count is a proper integer value
        # WHAT: The count should be numeric for monitoring systems to process correctly
        assert isinstance(data["active_count"], int)

# WHY: This block only executes when running this file directly (not when imported)
# WHAT: Provides a convenient way to run all tests without using pytest command line
if __name__ == "__main__":
    # WHY: Print an informative message indicating test execution is starting
    # WHAT: Gives users clear feedback that the testing process has begun
    print("🧪 Running comprehensive API tests with FIXED schema validation...")
    
    # WHY: Execute pytest on this specific file with verbose output enabled
    # WHAT: pytest.main() discovers and runs all test functions, reporting detailed results
    # WHY: [__file__, "-v"] means "run tests in this file with verbose/detailed output"
    # WHAT: -v flag shows individual test names and their pass/fail status
    pytest.main([__file__, "-v"])
