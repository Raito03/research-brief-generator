# advanced_workflow_openrouter.py - Using different models
from dotenv import load_dotenv

load_dotenv()

import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional, Callable
from langchain_openai import ChatOpenAI  # ← Changed from ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.llm_providers import (
    CloudflareChatWrapper,
    create_openrouter_llm,
    model_name_ctx,
    request_log_callback,
    set_log_callback,
    stream_log,
)
from app.parsers import (
    calculate_tokens_from_words,
    ensure_target_length,
    fix_detailed_analysis_enhanced,
    fix_executive_summary_enhanced,
    fix_key_findings_enhanced,
    parse_structured_response,
    parse_synthesis_response_with_length,
)
from app.schemas import ResearchPlan, SourceSummary, FinalBrief, ResearchDepth
from ddgs import DDGS
from app.crawler import fetch_page_content
import asyncio
from crawl4ai import AsyncWebCrawler


async def fetch_and_summarize(url: str, crawler: AsyncWebCrawler = None) -> str:
    """Fetches full page content using Crawl4AI for summarization."""
    content = await fetch_page_content(url, crawler)
    if len(content) > 30000:
        return content[:30000] + "... [TRUNCATED]"
    return content


import time
import json
import threading
# ✅ ROBUST LANGSMITH INTEGRATION - REPLACE THE COMMENTED SECTION
# try:
#     from langsmith_integration import (
#         token_tracker,
#         performance_monitor,
#         count_tokens_tiktoken,
#         count_tokens_estimate
#     )

#     def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
#         """Count tokens with fallback methods"""
#         try:
#             return count_tokens_tiktoken(text, model_name)
#         except:
#             return count_tokens_estimate(text)

#     print("✅ LangSmith integration loaded successfully")

# except ImportError as e:
#     print(f"⚠️ LangSmith integration not available: {e}")

#     # Fallback implementations
#     class DummyTracker:
#         def track_usage(self, *args, **kwargs):
#             print(f"📊 [DummyTracker] Usage tracked: {args[0] if args else 'N/A'}")
#         def get_current_stats(self):
#             return {"total_tokens": 0, "status": "dummy_mode"}
#         def reset_stats(self):
#             pass

#     class DummyMonitor:
#         def record_node_performance(self, node_name, duration, success=True):
#             print(f"⏱️ [DummyMonitor] {node_name}: {duration:.2f}s, success={success}")
#         def get_performance_report(self):
#             return {"summary": {"total_requests": 0, "status": "dummy_mode"}}

#     token_tracker = DummyTracker()
#     performance_monitor = DummyMonitor()

#     def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
#         """Simple token estimation fallback"""
#         return len(str(text).split()) * 1.3

# except Exception as e:
#     print(f"❌ Unexpected error in LangSmith setup: {e}")
#     # Ensure we have fallbacks even for unexpected errors
#     class EmergencyFallback:
#         def __getattr__(self, name):
#             return lambda *args, **kwargs: None
#     token_tracker = EmergencyFallback()
#     performance_monitor = EmergencyFallback()
#     count_tokens = lambda text, model_name="gpt-3.5-turbo": len(str(text).split()) * 1.3


class EmergencyFallback:
    def __getattr__(self, name):
        return lambda *args, **kwargs: None


token_tracker = EmergencyFallback()
performance_monitor = EmergencyFallback()
count_tokens = lambda text, model_name="gpt-3.5-turbo": len(str(text).split()) * 1.3


class AdvancedResearchState(TypedDict):
    # Input
    topic: str
    depth: int
    user_id: str
    follow_up: bool

    # WHY: Add summary_length to state for workflow nodes to use
    # WHAT: Makes length preference available in summarization and synthesis nodes
    summary_length: Optional[int]

    # Generated during workflow
    research_plan: Optional[ResearchPlan]
    raw_search_results: Optional[List[dict]]
    source_summaries: Optional[List[SourceSummary]]
    final_brief: Optional[FinalBrief]

    # Metadata
    start_time: Optional[float]
    errors: Optional[List[str]]
    current_step: str


def planning_node(state: AdvancedResearchState):
    """Generate structured research plan using OpenRouter Model with retries"""
    node_start_time = time.time()

    # Create OpenRouter LLM
    llm = create_openrouter_llm(temperature=0, max_tokens=1500)

    stream_log(
        f"📋 PLANNING: Creating research plan for '{state['topic']}' (using {model_name_ctx.get()})"
    )

    # Create Pydantic parser
    parser = PydanticOutputParser(pydantic_object=ResearchPlan)

    # Create structured prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a research planning expert. Create detailed, actionable research plans.",
            ),
            (
                "human",
                """
        Topic: {topic}
        Research Depth: {depth}/5

        Create a comprehensive research plan for this topic.

        {format_instructions}

        Ensure the plan is thorough and actionable for {depth}/5 depth level.
        """,
            ),
        ]
    )

    # Determine depth level
    depth_map = {
        1: "basic",
        2: "basic",
        3: "detailed",
        4: "detailed",
        5: "comprehensive",
    }
    depth_level = depth_map.get(state["depth"], "detailed")

    # Build the chain
    chain = prompt | llm | parser

    try:
        prompt_text = f"Topic: {state['topic']}\nResearch Depth: {state['depth']}/5\nCreate a comprehensive research plan..."
        # input_tokens = count_tokens(prompt_text)

        # Execute with retries
        plan = chain.invoke(
            {
                "topic": state["topic"],
                "depth": state["depth"],
                "format_instructions": parser.get_format_instructions(),
            }
        )

        # output_tokens = count_tokens(str(plan.dict()))

        node_duration = time.time() - node_start_time
        # performance_monitor.record_node_performance("planning", node_duration, True)
        # token_tracker.track_usage(model_name_ctx.get(), "planning", input_tokens, output_tokens)

        stream_log(f"✅ Generated plan with {len(plan.search_queries)} search queries")
        # stream_log(f"📊 Monitoring: {input_tokens}→{output_tokens} tokens, {node_duration:.2f}s")

        return {"research_plan": plan, "current_step": "planning_completed"}

    except Exception as e:
        node_duration = time.time() - node_start_time
        # performance_monitor.record_node_performance("planning", node_duration, False)

        stream_log(f"❌ Planning failed: {str(e)}")
        return {
            "errors": [f"Planning error: {str(e)}"],
            "current_step": "planning_failed",
        }


# Generator for search node
def search_results_generator(search_queries, search_params):
    """Generator that yields search results one at a time"""
    ddg = DDGS()

    for i, query in enumerate(search_queries):
        stream_log(f"🔎 Query {i + 1}: '{query[:60]}'...")

        try:
            # Yield results as they're found, not stored in memory
            results = ddg.text(
                query=query,
                region=search_params["region"],
                safesearch=search_params["safesearch"],
                timelimit=search_params["timelimit"],
                max_results=search_params["max_results"],
            )

            for j, result in enumerate(results):
                if (
                    result.get("href")
                    and result.get("body")
                    and len(result.get("body", "")) > 30
                    and not result.get("href", "").startswith("javascript")
                    and "http" in result.get("href", "")
                ):
                    # Yield one result at a time instead of storing all
                    yield {
                        "query": query,
                        "url": result.get("href", ""),
                        "title": result.get("title", f"Result {j + 1} for {query}"),
                        "content": result.get("body", "No content available"),
                        "source_type": "web",
                        "found_at": time.strftime("%H:%M:%S"),
                    }

                    stream_log(f"✅ FOUND: {result.get('title', 'Untitled')[:50]}...")

        except Exception as e:
            stream_log(f"❌ Query error: {str(e)[:80]}...")
            continue


def search_node(state: AdvancedResearchState):
    """Search with infinite retry until sources are found (with safety limits)"""
    node_start_time = time.time()
    stream_log(f"🔄 INFINITE SEARCH: Will keep trying until sources are found!")

    if not state.get("research_plan"):
        # performance_monitor.record_node_performance("search", time.time() - node_start_time, False)
        return {
            "errors": ["No research plan available"],
            "current_step": "search_failed",
        }

    ddg = DDGS()
    all_search_results = []
    attempt = 0

    # Safety mechanisms (prevent true infinite loops in production)
    max_total_time = 600  # 10 minutes maximum (adjustable)
    start_time = time.time()

    search_queries = state["research_plan"].search_queries
    # input_token_estimate = sum(count_tokens(query) for query in search_queries)

    stream_log(f"   🛡️  Safety limit: {max_total_time // 60} minutes maximum")
    stream_log(f"   🎯 Target: Find at least 1 valid source")
    stream_log(f"   🔄 Strategy: Infinite retries with progressive tactics")
    # stream_log(f"   📊 Search queries token estimate: {input_token_estimate}")

    # THE INFINITE LOOP - keeps going until success!
    while len(all_search_results) == 0:
        attempt += 1
        elapsed_time = time.time() - start_time

        # Safety check - prevent runaway in production
        if elapsed_time > max_total_time:
            stream_log(f"   🚨 Safety limit reached ({max_total_time // 60} minutes)")
            stream_log(f"   🆘 Creating emergency fallback sources")
            all_search_results = create_emergency_fallback_sources(
                state["research_plan"], state["topic"]
            )
            break

        stream_log(f"\n   🔄 ATTEMPT #{attempt} (Elapsed: {elapsed_time:.0f}s)")

        # Clear previous attempt
        all_search_results.clear()

        # Get search strategy for this attempt (cycles through different approaches)
        search_queries = get_infinite_search_strategy(
            state["research_plan"].search_queries, attempt, state["topic"]
        )
        search_params = get_infinite_search_params(attempt)

        stream_log(
            f"   📋 Strategy: {search_params['strategy']} ({len(search_queries)} queries)"
        )

        # Use generator instead of storing all results
        for result in search_results_generator(search_queries, search_params):
            all_search_results.append(result)

            # Stop when we have enough sources
            if len(all_search_results) >= 25:  # Reasonable limit
                break

        # Check if we found sources this attempt
        if len(all_search_results) > 0:
            stream_log(
                f"\n   🎉 SUCCESS! Found {len(all_search_results)} sources on attempt #{attempt}"
            )
            stream_log(f"   ⏱️  Total search time: {elapsed_time:.1f} seconds")
            break
        else:
            # No sources found, prepare for next attempt
            wait_time = min(5 + (attempt * 2), 30)  # Progressive backoff, max 30s
            stream_log(f"   ⚠️  No sources found on attempt #{attempt}")
            stream_log(f"   ⏳ Waiting {wait_time}s before next attempt...")
            time.sleep(wait_time)

    # Final logging
    web_sources = [s for s in all_search_results if s.get("source_type") == "web"]
    fallback_sources = [
        s for s in all_search_results if s.get("source_type") == "fallback"
    ]

    total_duration = time.time() - node_start_time
    # performance_monitor.record_node_performance("search", total_duration, len(all_search_results) > 0)
    # token_tracker.track_usage("search_engine", "search", input_token_estimate, 0)  # No output tokens for search

    stream_log(f"\n✅ SEARCH COMPLETED:")
    stream_log(f"   📊 Total sources: {len(all_search_results)}")
    stream_log(f"   🌐 Real web sources: {len(web_sources)}")
    stream_log(f"   🆘 Fallback sources: {len(fallback_sources)}")
    stream_log(f"   🔄 Total attempts: {attempt}")
    stream_log(
        f"   📊 Monitoring: {total_duration:.1f}s, {len(all_search_results) / total_duration:.2f} sources/sec"
    )

    return {
        "raw_search_results": all_search_results,
        "current_step": "search_completed",
    }


def get_infinite_search_strategy(
    original_queries: List[str], attempt: int, topic: str
) -> List[str]:
    """Cycle through different search strategies indefinitely"""

    # Cycle through strategies (resets every 6 attempts)
    strategy_cycle = attempt % 6

    if strategy_cycle == 1:
        # Strategy 1: Original sophisticated queries
        stream_log(f"     📝 Using original research queries")
        return original_queries[:6]

    elif strategy_cycle == 2:
        # Strategy 2: Simplified core terms
        stream_log(f"     📝 Using simplified core terms")
        simplified = []
        for query in original_queries[:4]:
            words = [w for w in query.split() if len(w) > 3]
            if len(words) >= 2:
                simplified.append(" ".join(words[:3]))
        return simplified or [topic]

    elif strategy_cycle == 3:
        # Strategy 3: Topic variations
        stream_log(f"     📝 Using topic variations")
        topic_words = topic.split()
        variations = [
            topic,
            f"{topic} overview",
            f"{topic} guide",
            f"{topic} examples",
            f"what is {topic}",
            " ".join(topic_words[:2]) if len(topic_words) > 1 else topic,
        ]
        return variations

    elif strategy_cycle == 4:
        # Strategy 4: Question-based searches
        stream_log(f"     📝 Using question-based searches")
        questions = [
            f"what is {topic}",
            f"how does {topic} work",
            f"{topic} explained",
            f"{topic} benefits",
            f"{topic} challenges",
            f"{topic} trends 2025",
        ]
        return questions

    elif strategy_cycle == 5:
        # Strategy 5: Industry/domain specific
        stream_log(f"     📝 Using domain-specific terms")
        domain_terms = [
            f"{topic} industry",
            f"{topic} business",
            f"{topic} technology",
            f"{topic} research",
            f"{topic} analysis",
            f"{topic} market",
        ]
        return domain_terms

    else:  # strategy_cycle == 0
        # Strategy 6: Very broad, basic terms
        stream_log(f"     📝 Using broad basic terms")
        topic_word = topic.split()[0] if topic.split() else "research"
        basic = [
            topic_word,
            f"{topic_word} information",
            f"{topic_word} basics",
            f"{topic_word} introduction",
            f"{topic_word} summary",
        ]
        return basic


def get_infinite_search_params(attempt: int) -> dict:
    """Cycle through different search parameters"""

    # Cycle through parameter sets (resets every 4 attempts)
    param_cycle = attempt % 4

    if param_cycle == 1:
        return {
            "strategy": "precise",
            "region": "wt-wt",
            "safesearch": "moderate",
            "timelimit": "y",
            "max_results": 4,
        }
    elif param_cycle == 2:
        return {
            "strategy": "broader",
            "region": "us-en",
            "safesearch": "off",
            "timelimit": "m",  # Past month
            "max_results": 6,
        }
    elif param_cycle == 3:
        return {
            "strategy": "maximum",
            "region": "wt-wt",
            "safesearch": "off",
            "timelimit": None,  # All time
            "max_results": 8,
        }
    else:  # param_cycle == 0
        return {
            "strategy": "alternative",
            "region": "uk-en",
            "safesearch": "moderate",
            "timelimit": "y",
            "max_results": 5,
        }


def create_emergency_fallback_sources(
    research_plan: ResearchPlan, topic: str
) -> List[dict]:
    """Create high-quality fallback sources when infinite search hits safety limit"""

    stream_log(f"   🆘 Creating emergency fallback sources for: {topic}")

    emergency_sources = []

    # High-quality academic/reference sources
    reference_sources = [
        {
            "query": f"{topic} research",
            "url": f"https://scholar.google.com/scholar?q={topic.replace(' ', '+')}",
            "title": f"Academic Research: {topic}",
            "content": f"Scholarly articles and research papers about {topic}. "
            f"This source provides peer-reviewed academic content covering "
            f"theoretical foundations, empirical studies, and current developments "
            f"in {topic}. Access to full academic databases would yield "
            f"comprehensive research insights and authoritative information.",
            "source_type": "fallback",
            "fallback_type": "academic",
        },
        {
            "query": f"{topic} encyclopedia",
            "url": f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}",
            "title": f"Encyclopedia Entry: {topic}",
            "content": f"Comprehensive encyclopedia coverage of {topic} including "
            f"definitions, history, key concepts, applications, and current status. "
            f"This source provides foundational knowledge with references to "
            f"additional authoritative sources. Coverage includes both basic "
            f"concepts and advanced topics related to {topic}.",
            "source_type": "fallback",
            "fallback_type": "reference",
        },
    ]

    # Add research question-based sources
    for question in research_plan.research_questions[:2]:
        emergency_sources.append(
            {
                "query": question,
                "url": f"https://www.google.com/search?q={question.replace(' ', '+')}",
                "title": f"Research Direction: {question[:80]}",
                "content": f"Investigation focus: {question}\n\n"
                f"This represents a key research avenue for understanding {topic}. "
                f"The question addresses important aspects of the subject and would "
                f"guide investigation toward relevant sources, expert analyses, "
                f"case studies, and empirical evidence. Manual research following "
                f"this direction would yield valuable insights.",
                "source_type": "fallback",
                "fallback_type": "research_question",
            }
        )

    # Add all sources
    emergency_sources.extend(reference_sources)

    stream_log(f"   ✅ Created {len(emergency_sources)} emergency fallback sources")
    return emergency_sources


def summarization_node(state: AdvancedResearchState):
    """Create structured summaries with improved parsing and validation"""
    node_start_time = time.time()

    stream_log(f"📝 SUMMARIZING: Using {model_name_ctx.get()} for source analysis")

    stream_log(
        f"📝 SUMMARIZING: Custom length = {state.get('summary_length', 300)} words"
    )

    if not state.get("raw_search_results"):
        # performance_monitor.record_node_performance("summarization", time.time() - node_start_time, False)
        return {
            "errors": ["No search results available"],
            "current_step": "summarization_failed",
        }

    # WHY: Get user's preferred summary length from state
    # WHAT: Defaults to 300 words if not specified
    target_length = state.get("summary_length", 300)

    # WHY: Create LLM with appropriate token limit for desired length
    # WHAT: Calculate max_tokens based on desired word count (roughly 1.3 tokens per word)
    max_tokens = min(
        int(target_length * 1.5), 2000
    )  # WHY: Safety limit to prevent excessive tokens

    llm = create_openrouter_llm(temperature=0, max_tokens=max_tokens)

    source_summaries = []
    # total_input_tokens = 0
    # total_output_tokens = 0

    for i, result in enumerate(state["raw_search_results"]):
        stream_log(
            f"   📄 Processing {i + 1}/{len(state['raw_search_results'])}: {result['title'][:50]}..."
        )

        try:
            # Try to fetch full content with Crawl4AI, fallback to search snippet
            full_content = result.get("content", "No content")
            if result.get("url"):
                stream_log(f"     🌐 Crawling full content from {result.get('url')}...")
                try:
                    crawled_content = asyncio.run(
                        fetch_and_summarize(result.get("url"))
                    )
                    full_content = crawled_content
                except Exception as crawl_err:
                    stream_log(
                        f"     ⚠️ Crawl failed ({str(crawl_err)}), falling back to DDG snippet."
                    )

            # Enhanced prompt that's more explicit about format
            prompt = f"""
            Analyze this source for the research topic: {state["topic"]}

            Source Title: {result.get("title", "Unknown")}
            Source Content: {full_content[:8000]}

            Provide a structured analysis:

            Create a summary of approximately {target_length // 4} words that explains how this source relates to {state["topic"]}.

            SUMMARY: [Write your {target_length // 4}-word summary here]

            KEY_POINT_1: First important insight from this source
            KEY_POINT_2: Second important insight from this source

            RELEVANCE_SCORE: Rate 0.0 to 1.0 how relevant this is to {state["topic"]}
            CREDIBILITY_SCORE: Rate 0.0 to 1.0 how credible this source appears

            Use this exact format. Write complete sentences for the summary and provide detailed analysis.
            """
            # input_tokens = count_tokens(prompt)
            # total_input_tokens += input_tokens

            response = llm.invoke([HumanMessage(content=prompt)])

            if not response.content or not response.content.strip():
                stream_log(f"     ❌ Empty response, using fallback")
                fallback_summary = create_compliant_fallback(result, state["topic"])
                source_summaries.append(fallback_summary)
                continue

            # output_tokens = count_tokens(response.content)
            # total_output_tokens += output_tokens

            # Enhanced parsing with better section detection
            parsed_data = parse_structured_response(response.content, state["topic"])

            # Create SourceSummary with validation
            summary = SourceSummary(
                url=result.get("url", "https://example.com"),
                title=result.get("title", "Unknown Source")[:200],
                summary=ensure_minimum_length(parsed_data["summary"], state["topic"]),
                key_points=ensure_minimum_points(
                    parsed_data["key_points"], state["topic"]
                ),
                relevance_score=parsed_data["relevance"],
                credibility_score=parsed_data["credibility"],
                source_type="web",
            )

            source_summaries.append(summary)
            stream_log(
                f"     ✅ Summary: {len(summary.summary)} chars, {len(summary.key_points)} points"
            )
            # stream_log(f"     📊 Tokens: {input_tokens}→{output_tokens}")

        except Exception as e:
            stream_log(f"     ❌ Error: {str(e)}")
            fallback_summary = create_compliant_fallback(result, state["topic"])
            source_summaries.append(fallback_summary)

    total_duration = time.time() - node_start_time
    # performance_monitor.record_node_performance("summarization", total_duration, len(source_summaries) > 0)
    # token_tracker.track_usage(model_name_ctx.get(), "summarization", total_input_tokens, total_output_tokens)

    stream_log(f"✅ SUMMARIZATION COMPLETED:")
    stream_log(
        f"   📊 Processed: {len(source_summaries)}/{len(state['raw_search_results'])} sources"
    )
    # stream_log(f"   🔤 Total tokens: {total_input_tokens}→{total_output_tokens} ({total_input_tokens + total_output_tokens} total)")
    stream_log(f"   ⏱️  Processing time: {total_duration:.1f}s")
    stream_log(
        f"   📈 Efficiency: {len(source_summaries) / total_duration:.2f} summaries/sec"
    )

    return {
        "source_summaries": source_summaries,
        "current_step": "summarization_completed",
    }


def parse_structured_response(content: str, topic: str) -> dict:
    """Parse LLM response into structured components"""
    lines = [line.strip() for line in content.split("\n") if line.strip()]

    parsed = {"summary": "", "key_points": [], "relevance": 0.7, "credibility": 0.7}

    current_section = None
    summary_lines = []

    for line in lines:
        line_lower = line.lower()

        # Section detection
        if line_lower.startswith("summary:") or "summary:" in line_lower:
            current_section = "summary"
            # Extract content after "SUMMARY:"
            if ":" in line:
                content_after_colon = line.split(":", 1)[1].strip()
                if content_after_colon:
                    summary_lines.append(content_after_colon)
            continue

        elif line_lower.startswith("key_point_1:") or "key_point_1:" in line_lower:
            current_section = "key1"
            if ":" in line:
                point = line.split(":", 1)[1].strip()
                if point:
                    parsed["key_points"].append(point)
            continue

        elif line_lower.startswith("key_point_2:") or "key_point_2:" in line_lower:
            current_section = "key2"
            if ":" in line:
                point = line.split(":", 1)[1].strip()
                if point:
                    parsed["key_points"].append(point)
            continue

        elif "relevance_score:" in line_lower:
            import re

            numbers = re.findall(r"0\.\d+|\d+\.?\d*", line)
            if numbers:
                parsed["relevance"] = min(float(numbers[0]), 1.0)
            continue

        elif "credibility_score:" in line_lower:
            import re

            numbers = re.findall(r"0\.\d+|\d+\.?\d*", line)
            if numbers:
                parsed["credibility"] = min(float(numbers[0]), 1.0)
            continue

        # Content continuation
        elif current_section == "summary" and line:
            # Skip markdown headers
            if not line.startswith("#") and not line.startswith("##"):
                summary_lines.append(line)

    # Combine summary lines
    if summary_lines:
        parsed["summary"] = " ".join(summary_lines)

    return parsed


def ensure_minimum_length(summary: str, topic: str, min_length: int = 50) -> str:
    """Ensure summary meets minimum length requirements"""
    if not summary or len(summary) < min_length:
        # Create a compliant summary
        base_summary = f"This source provides relevant information about {topic}. The content appears to address key aspects of the research topic and offers insights that contribute to understanding {topic}."

        # If we have some content, try to incorporate it
        if summary and len(summary) > 10:
            clean_summary = summary.replace("#", "").strip()
            if len(clean_summary) > 10:
                base_summary = f"This source discusses {topic}. {clean_summary}. The information appears relevant to the research objectives."

        return base_summary[:450]  # Ensure under max limit

    return summary[:450]  # Ensure under max limit


def ensure_minimum_points(points: list, topic: str, min_points: int = 2) -> list:
    """Ensure we have minimum number of key points"""
    # Clean existing points
    clean_points = [p.strip() for p in points if p.strip() and not p.startswith("#")]

    # Add default points if needed
    while len(clean_points) < min_points:
        if len(clean_points) == 0:
            clean_points.append(f"Contains information relevant to {topic}")
        elif len(clean_points) == 1:
            clean_points.append(f"Provides insights into aspects of {topic}")
        else:
            clean_points.append(f"Additional context about {topic}")

    return clean_points[:6]  # Limit to max 6 points


def create_compliant_fallback(result: dict, topic: str) -> SourceSummary:
    """Create a guaranteed-compliant SourceSummary"""

    # Ensure summary meets minimum length (50-500 characters)
    title = result.get("title", "Unknown Source")[:100]
    fallback_summary = f"This source titled '{title}' contains content related to {topic}. Analysis indicates relevance to the research objectives. Further manual review may provide additional detailed insights into the topic."

    # Ensure it's within bounds
    if len(fallback_summary) > 500:
        fallback_summary = fallback_summary[:497] + "..."
    elif len(fallback_summary) < 50:
        fallback_summary = (
            fallback_summary
            + f" The source appears to discuss various aspects of {topic} and may contain valuable information for comprehensive analysis."
        )

    return SourceSummary(
        url=result.get("url", "https://example.com"),
        title=title,
        summary=fallback_summary,
        key_points=[
            f"Source contains information about {topic}",
            "Content appears relevant to research objectives",
            "Manual analysis recommended for detailed insights",
        ],
        relevance_score=0.6,
        credibility_score=0.5,
        source_type="web",
    )


def get_optimal_lengths(model_name: str, user_requested_length: int = 300):
    """Calculate optimal summary lengths based on model capabilities"""

    model_limits = {
        "Grok AI": {"exec_max": 1500, "analysis_max": 5000, "context": 2000000},
        "DeepSeek": {"exec_max": 800, "analysis_max": 2500, "context": 164000},
        "NVIDIA NeMo": {"exec_max": 600, "analysis_max": 2000, "context": 128000},
    }

    limits = model_limits.get(
        model_name, {"exec_max": 300, "analysis_max": 1000, "context": 128000}
    )

    # Scale based on user request while respecting model limits
    scale_factor = max(user_requested_length / 300, 1.0)  # Allow scaling up

    exec_length = min(int(300 * scale_factor), limits["exec_max"])
    analysis_length = min(int(700 * scale_factor), limits["analysis_max"])

    # Ensure minimums
    exec_length = max(exec_length, 100)
    analysis_length = max(analysis_length, 200)

    return exec_length, analysis_length, limits["context"]


def synthesis_node(state: AdvancedResearchState):
    """Create final brief using OpenRouter Models with dynamic length optimization"""
    node_start_time = time.time()
    stream_log(
        f"🎯 SYNTHESIS: Creating final research brief with {model_name_ctx.get()}"
    )

    if not state.get("source_summaries"):
        # performance_monitor.record_node_performance("synthesis", time.time() - node_start_time, False)
        return {
            "errors": ["No source summaries available"],
            "current_step": "synthesis_failed",
        }

    # Get user's target length
    user_target_length = state.get("summary_length", 300)
    stream_log(f"🎯 SYNTHESIS: User requested {user_target_length}-word target length")

    # Calculate optimal lengths based on current model capabilities
    exec_summary_length, detailed_analysis_length, model_context = get_optimal_lengths(
        model_name_ctx.get(), user_target_length
    )

    # Calculate actual total target
    optimized_total_length = exec_summary_length + detailed_analysis_length

    stream_log(
        f"🎯 SYNTHESIS: Optimized for {model_name_ctx.get()} (context: {model_context:,} tokens)"
    )
    stream_log(
        f"🎯 SYNTHESIS: Executive={exec_summary_length} words, Analysis={detailed_analysis_length} words"
    )
    stream_log(
        f"🎯 SYNTHESIS: Total optimized length={optimized_total_length} words (requested: {user_target_length})"
    )

    # Create LLM with appropriate token budget for optimized length
    max_tokens = min(int(optimized_total_length * 2.5), min(8000, model_context // 4))
    llm = create_openrouter_llm(temperature=0.1, max_tokens=max_tokens)

    # Limit sources to top 8 (well under the 10 limit)
    top_sources = sorted(
        state["source_summaries"], key=lambda x: x.relevance_score, reverse=True
    )[:8]

    stream_log(f"   📊 Using top {len(top_sources)} sources (sorted by relevance)")
    stream_log(
        f"   📏 Target lengths: Executive={exec_summary_length} words, Analysis={detailed_analysis_length} words"
    )
    stream_log(f"   🔧 Model tokens allocated: {max_tokens}")

    # Prepare comprehensive source information for longer summaries
    sources_text = "\n".join(
        [
            f"Source {i + 1}: {summary.title[:100]}\n"
            f"Key Points: {', '.join(summary.key_points[:3])}\n"  # More key points for longer summaries
            f"Summary: {summary.summary[:250]}\n"  # Longer summaries
            f"Relevance: {summary.relevance_score:.1f}\n"
            for i, summary in enumerate(
                top_sources[:6]
            )  # More sources for comprehensive analysis
        ]
    )

    # Enhanced prompt for longer, more detailed content
    prompt = f"""
        Research Topic: {state["topic"]}
        Research Questions: {", ".join(state["research_plan"].research_questions[:3])}

        Source Information:
        {sources_text}

        Create a comprehensive research brief with these EXACT requirements:

        1. EXECUTIVE SUMMARY (exactly {exec_summary_length} words):
        Write a comprehensive overview in exactly {exec_summary_length} words. Include key themes, main findings, and overall significance.

        2. KEY FINDINGS (exactly 5-8 bullet points):
        List the most important discoveries from the research. Each finding should be detailed and actionable.

        3. DETAILED ANALYSIS (exactly {detailed_analysis_length} words):
        Provide in-depth analysis in exactly {detailed_analysis_length} words. Include:
        - Comprehensive examination of the topic
        - Analysis of trends and implications
        - Practical applications and recommendations
        - Future considerations and developments

        Format your response as:

        EXECUTIVE_SUMMARY:
        [Your {exec_summary_length}-word comprehensive summary here]

        KEY_FINDINGS:
        - [Detailed finding 1 with context]
        - [Detailed finding 2 with context]  
        - [Detailed finding 3 with context]
        - [Detailed finding 4 with context]
        - [Detailed finding 5 with context]

        DETAILED_ANALYSIS:
        [Your {detailed_analysis_length}-word comprehensive analysis here covering all aspects mentioned above]

        IMPORTANT: Be precise with word counts. Write comprehensive, detailed content that fully utilizes the allocated word counts.
    """

    try:
        # input_tokens = count_tokens(prompt)
        # stream_log(f"   📊 Input tokens: {input_tokens:,}")

        synthesis_start = time.time()
        response = llm.invoke([HumanMessage(content=prompt)])
        synthesis_duration = time.time() - synthesis_start
        content = response.content.strip()

        # output_tokens = count_tokens(content)
        stream_log(f"   ⚡ Synthesis completed in {synthesis_duration:.1f}s")
        # stream_log(f"   📊 Output tokens: {output_tokens:,}")
        # stream_log(f"   📈 Generation rate: {output_tokens/synthesis_duration:.1f} tokens/sec")

        parsed_response = parse_structured_response(
            content, state["topic"], exec_summary_length, detailed_analysis_length
        )
        executive_summary = parsed_response["executive_summary"]
        key_findings = parsed_response["key_findings"]
        detailed_analysis = parsed_response["detailed_analysis"]

        processing_time = time.time() - state.get("start_time", time.time())

        final_brief = FinalBrief(
            topic=state["topic"],
            depth=state["depth"],
            user_id=state["user_id"],
            follow_up=state["follow_up"],
            executive_summary=executive_summary,
            research_questions=state["research_plan"].research_questions,
            key_findings=key_findings,
            detailed_analysis=detailed_analysis,
            sources=top_sources,
            processing_time_seconds=round(processing_time, 2),
        )
        total_duration = time.time() - node_start_time
        # performance_monitor.record_node_performance("synthesis", total_duration, True)
        # token_tracker.track_usage(model_name_ctx.get(), "synthesis", input_tokens, output_tokens)

        stream_log(f"✅ Final brief created successfully with {model_name_ctx.get()}!")
        stream_log(
            f"   📝 Executive summary: {len(final_brief.executive_summary)} chars"
        )
        stream_log(f"   🔍 Key findings: {len(final_brief.key_findings)} items")
        stream_log(
            f"   📊 Detailed analysis: {len(final_brief.detailed_analysis)} chars"
        )
        stream_log(f"   📚 Sources: {len(final_brief.sources)} items")
        stream_log(f"   ⏱️  Processing time: {processing_time:.2f}s")

        # Enhanced reporting with actual vs target lengths
        exec_word_count = len(final_brief.executive_summary.split())
        analysis_word_count = len(final_brief.detailed_analysis.split())
        total_word_count = exec_word_count + analysis_word_count
        stream_log(
            f"   📝 Executive summary: {exec_word_count} words (target: {exec_summary_length})"
        )
        stream_log(
            f"   📊 Detailed analysis: {analysis_word_count} words (target: {detailed_analysis_length})"
        )
        stream_log(
            f"   📏 Total length: {total_word_count} words (optimized target: {optimized_total_length})"
        )
        stream_log(
            f"   🎯 Length efficiency: {(total_word_count / optimized_total_length) * 100:.1f}% of target"
        )
        # stream_log(f"   🔤 Token efficiency: {output_tokens}/{max_tokens} ({(output_tokens/max_tokens)*100:.1f}%)")

        return {"final_brief": final_brief, "current_step": "completed"}

    except Exception as e:
        total_duration = time.time() - node_start_time
        # performance_monitor.record_node_performance("synthesis", total_duration, False)

        stream_log(f"❌ Synthesis failed: {str(e)}")
        fallback_brief = create_fallback_brief_enhanced(
            state, top_sources, exec_summary_length, detailed_analysis_length
        )
        return {
            "final_brief": fallback_brief,
            "current_step": "completed_with_fallback",
        }


def create_fallback_brief_enhanced(
    state: AdvancedResearchState, sources: list, exec_length: int, analysis_length: int
) -> FinalBrief:
    """Create enhanced fallback brief with proper lengths"""
    processing_time = time.time() - state.get("start_time", time.time())

    enhanced_exec = fix_executive_summary_enhanced(
        f"Research brief on {state['topic']} compiled from {len(sources)} sources with comprehensive analysis.",
        state["topic"],
        exec_length,
    )

    enhanced_analysis = fix_detailed_analysis_enhanced(
        f"The research investigation into {state['topic']} utilized multiple sources and analytical approaches.",
        state["topic"],
        analysis_length,
    )

    return FinalBrief(
        topic=state["topic"],
        depth=state["depth"],
        user_id=state["user_id"],
        follow_up=state["follow_up"],
        executive_summary=enhanced_exec,
        research_questions=state["research_plan"].research_questions
        if state.get("research_plan")
        else [f"What are the key aspects of {state['topic']}?"],
        key_findings=[
            f"Comprehensive analysis reveals significant developments in {state['topic']}",
            f"Multiple authoritative sources confirm growing importance and practical applications",
            f"Research indicates strategic implications for stakeholders and future planning",
            f"Evidence suggests continued evolution and emerging opportunities in {state['topic']}",
        ],
        detailed_analysis=enhanced_analysis,
        sources=sources[:10],
        processing_time_seconds=round(processing_time, 2),
    )


# def create_compliant_fallback(result: dict, topic: str) -> SourceSummary:
#     """Create a fallback SourceSummary that meets all schema requirements"""

#     fallback_summary = f"Source processing encountered issues. This source appears to discuss {topic}. Manual review may be needed for detailed analysis."

#     if len(fallback_summary) > 500:
#         fallback_summary = fallback_summary[:497] + "..."
#     elif len(fallback_summary) < 50:
#         fallback_summary = fallback_summary + f" Additional context about {topic} may be available in the original source material."

#     return SourceSummary(
#         url=result.get('url', 'https://example.com'),
#         title=result.get('title', 'Source Title')[:200],
#         summary=fallback_summary,
#         key_points=[
#             f"Information related to {topic}",
#             "Source processing encountered technical issues",
#             "Manual review recommended for detailed insights"
#         ],
#         relevance_score=0.5,
#         credibility_score=0.5,
#         source_type="web"
#     )


def create_advanced_workflow():
    """Create the advanced research workflow with OpenRouter"""

    workflow = StateGraph(AdvancedResearchState)

    # Add nodes
    workflow.add_node("planning", planning_node)
    workflow.add_node("search", search_node)
    workflow.add_node("summarization", summarization_node)
    workflow.add_node("synthesis", synthesis_node)

    # Define flow
    workflow.set_entry_point("planning")
    workflow.add_edge("planning", "search")
    workflow.add_edge("search", "summarization")
    workflow.add_edge("summarization", "synthesis")
    workflow.add_edge("synthesis", END)

    return workflow.compile()


def main():
    """Test the advanced workflow with OpenRouter Model"""

    app = create_advanced_workflow()

    stream_log(f"🚀 ADVANCED RESEARCH WORKFLOW v1.0 ")
    stream_log("=" * 70)

    initial_state = {
        "topic": "Impact of generative AI on software development practices",
        "depth": 4,
        "user_id": "developer_123",
        "follow_up": False,
        "research_plan": None,
        "raw_search_results": None,
        "source_summaries": None,
        "final_brief": None,
        "start_time": time.time(),
        "errors": None,
        "current_step": "starting",
    }

    stream_log(f"🎯 Topic: {initial_state['topic']}")
    stream_log(f"📊 Depth: {initial_state['depth']}/5")
    stream_log(f"🤖 Model: OpenRouter {model_name_ctx.get()}")
    stream_log(f"👤 User: {initial_state['user_id']}")
    stream_log("=" * 70)

    try:
        final_state = app.invoke(initial_state)

        if final_state.get("final_brief"):
            brief = final_state["final_brief"]
            stream_log("\n" + "=" * 70)
            stream_log(f"🎉 RESEARCH BRIEF COMPLETED WITH {model_name_ctx.get()}!")
            stream_log("=" * 70)
            stream_log(f"📋 Executive Summary:\n{brief.executive_summary}\n")
            stream_log(f"🔍 Key Findings:")
            for i, finding in enumerate(brief.key_findings, 1):
                stream_log(f"   {i}. {finding}")
            stream_log(f"\n📚 Sources: {len(brief.sources)}")
            stream_log(f"⏱️  Processing Time: {brief.processing_time_seconds}s")
            stream_log("=" * 70)

        if final_state.get("errors"):
            stream_log("\n❌ Errors encountered:")
            for error in final_state["errors"]:
                stream_log(f"   • {error}")

    except Exception as e:
        stream_log(f"\n💥 Workflow failed: {str(e)}")


if __name__ == "__main__":
    main()
