# api.py - This file creates web endpoints that others can call over HTTP
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
import time
import uuid
from datetime import datetime

# Import your existing workflow
from advanced_workflow import create_advanced_workflow, AdvancedResearchState
from schemas import FinalBrief

# WHY: FastAPI() creates our web application instance
# WHAT: This is like opening a restaurant - you need a place to serve customers
app = FastAPI(
    title="Research Brief Generator API",          # WHY: Shows up in auto-generated docs
    description="AI-powered research assistant using LangGraph and LangChain",  # WHY: Explains what your API does
    version="1.0.0",                             # WHY: Version tracking for updates
    docs_url="/docs",                            # WHY: Auto-generated interactive documentation
    redoc_url="/redoc"                           # WHY: Alternative documentation format
)

# WHY: CORS allows websites to call your API from browsers
# WHAT: Without this, web apps can't use your API due to browser security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # WHY: "*" means any website can call your API (use specific domains in production)
    allow_credentials=True,        # WHY: Allows cookies/authentication
    allow_methods=["*"],          # WHY: Allows GET, POST, PUT, DELETE etc.
    allow_headers=["*"],          # WHY: Allows any HTTP headers
)

# WHY: We define request/response schemas so users know what to send/expect
# WHAT: This is like a menu at a restaurant - shows what you can order and what you get
class BriefRequest(BaseModel):
    """
    WHY: This defines what data users must send to create a research brief
    WHAT: Pydantic automatically validates incoming requests against this schema
    """
    topic: str = Field(..., min_length=5, max_length=200, description="Research topic to investigate")
    depth: int = Field(default=3, ge=1, le=5, description="Research depth (1=basic, 5=comprehensive)")
    follow_up: bool = Field(default=False, description="Is this a follow-up to previous research?")
    user_id: str = Field(..., min_length=1, description="Unique identifier for the user")

class BriefResponse(BaseModel):
    """
    WHY: This defines what users will receive back from the API
    WHAT: Ensures consistent response format and auto-generates documentation
    """
    success: bool = Field(..., description="Whether the request was successful")
    brief_id: str = Field(..., description="Unique identifier for this research brief")
    brief: Optional[FinalBrief] = Field(None, description="The completed research brief")
    error: Optional[str] = Field(None, description="Error message if request failed")
    processing_time: Optional[float] = Field(None, description="Time taken to generate brief in seconds")
    created_at: datetime = Field(default_factory=datetime.now, description="When this brief was created")

class HealthResponse(BaseModel):
    """
    WHY: Health checks let users/systems verify your API is running
    WHAT: Like checking if a store is open before driving there
    """
    status: str = Field(..., description="API health status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Current server time")
    version: str = Field(default="1.0.0", description="API version")

# WHY: We store active requests to prevent duplicate processing
# WHAT: Like a ticket system - each request gets a number and status
active_requests = {}

# WHY: GET endpoints are for retrieving information (like viewing a webpage)
# WHAT: This endpoint lets users check if your API is working
@app.get("/", response_model=HealthResponse)
async def root():
    """
    Root endpoint - like the homepage of your API
    
    WHY: Every API needs a root endpoint for basic connectivity testing
    WHAT: Returns basic info about your API
    WHEN: Users can call this anytime to check if API is alive
    """
    return HealthResponse(
        status="online",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - like asking "Are you open?"
    
    WHY: Load balancers and monitoring systems use this to check service health
    WHAT: Returns detailed health information
    WHEN: Called frequently by monitoring systems
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

# WHY: POST endpoints are for creating/submitting new data (like filling out a form)
# WHAT: This is the main endpoint where users request research briefs
@app.post("/brief", response_model=BriefResponse)
async def generate_brief(request: BriefRequest, background_tasks: BackgroundTasks):
    """
    Generate a research brief - the main function of your API
    
    WHY: This is what users came for - to get AI-generated research briefs
    WHAT: Takes a research topic and returns a comprehensive brief with sources
    HOW: Uses your LangGraph workflow to process the request
    """
    
    # WHY: Generate unique ID for tracking this specific request
    # WHAT: Like giving each customer a receipt number
    brief_id = str(uuid.uuid4())
    start_time = time.time()
    
    print(f"🎯 API: Starting brief generation for topic: '{request.topic}'")
    print(f"📊 Request ID: {brief_id}")
    print(f"👤 User: {request.user_id}")
    print(f"🔍 Depth: {request.depth}/5")
    
    try:
        # WHY: Create workflow instance for this specific request
        # WHAT: Like assigning a chef to prepare this specific order
        workflow_app = create_advanced_workflow()
        
        # WHY: Prepare initial state with user's request data
        # WHAT: Like giving the chef the order details and ingredients
        initial_state = {
            "topic": request.topic,
            "depth": request.depth,
            "user_id": request.user_id,
            "follow_up": request.follow_up,
            "research_plan": None,
            "raw_search_results": None,
            "source_summaries": None,
            "final_brief": None,
            "start_time": start_time,
            "errors": None,
            "current_step": "starting"
        }
        
        # WHY: Add to active requests for tracking
        # WHAT: Like putting the order on the kitchen board
        active_requests[brief_id] = {
            "status": "processing",
            "started_at": datetime.now(),
            "topic": request.topic
        }
        
        print(f"🚀 Starting workflow execution...")
        
        # WHY: Execute the actual research workflow
        # WHAT: This runs your entire LangGraph pipeline (search, summarize, synthesize)
        # HOW: The workflow processes through all nodes until completion
        final_state = workflow_app.invoke(initial_state)
        
        # WHY: Calculate processing time for performance monitoring
        # WHAT: Like timing how long it takes to prepare a dish
        processing_time = time.time() - start_time
        
        print(f"✅ Workflow completed in {processing_time:.2f} seconds")
        
        # WHY: Check if workflow completed successfully
        # WHAT: Like checking if the chef finished the dish properly
        if final_state.get("final_brief"):
            brief = final_state["final_brief"]
            
            # WHY: Remove from active requests since it's done
            # WHAT: Like clearing the completed order from the kitchen board
            if brief_id in active_requests:
                del active_requests[brief_id]
            
            print(f"🎉 Successfully generated brief with {len(brief.sources)} sources")
            
            # WHY: Return success response with the generated brief
            # WHAT: Like serving the completed dish to the customer
            return BriefResponse(
                success=True,
                brief_id=brief_id,
                brief=brief,
                error=None,
                processing_time=processing_time,
                created_at=datetime.now()
            )
        else:
            # WHY: Handle case where workflow didn't produce a brief
            # WHAT: Like when the kitchen can't complete an order
            error_msg = "Workflow completed but no brief was generated"
            if final_state.get("errors"):
                error_msg = f"Workflow errors: {', '.join(final_state['errors'])}"
            
            print(f"❌ Workflow failed: {error_msg}")
            
            # WHY: Clean up failed request
            if brief_id in active_requests:
                del active_requests[brief_id]
            
            # WHY: Return error response instead of crashing
            # WHAT: Like politely telling the customer the dish isn't available
            return BriefResponse(
                success=False,
                brief_id=brief_id,
                brief=None,
                error=error_msg,
                processing_time=time.time() - start_time,
                created_at=datetime.now()
            )
            
    except Exception as e:
        # WHY: Catch any unexpected errors to prevent API crashes
        # WHAT: Like having a backup plan when something goes wrong in the kitchen
        processing_time = time.time() - start_time
        error_msg = f"Internal server error: {str(e)}"
        
        print(f"💥 API Error: {error_msg}")
        
        # WHY: Clean up failed request
        if brief_id in active_requests:
            del active_requests[brief_id]
        
        # WHY: Return proper error response instead of letting the API crash
        # WHAT: Like having good customer service when problems occur
        return BriefResponse(
            success=False,
            brief_id=brief_id,
            brief=None,
            error=error_msg,
            processing_time=processing_time,
            created_at=datetime.now()
        )

@app.get("/status/{brief_id}")
async def get_brief_status(brief_id: str):
    """
    Check the status of a research brief request
    
    WHY: For long-running requests, users want to know progress
    WHAT: Like asking "Is my food ready yet?"
    WHEN: Users can check anytime while their brief is being generated
    """
    if brief_id in active_requests:
        return {
            "brief_id": brief_id,
            "status": "processing",
            "details": active_requests[brief_id]
        }
    else:
        return {
            "brief_id": brief_id,
            "status": "completed_or_not_found",
            "details": None
        }

@app.get("/active")
async def get_active_requests():
    """
    Get list of currently processing requests
    
    WHY: For monitoring and debugging - see what's currently happening
    WHAT: Like looking at all orders currently being prepared
    WHEN: Admins/developers use this to monitor system load
    """
    return {
        "active_count": len(active_requests),
        "requests": active_requests
    }

# WHY: This block only runs when you execute this file directly (not when imported)
# WHAT: Standard Python pattern for making modules both importable and executable
if __name__ == "__main__":
    
    # WHY: Import uvicorn inside the main block (not at top) for cleaner module structure
    # WHAT: uvicorn is the ASGI server that actually serves our FastAPI application
    import uvicorn
    
    # WHY: Print helpful startup messages before starting the server
    # WHAT: Gives users clear information about what's happening and where to find docs
    print("🚀 Starting Research Brief Generator API...")
    print("📚 Documentation available at: http://localhost:8000/docs")
    print("🔄 Alternative docs at: http://localhost:8000/redoc")
    print("❤️  Health check at: http://localhost:8000/health")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # WHY: Use string reference "api:app" instead of direct app object
    # WHAT: This tells uvicorn to import the app from the api module, enabling reload functionality
    # WHY: "api:app" means "from the api module, get the app variable"
    # WHAT: This allows uvicorn to restart the server when code changes are detected
    uvicorn.run(
        "api:app",                    # ← FIXED: String reference instead of app object
        host="0.0.0.0",              # WHY: "0.0.0.0" accepts connections from any IP address
        port=8000,                   # WHY: Port 8000 is the standard FastAPI development port
        reload=True,                 # WHY: Auto-restart server when code changes (development feature)
        log_level="info",            # WHY: Show informational logs for debugging and monitoring
        access_log=True,             # WHY: Log all HTTP requests for monitoring and debugging
        reload_dirs=["./"],          # WHY: Watch current directory for file changes
        reload_excludes=["*.pyc", "__pycache__", "*.log"]  # WHY: Don't reload for temporary files
    )
