# 📖 User Guide - AI Research Brief Generator

## Welcome

Welcome to the AI Research Brief Generator! This comprehensive guide will help you get the most out of your AI-powered research assistant, whether you're a student, researcher, professional, or content creator.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Using the Web Interface](#using-the-web-interface)
3. [Command Line Interface](#command-line-interface)
4. [API Integration](#api-integration)
5. [Advanced Features](#advanced-features)
6. [Tips & Best Practices](#tips--best-practices)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#frequently-asked-questions)

## Getting Started

### What is the AI Research Brief Generator?

The AI Research Brief Generator is an intelligent research assistant that:
- **Automatically researches** any topic using real web search
- **Generates structured briefs** with executive summaries, key findings, and detailed analysis
- **Provides verified sources** with relevance and credibility scoring
- **Customizes output length** from 50 to 2000 words based on your needs
- **Supports follow-up research** building on previous context

### Who Should Use This Tool?

**🎓 Students**: Research assignments, essay preparation, topic exploration
**📊 Researchers**: Literature reviews, market analysis, competitive intelligence
**💼 Professionals**: Business intelligence, industry reports, decision support
**✍️ Content Creators**: Article research, fact-checking, source gathering
**🏢 Organizations**: Knowledge management, training materials, briefing documents

### Access Methods

You have three ways to use the research assistant:

1. **🌐 Web Interface** (Easiest): https://ai-research-assistant-production-1ef8.up.railway.app/docs
2. **⌨️ Command Line** (Most Powerful): Download and run locally
3. **🔗 API Integration** (Most Flexible): Integrate into your applications

## Using the Web Interface

### Accessing the Interactive Documentation

1. **Open your browser** and go to: https://ai-research-assistant-production-1ef8.up.railway.app/docs
2. **Find the POST /brief endpoint** in the interface
3. **Click "Try it out"** to enable the request form

### Making Your First Request

#### Step 1: Fill in the Request Form
```json
{
    "topic": "renewable energy storage solutions",
    "depth": 3,
    "user_id": "your_name_here",
    "summary_length": 400,
    "follow_up": false
}
```

#### Step 2: Understanding the Parameters

**Topic** (Required)
- **What**: The research subject you want to investigate
- **Format**: 5-200 characters
- **Examples**: 
  - "artificial intelligence in healthcare"
  - "sustainable transportation technologies"
  - "blockchain applications in supply chain"

**Depth** (Optional, default: 3)
- **What**: How thorough the research should be
- **Options**:
  - **1 (Quick)**: Basic overview, 2-3 sources, ~15-30 seconds
  - **2 (Light)**: Standard research, 3-4 sources, ~25-40 seconds
  - **3 (Medium)**: Balanced analysis, 4-6 sources, ~35-50 seconds
  - **4 (Detailed)**: Comprehensive research, 6-8 sources, ~45-70 seconds
  - **5 (Exhaustive)**: Maximum depth, 8-10 sources, ~60-90 seconds

**User ID** (Required)
- **What**: A unique identifier for tracking your research
- **Format**: Any text, minimum 1 character
- **Purpose**: Enables follow-up research and user-specific context
- **Examples**: "john_student", "researcher_2025", "marketing_team"

**Summary Length** (Optional, default: 300)
- **What**: Target word count for the generated summary sections
- **Range**: 50-2000 words
- **Usage**:
  - **50-150**: Quick overviews, social media posts
  - **200-400**: Standard reports, presentations
  - **500-800**: Detailed analysis, academic papers
  - **1000-2000**: Comprehensive reports, white papers

**Follow Up** (Optional, default: false)
- **What**: Whether this research builds on previous research
- **When to use**: Set to `true` when researching related topics with the same user_id
- **Benefits**: AI maintains context and provides deeper, more connected insights

#### Step 3: Execute the Request

1. **Click "Execute"** to send your request
2. **Wait for processing** (30-90 seconds depending on depth)
3. **Review the response** in the interface

### Understanding the Response

#### Success Response Structure
```json
{
    "success": true,
    "brief_id": "550e8400-e29b-41d4-a716-446655440000",
    "brief": {
        "topic": "renewable energy storage solutions",
        "executive_summary": "Renewable energy storage is rapidly evolving...",
        "key_findings": [
            "Battery costs have decreased 90% since 2010",
            "Grid-scale storage is becoming economically viable",
            "Policy support is accelerating deployment"
        ],
        "detailed_analysis": "The renewable energy storage sector...",
        "sources": [
            {
            "title": "Global Energy Storage Report 2025",
            "url": "https://example.com/report",
            "summary": "Comprehensive analysis of storage trends...",
            "relevance_score": 0.9,
            "credibility_score": 0.8
            }
        ]
    },
    "processing_time": 45.7
}
```

#### Response Components Explained

**Brief ID**: Unique identifier for this research brief (useful for reference)

**Executive Summary**: High-level overview of the research findings (typically 20-30% of total length)

**Key Findings**: 3-8 bullet points highlighting the most important discoveries

**Detailed Analysis**: Comprehensive analysis with insights and implications (typically 70-80% of total length)

**Sources**: Array of verified sources with:
- **Title**: Human-readable source name
- **URL**: Direct link to the source
- **Summary**: AI-generated summary of source content
- **Key Points**: Important insights from this specific source
- **Relevance Score**: 0.0-1.0 rating of relevance to your topic
- **Credibility Score**: 0.0-1.0 rating of source trustworthiness

## Command Line Interface

### Installation

1. **Download the project files** to your computer
2. **Install Python 3.11+** if not already installed
3. **Install dependencies**:
    ```python 
    pip install -r requirements.txt
    ```
4. **Get OpenRouter API key** from https://openrouter.ai (free)
5. **Set up environment**:
    ```echo "OPENROUTER_API_KEY=your_key_here" > .env```


### Basic Usage

#### Quick Research Brief
```python cli.py --topic "AI in education" --depth 3 --user student_123```

#### Custom Length Research
```python cli.py --topic "climate change mitigation" --depth 4 --user researcher --length 600```


#### Follow-up Research
```python
# First research
python cli.py --topic "renewable energy trends" --depth 3 --user energy_analyst

# Follow-up research (builds on previous)
python cli.py --topic "solar energy challenges" --depth 3 --user energy_analyst --follow-up
```

#### Interactive Mode
```python cli.py --interactive```

This will prompt you step-by-step for all parameters:
```bash
📝 Enter research topic: artificial intelligence in healthcare
📊 Enter research depth (1-5, default 3): 4
👤 Enter your user ID: medical_student
📏 Enter desired summary length in words (50-2000, default 300): 500
🔄 Is this a follow-up query? (y/N): n
```

#### Using with Deployed API
```bash
# Point CLI to live API instead of local server
export API_BASE_URL=https://ai-research-assistant-production-1ef8.up.railway.app
python cli.py --topic "quantum computing" --depth 3 --user tech_researcher
```

### CLI Options Reference

| Option | Short | Description | Required | Default |
|--------|-------|-------------|----------|---------|
| `--topic` | `-t` | Research topic (5-200 chars) | Yes* | - |
| `--depth` | `-d` | Research depth (1-5) | No | 3 |
| `--user` | `-u` | User identifier | Yes* | - |
| `--length` | `-l` | Summary length (50-2000 words) | No | 300 |
| `--follow-up` | `-f` | Enable follow-up mode | No | false |
| `--interactive` | `-i` | Interactive mode | No | false |
| `--json` | `-j` | Output in JSON format | No | false |

*Required unless using `--interactive` mode

## API Integration

### Direct HTTP Requests

#### Using cURL (Linux/Mac)
```curl 
curl -X POST https://ai-research-assistant-production-1ef8.up.railway.app/brief
-H "Content-Type: application/json"
-d '{
    "topic": "sustainable agriculture technologies",
    "depth": 3,
    "user_id": "farmer_researcher",
    "summary_length": 500
    }'
```

#### Using PowerShell (Windows)
``` 
$headers = @{"Content-Type" = "application/json"}
$body = @{
topic = "digital transformation in retail"
depth = 4
user_id = "retail_analyst"
summary_length = 700
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://ai-research-assistant-production-1ef8.up.railway.app/brief" `
-Method POST -Headers $headers -Body $body

```

### Programming Language Integration

#### Python Integration
```python 
import requests
import json

def generate_research_brief(topic, depth=3, user_id="default", summary_length=300, follow_up=False):
    url = "https://ai-research-assistant-production-1ef8.up.railway.app/brief"
    payload = {
    "topic": topic,
    "depth": depth,
    "user_id": user_id,
    "summary_length": summary_length,
    "follow_up": follow_up
    }
    try:
        response = requests.post(url, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data['brief']
            else:
                print(f"Error: {data.get('error')}")
                return None
        else:
            print(f"HTTP Error: {response.status_code}")
            return None
            
    except requests.Timeout:
        print("Request timed out")
        return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# Usage example
brief = generate_research_brief(
topic="machine learning in finance",
depth=4,
user_id="fintech_developer",
summary_length=600
)

if brief:
    print(f"Topic: {brief['topic']}")
    print(f"Summary: {brief['executive_summary']}")
    print(f"Key Findings: {len(brief['key_findings'])} points")
    print(f"Sources: {len(brief['sources'])} references")
```

#### JavaScript/Node.js Integration
```javascript
const axios = require('axios');

async function generateResearchBrief(topic, depth = 3, userId = 'default', summaryLength = 300, followUp = false) {
    const url = 'https://ai-research-assistant-production-1ef8.up.railway.app/brief';
    const payload = {
        topic: topic,
        depth: depth,
        user_id: userId,
        summary_length: summaryLength,
        follow_up: followUp
    };

    try {
        const response = await axios.post(url, payload, { timeout: 120000 });
        
        if (response.data.success) {
            return response.data.brief;
        } else {
            console.error('Error:', response.data.error);
            return null;
        }
    } catch (error) {
        if (error.code === 'ECONNABORTED') {
            console.error('Request timed out');
        } else {
            console.error('Request failed:', error.message);
        }
        return null;
    }
}

// Usage example
(async () => {
    const brief = await generateResearchBrief(
        'blockchain in supply chain management',
        4,
        'supply_chain_analyst',
        800
    );

    if (brief) {
        console.log(`Topic: ${brief.topic}`);
        console.log(`Summary: ${brief.executive_summary}`);
        console.log(`Key Findings: ${brief.key_findings.length} points`);
        console.log(`Sources: ${brief.sources.length} references`);
    }
})();
```

## Advanced Features

### Variable Summary Length

The AI automatically adjusts the distribution of content based on your requested length:

**Length Distribution Strategy:**
- **Executive Summary**: ~30% of total length
- **Detailed Analysis**: ~70% of total length
- **Key Findings**: Fixed at 3-8 points regardless of length

**Recommended Lengths by Use Case:**
- Blog Post Summary: 150-250 words
- Presentation Brief: 300-500 words
- Research Paper Prep: 600-1000 words
- Comprehensive Report: 1200-2000 words

**Example: Length Comparison**

```bash
# Short summary (200 words)
python cli.py --topic "AI ethics" --depth 3 --user researcher --length 200
# Result: Concise overview with essential points only

# Medium summary (500 words)
python cli.py --topic "AI ethics" --depth 3 --user researcher --length 500
# Result: Balanced coverage with moderate detail

# Long summary (1000 words)
python cli.py --topic "AI ethics" --depth 3 --user researcher --length 1000
# Result: Comprehensive analysis with extensive detail
```

### Context-Aware Follow-up Research

Follow-up research builds on previous research context for the same user:

**How It Works:**
1. **Initial Research**: Research a broad topic
2. **Follow-up Research**: Use same `user_id` with `follow_up: true`
3. **AI Context**: System remembers previous research and builds upon it
4. **Enhanced Insights**: More focused, deeper analysis with connections to previous research

**Example Workflow:**
```bash
# Step 1: Broad research
python cli.py --topic "renewable energy technologies" --depth 3 --user energy_student

# Step 2: Focused follow-up
python cli.py --topic "solar panel efficiency improvements" --depth 4 --user energy_student --follow-up

# Step 3: Specific implementation follow-up
python cli.py --topic "solar panel installation challenges" --depth 3 --user energy_student --follow-up
```

**Benefits of Follow-up Research:**
- **Less Redundant Information**: Skips basics covered in previous research
- **Deeper Analysis**: Focuses on advanced concepts and specific details
- **Better Connections**: Links current research to previous findings
- **Specialized Terminology**: Uses domain-specific language appropriate for continued research

### Multi-Depth Research Strategy

Choose the right depth level for your needs:

**Depth 1 (Quick Overview) - 15-30 seconds**
- **Best for**: Initial topic exploration, social media content
- **Content**: Basic definitions, key statistics, primary sources
- **Sources**: 2-3 high-quality sources
- **Use cases**: Quick fact-checking, conversation starters

**Depth 2 (Light Research) - 25-40 seconds**
- **Best for**: Blog posts, presentations, student assignments
- **Content**: Core concepts, main trends, essential facts
- **Sources**: 3-4 diverse sources
- **Use cases**: Content creation, homework help

**Depth 3 (Medium Research) - 35-50 seconds** 
- **Best for**: Business reports, academic papers, decision-making
- **Content**: Comprehensive overview, multiple perspectives, analysis
- **Sources**: 4-6 authoritative sources
- **Use cases**: Professional research, strategic planning

**Depth 4 (Detailed Research) - 45-70 seconds**
- **Best for**: Literature reviews, competitive analysis, expert-level content
- **Content**: In-depth analysis, edge cases, implementation details
- **Sources**: 6-8 specialized sources
- **Use cases**: Graduate research, consulting reports

**Depth 5 (Exhaustive Research) - 60-90 seconds**
- **Best for**: Comprehensive reports, white papers, policy analysis
- **Content**: Complete coverage, nuanced analysis, expert insights
- **Sources**: 8-10 authoritative and specialized sources  
- **Use cases**: Doctoral research, industry reports, policy documents

## Tips & Best Practices

### Writing Effective Research Topics

**✅ Good Topics:**
- "artificial intelligence applications in medical diagnosis"
- "sustainable packaging solutions for e-commerce"
- "remote work productivity challenges and solutions"
- "blockchain technology impact on financial services"

**❌ Avoid These:**
- "AI" (too vague)
- "technology" (too broad)
- "What is the best investment?" (subjective, no clear answer)
- Very long topics over 200 characters

**Topic Writing Tips:**
1. **Be Specific**: Include industry, application, or context
2. **Use Clear Language**: Avoid jargon or acronyms without explanation
3. **Include Timeframe**: Add years or periods if relevant ("trends 2025", "future of...")
4. **Focus on Actionable Topics**: Research that leads to insights or decisions

### Choosing the Right Parameters

**For Academic Research:**
```bash
python cli.py --topic "machine learning bias in hiring algorithms" --depth 4 --user grad_student --length 800
```

**For Content Creation:**
```bash
python cli.py --topic "sustainable fashion consumer behavior 2025" --depth 2 --user content_creator --length 400
```

**For Quick Decision Support:**
```bash 
python cli.py --topic "electric vehicle charging infrastructure challenges" --depth 3 --user policy_maker --length 500 
```

### Optimizing Response Time

**Faster Results:**
- Use **depth 1-2** for quick research
- Keep **summary length under 400** words
- Choose **specific, focused topics**
- Avoid **very recent events** (may require more searching)

**Higher Quality Results:**
- Use **depth 3-4** for comprehensive analysis
- Set **summary length 500-800** words for detailed coverage
- Include **context and timeframe** in topics
- Use **follow-up research** for specialized deep-dives

### Managing Research Sessions

**Organize by User ID:**
```
# Use consistent user IDs for related research
--user "project_alpha_researcher"
--user "market_analysis_team"
--user "john_thesis_research"
```


**Research Session Planning:**
1. **Start broad** with depth 2-3
2. **Identify specific areas** for follow-up
3. **Deep dive** with depth 4-5 and follow-up enabled
4. **Verify findings** with additional targeted research

### Source Quality Assessment

**High-Quality Indicators:**
- **Relevance Score > 0.8**: Highly relevant to your topic
- **Credibility Score > 0.7**: Trustworthy and authoritative sources
- **Recent Dates**: Current information for trending topics
- **Diverse Sources**: Multiple perspectives and source types

**Using Source Information:**
- **Always verify** important claims with original sources
- **Check publication dates** for time-sensitive information
- **Cross-reference** findings across multiple sources
- **Note credibility scores** when citing sources

## Troubleshooting

### Common Issues and Solutions

#### "Request Timeout" Errors
**Cause**: Research taking longer than expected
**Solutions**:
- Reduce depth level (try depth 2-3 instead of 4-5)
- Shorten summary length (try 300-500 words instead of 1000+)
- Simplify the topic (make it more specific and focused)
- Try again later (server may be busy)

#### "Validation Error" Messages
**Cause**: Input parameters don't meet requirements
**Solutions**:
- **Topic too short**: Make sure topic is at least 5 characters
- **Invalid depth**: Use numbers 1-5 only
- **Empty user_id**: Provide any non-empty user identifier
- **Invalid length**: Use summary length between 50-2000 words

#### "API Connection Failed"
**Cause**: Network or server issues
**Solutions**:
- Check internet connection
- Verify the API URL is correct
- Try the health check: https://ai-research-assistant-production-1ef8.up.railway.app/health
- Wait a few minutes and try again

#### Poor Quality Results
**Cause**: Topic too vague or inappropriate parameters
**Solutions**:
- Make topic more specific and focused
- Increase depth level for more comprehensive research
- Use follow-up research for specialized topics
- Adjust summary length for appropriate level of detail

#### CLI Tool Issues
**Cause**: Installation or environment problems
**Solutions**:
- Verify Python 3.10+ is installed: `python --version`
- Install requirements: `pip install -r requirements.txt`
- Check environment variables: `echo $API_BASE_URL`
- Try interactive mode: `python cli.py --interactive`

### Error Code Reference

| HTTP Code | Meaning | Solution |
|-----------|---------|----------|
| 200 | Success | Request completed successfully |
| 422 | Validation Error | Check input parameters |
| 500 | Server Error | Try again later or contact support |
| Timeout | Request Timeout | Reduce complexity or retry |

### Getting Help

**Self-Help Resources:**
1. **Interactive Documentation**: https://ai-research-assistant-production-1ef8.up.railway.app/docs
2. **Health Check**: https://ai-research-assistant-production-1ef8.up.railway.app/health
3. **This User Guide**: Complete reference for all features

**Contact Support:**
- **GitHub Issues**: [Here](https://github.com/Raito03/research-brief-generator/issues)
- **Email**:     [Email Me](mailto:anugraha0606@hotmail.com)
- **Documentation**: [Link to full documentation](https://ai-research-assistant-production-1ef8.up.railway.app/docs)

## Frequently Asked Questions

### General Usage

**Q: How long does it take to generate a research brief?**
A: Response times vary by depth level:
- Depth 1-2: 15-40 seconds
- Depth 3: 35-50 seconds  
- Depth 4: 45-70 seconds
- Depth 5: 60-90 seconds

**Q: How many sources will my research brief include?**
A: Source count varies by depth:
- Depth 1: 2-3 sources
- Depth 2: 3-4 sources
- Depth 3: 4-6 sources
- Depth 4: 6-8 sources
- Depth 5: 8-10 sources

**Q: Can I research any topic?**
A: Yes, but some work better than others:
- ✅ Best: Factual, informational topics with available web sources
- ✅ Good: Current events, technology, business, science, education
- ⚠️ Limited: Very personal topics, private company internal information
- ❌ Avoid: Illegal activities, personal medical advice, financial advice

**Q: Is there a limit to how many requests I can make?**
A: Currently no explicit limits, but fair usage policies apply. Heavy usage may be automatically throttled.

### Technical Questions

**Q: What AI model does the system use?**
A: Primarily OpenRouter's Sonoma Dusk Alpha model, with fallback to other models if needed.

**Q: How recent is the information?**
A: The system performs real-time web searches, so information is as current as available web sources.

**Q: Can I use this for commercial purposes?**
A: The system is designed for educational and research purposes. For commercial use, please contact us.

**Q: Is my research data stored?**
A: No personal research data is permanently stored. Session data is temporarily cached for follow-up research only.

### Advanced Usage

**Q: How does follow-up research work?**
A: When you use the same `user_id` with `follow_up: true`, the AI maintains context from previous research sessions, providing more focused and connected analysis.

**Q: Can I integrate this into my application?**
A: Yes! Use the REST API for integration. See the API Integration section of this guide.

**Q: What's the difference between summary length settings?**
A: Summary length controls the total word count of executive summary and detailed analysis sections. The AI automatically distributes content appropriately.

**Q: Can I get results in different languages?**
A: Currently optimized for English research topics and sources. Other languages may work but results quality may vary.

### Troubleshooting

**Q: Why did my request time out?**
A: Requests may time out if they're too complex. Try reducing the depth level or making the topic more specific.

**Q: Why are my results not relevant?**
A: Make your topic more specific. For example, use "machine learning applications in retail inventory management" instead of just "machine learning".

**Q: Can I cancel a request in progress?**
A: Web interface requests cannot be cancelled once submitted. CLI requests can be cancelled with Ctrl+C.

**Q: Why do I get validation errors?**
A: Check that your topic is 5-200 characters, depth is 1-5, user_id is not empty, and summary_length is 50-2000 words.

---

**Need more help?** Visit our interactive documentation at: https://ai-research-assistant-production-1ef8.up.railway.app/docs

**User Guide Version**: 1.0.0  
**Last Updated**: September 18, 2025  
**System Compatibility**: All current versions
