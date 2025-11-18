# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BettaFish (微舆) is a multi-agent public opinion analysis system built from scratch. It helps users break information bubbles, restore public opinion, predict future trends, and assist decision-making. Users simply chat with the system to describe their analysis needs, and intelligent agents automatically analyze 30+ mainstream social media platforms and millions of public comments.

## Development Commands

### Environment Setup

```bash
# Create conda environment (recommended Python 3.9+)
conda create -n bettafish python=3.11
conda activate bettafish

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser drivers (required for crawler functionality)
playwright install chromium
```

### Configuration

1. Copy `.env.example` to `.env` and configure:
   - Database connection (PostgreSQL or MySQL)
   - LLM API keys for each agent (Insight, Media, Query, Report, Forum Host)
   - Search API keys (Tavily, Bocha)

2. All configuration is managed via `.env` file using Pydantic Settings
3. The `config.py` module loads settings from `.env` or environment variables

### Running the Application

**Full System (Recommended):**
```bash
python app.py
# Access at http://localhost:5000
```

**Individual Agents (for testing):**
```bash
# Insight Engine (private database mining)
streamlit run SingleEngineApp/insight_engine_streamlit_app.py --server.port 8501

# Media Engine (multimodal content analysis)
streamlit run SingleEngineApp/media_engine_streamlit_app.py --server.port 8502

# Query Engine (web search)
streamlit run SingleEngineApp/query_engine_streamlit_app.py --server.port 8503
```

**Crawler System:**
```bash
cd MindSpider

# Initialize database
python main.py --setup

# Extract hot topics
python main.py --broad-topic

# Run complete crawling workflow
python main.py --complete --date 2024-01-20

# Run deep sentiment crawling
python main.py --deep-sentiment --platforms xhs dy wb
```

### Testing

```bash
# Run tests (if available)
pytest

# Check code quality
flake8
black .
```

## Architecture

### Multi-Agent System Design

BettaFish uses a **forum-based collaborative mechanism** where specialized agents work together:

1. **Insight Agent** (`InsightEngine/`) - Private database mining and analysis
   - Primary LLM: Kimi (kimi-k2-0711-preview recommended)
   - Performs deep analysis on private sentiment databases
   - Uses local sentiment analysis models for accuracy

2. **Media Agent** (`MediaEngine/`) - Multimodal content analysis
   - Primary LLM: Gemini 2.5 Pro (recommended)
   - Powerful multimodal capabilities for images/videos
   - Processes content from Douyin, Kuaishou, etc.

3. **Query Agent** (`QueryEngine/`) - Web search and news aggregation
   - Primary LLM: DeepSeek Chat (recommended)
   - Searches domestic and international news
   - Integrates with Tavily and Bocha search APIs

4. **Report Agent** (`ReportEngine/`) - Intelligent report generation
   - Primary LLM: Gemini 2.5 Pro (recommended)
   - Dynamically selects templates from `report_template/`
   - Multi-round generation for high-quality reports

5. **Forum Engine** (`ForumEngine/`) - Agent coordination and debate
   - Forum host LLM: Qwen Plus (recommended)
   - Monitors agent logs and facilitates debate
   - Generates moderator summaries to guide discussion

### Complete Analysis Flow

1. User submits query via Flask web interface
2. Three agents (Insight, Media, Query) start in parallel
3. Each agent performs initial overview search with specialized tools
4. Agents develop research strategies based on initial results
5. **Forum Loop** (multiple rounds):
   - Agents conduct deep research guided by forum host
   - ForumEngine monitors agent logs and generates moderator summaries
   - Agents adjust research direction based on forum discussion
6. Report Agent collects all analysis results and forum content
7. Report Agent generates final HTML report with dynamic template selection

### Key Components

**Flask Main Application (`app.py`):**
- Manages Streamlit sub-applications via subprocess
- Provides REST API and WebSocket interface
- Handles configuration management via `/api/config` endpoints
- Coordinates system startup and shutdown

**ForumEngine (`ForumEngine/monitor.py`):**
- Monitors log files from all three search agents
- Captures SummaryNode outputs (FirstSummaryNode, ReflectionSummaryNode)
- Writes agent speeches to `logs/forum.log`
- Triggers forum host to generate moderation speeches every 5 agent messages
- Implements ERROR block filtering to skip malformed content

**Agent Base Pattern:**
Each agent follows similar structure:
- `agent.py` - Main agent logic and workflow orchestration
- `nodes/` - Processing nodes (search, summary, formatting, etc.)
- `llms/` - LLM interface wrappers (OpenAI-compatible)
- `tools/` - Specialized tools for each agent
- `utils/` - Configuration and utility functions
- `state/` - Agent state management

**Database Layer:**
- Supports both PostgreSQL and MySQL (configured via `DB_DIALECT`)
- Uses SQLAlchemy for ORM
- Schema defined in `MindSpider/schema/`
- Crawler populates sentiment database with social media data

**LLM Integration:**
- All LLMs use OpenAI-compatible API format
- Each agent/component has independent API configuration (KEY, BASE_URL, MODEL_NAME)
- Configuration managed centrally via `config.py` Pydantic Settings
- Supports any LLM provider compatible with OpenAI API format

### Directory Structure

```
BettaFish/
├── QueryEngine/           # Web search agent
├── MediaEngine/           # Multimodal analysis agent
├── InsightEngine/         # Database mining agent
├── ReportEngine/          # Report generation agent
├── ForumEngine/           # Agent coordination and debate
├── MindSpider/            # Web crawler system
│   ├── BroadTopicExtraction/      # Topic extraction
│   ├── DeepSentimentCrawling/     # Deep sentiment crawling
│   └── schema/                    # Database schema
├── SentimentAnalysisModel/        # Sentiment analysis models
│   ├── WeiboMultilingualSentiment/  # Multilingual (recommended)
│   ├── WeiboSentiment_SmallQwen/   # Small parameter Qwen3
│   ├── WeiboSentiment_Finetuned/   # BERT/GPT-2 fine-tuned
│   └── WeiboSentiment_MachineLearning/  # Traditional ML
├── SingleEngineApp/       # Individual agent Streamlit apps
├── ReportEngine/report_template/  # Report templates (markdown)
├── templates/             # Flask HTML templates
├── static/                # Static assets
├── logs/                  # Runtime logs (forum.log, insight.log, etc.)
├── final_reports/         # Generated HTML reports
├── utils/                 # Shared utilities
├── app.py                 # Flask main application
├── config.py              # Configuration management
└── requirements.txt       # Python dependencies
```

## Development Guidelines

### Working with Agents

When modifying agent behavior:
- Each agent's configuration is in `{AgentName}/utils/config.py`
- Key parameters: `max_reflections`, `max_search_results`, `max_content_length`
- Agent state is managed via dataclasses in `{AgentName}/state/state.py`
- Tools are independent modules in `{AgentName}/tools/`

### Working with LLM Configuration

- All LLM configuration is in `.env` file
- Each component has dedicated API settings (e.g., `INSIGHT_ENGINE_API_KEY`)
- The `config.py` uses Pydantic Settings for automatic `.env` loading
- To reload config at runtime: `from config import reload_settings; reload_settings()`

### Working with ForumEngine

- ForumEngine monitors `logs/insight.log`, `logs/media.log`, `logs/query.log`
- Only captures content from SummaryNode outputs
- Automatically filters out ERROR-level logs
- Forum host generates summaries every 5 agent messages (configurable)
- Forum content written to `logs/forum.log` with format: `[HH:MM:SS] [SOURCE] content`

### Adding Custom Business Data

To integrate custom business databases:
1. Add database config to `.env` file
2. Create custom tool in `InsightEngine/tools/` (e.g., `custom_db_tool.py`)
3. Integrate tool into `InsightEngine/agent.py`
4. Update prompts in `InsightEngine/prompts/prompts.py` if needed

### Adding Report Templates

1. Create markdown template in `ReportEngine/report_template/`
2. Use clear section headers and structure
3. The Report Agent will automatically discover and select appropriate templates
4. Templates can also be uploaded via web interface

### Sentiment Analysis Models

The system integrates multiple sentiment analysis approaches:
- **Multilingual** (recommended): `SentimentAnalysisModel/WeiboMultilingualSentiment/`
- **Small Qwen3**: `SentimentAnalysisModel/WeiboSentiment_SmallQwen/`
- **BERT/GPT-2**: `SentimentAnalysisModel/WeiboSentiment_Finetuned/`
- **Traditional ML**: `SentimentAnalysisModel/WeiboSentiment_MachineLearning/`

Configuration in `InsightEngine/tools/sentiment_analyzer.py`

## Important Notes

### Database Initialization

- Database is automatically initialized when running `app.py`
- Tables are created based on schemas in `MindSpider/schema/`
- No manual database setup required

### Port Configuration

Default ports:
- Flask main app: 5000
- Insight Engine: 8501 (Streamlit) + 8601 (API)
- Media Engine: 8502 (Streamlit) + 8602 (API)
- Query Engine: 8503 (Streamlit) + 8603 (API)

If Streamlit processes don't shut down cleanly, manually kill processes on these ports.

### Environment Variables

The system uses `.env` file for all configuration. Never commit `.env` with actual API keys. Always use `.env.example` as template.

### Code Style

- Python 3.9+ required (3.11 recommended)
- Uses loguru for logging
- Async operations with aiohttp/asyncio where applicable
- Type hints encouraged but not strictly enforced

### Security Considerations

- Never commit API keys or database credentials
- The crawler respects robots.txt and rate limits
- Be mindful of data privacy when analyzing public opinion
- Use prepared statements for all database queries (SQLAlchemy handles this)

## Troubleshooting

**"Process already running on port"**: Kill existing Streamlit processes
```bash
# Windows
netstat -ano | findstr :<port>
taskkill /PID <pid> /F

# Linux/Mac
lsof -ti:<port> | xargs kill -9
```

**"Database connection failed"**: Verify `.env` database settings match your database server

**"LLM API error"**: Check API keys and base URLs in `.env` file. Ensure the model name matches provider's API.

**"ForumEngine not capturing content"**: Check that logs contain SummaryNode outputs and are not ERROR-level

**"Playwright browser not found"**: Run `playwright install chromium`

## Performance Optimization

- Use GPU version of PyTorch for faster sentiment analysis:
  ```bash
  pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
  ```
- Adjust search limits in agent configs to balance speed vs. depth
- Use Redis caching for frequently accessed data (optional, not implemented by default)
- Consider deploying agents on separate machines for production use

## Docker Deployment

```bash
# Start all services in background
docker compose up -d

# Database configuration in docker-compose environment
DB_HOST=db  # Service name in docker-compose.yml
DB_PORT=5432
DB_USER=bettafish
DB_PASSWORD=bettafish
DB_NAME=bettafish
```

## Future Development

The project roadmap includes:
- Predictive models using time-series and graph neural networks
- Enhanced multimodal fusion capabilities
- Additional social media platform integrations
- Improved real-time monitoring and alerting
