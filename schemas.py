# schemas.py - Your Data Models
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum

class ResearchDepth(str, Enum):
    """Depth levels for research"""
    BASIC = "basic"
    DETAILED = "detailed" 
    COMPREHENSIVE = "comprehensive"

class ResearchPlan(BaseModel):
    """Schema for research planning step"""
    topic: str = Field(..., description="The research topic")
    research_questions: List[str] = Field(..., min_items=2, max_items=5)
    search_queries: List[str] = Field(..., min_items=3, max_items=8)
    expected_sources: int = Field(..., ge=3, le=15)
    estimated_time_minutes: int = Field(..., ge=5, le=60)
    depth_level: ResearchDepth
    
    @field_validator('search_queries')
    def validate_queries(cls, v):
        """Ensure search queries are meaningful"""
        for query in v:
            if len(query.strip()) < 5:
                raise ValueError("Search queries must be at least 5 characters")
        return v

class SourceSummary(BaseModel):
    """Schema for individual source summaries"""
    url: str = Field(..., description="Source URL")
    title: str = Field(..., max_length=200)
    summary: str = Field(..., min_length=50, max_length=500)
    key_points: List[str] = Field(..., min_items=2, max_items=6)
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    credibility_score: float = Field(..., ge=0.0, le=1.0)
    source_type: Literal["academic", "news", "blog", "official", "other", "web"]
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com/article",
                "title": "AI in Healthcare: 2025 Trends",
                "summary": "This article discusses emerging AI applications...",
                "key_points": ["AI diagnostics improving", "Regulatory challenges"],
                "relevance_score": 0.85,
                "credibility_score": 0.90,
                "source_type": "academic"
            }
        }

class ContextSummary(BaseModel):
    """Schema for user context from previous briefs"""
    user_id: str
    previous_topics: List[str]
    common_themes: List[str]
    research_preferences: Optional[str] = None
    last_updated: datetime

class FinalBrief(BaseModel):
    """Schema for the complete research brief - YOUR ASSIGNMENT OUTPUT"""
    topic: str = Field(..., min_length=5, description="Research topic to investigate")
    depth: int = Field(..., ge=1, le=5, description="Research depth (1=basic, 5=comprehensive)")
    user_id: str = Field(..., min_length=1, description="Unique identifier for the user")
    follow_up: bool = Field(default=False, description="Is this a follow-up to previous research?")
    
    # WHY: Add summary_length as optional parameter with validation
    # WHAT: Allows users to control summary length, defaults to 300 words for existing users
    summary_length: Optional[int] = Field(
        default=300,                    # WHY: Reasonable default for most use cases
        ge=50,                         # WHY: Minimum 50 words for meaningful summaries
        le=2000,                       # WHY: Maximum 2000 words to prevent excessive output
        description="Desired summary length in words (50-2000, default: 300)"
    )
    
    # Research content
    executive_summary: str = Field(..., min_length=100, max_length=300)
    research_questions: List[str]
    key_findings: List[str] = Field(..., min_items=3, max_items=8)
    detailed_analysis: str = Field(..., min_length=200, max_length=1000)
    
    # Sources and metadata  
    sources: List[SourceSummary] = Field(..., min_items=2, max_items=10)
    context_used: Optional[ContextSummary] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    processing_time_seconds: Optional[float] = None
    total_tokens_used: Optional[int] = None
    
    class Config:
        schema_extra = {
            "example": {
                "topic": "AI in Healthcare 2025",
                "depth": 3,
                "user_id": "user_123",
                "follow_up": False,
                "executive_summary": "AI in healthcare is transforming...",
                "research_questions": ["How is AI improving diagnostics?"],
                "key_findings": ["AI reduces diagnosis time by 40%"],
                "detailed_analysis": "The healthcare industry...",
                "sources": [],
                "created_at": "2025-09-12T00:26:00Z"
            }
        }
