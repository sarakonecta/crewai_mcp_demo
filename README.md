# Tech Stack Validator with CrewAI

A multi-agent AI system that evaluates and analyzes technology stacks using native tools and APIs for web search and GitHub analysis.

## Objective

Research and validate technology stacks by analyzing:
- **Web presence** and community engagement
- **GitHub repositories** (health, activity, maturity)
- **Project viability** and long-term sustainability

The system generates comprehensive evaluation reports with actionable recommendations.

## Technologies Used

- **CrewAI** (multi-agent orchestration)
- **Native Tools** (direct API integration)
  - Google Search MCP (HTTP - web and image search)
  - GitHub REST API (native tools for repository analysis)
- **LiteLLM** (Gemini 2.5 Flash)
- **Python** (>=3.10 and <3.14)

## System Architecture

### AI Agents (3)

1. **Technology Researcher** - Web and image search for technology information
2. **GitHub Analyst** - Repository analysis using GitHub REST API (commits, issues, PRs)
3. **Decision Advisor** - Synthesis and recommendations

### Tools

- **Google Search MCP** - Web search capabilities (HTTP)
- **GitHub Native Tools** - Direct REST API access (no Docker required)
  - `GitHubRepoTool` - Repository information and metrics
  - `GitHubCommitsTool` - Recent commit activity
  - `GitHubIssuesTool` - Open/closed issues tracking
  - `GitHubPullRequestsTool` - Pull request analysis

## Prerequisites

- Python >=3.10 and <3.14
- API credentials:
  - LiteLLM Proxy API Key (or OpenAI/Anthropic/etc.)
  - GitHub Personal Access Token
  - Google Search MCP API Key

## Installation

### Step 1: Install Dependencies
```bash
# Install UV package manager
pip install uv

# Install project dependencies
uv sync
```

Or using crewAI CLI:
```bash
crewai install
```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root:
```env
# LLM Configuration
OPENAI_API_BASE=your-api-base-here
OPENAI_API_KEY=sk-your-api-key-here
MODEL=openai/gemini-2.5-flash

# Google Search MCP (HTTP endpoint)
GOOGLE_SEARCH_MCP_URL=your-google-search-mcp-url-here
GOOGLE_SEARCH_MCP_KEY=your-google-search-key-here

# GitHub API
GITHUB_API_KEY=ghp_your_github_token_here
```

### Step 3: Get Your API Keys

#### GitHub Personal Access Token
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`, `read:user`
4. Copy token to `GITHUB_API_KEY` in `.env`

#### LiteLLM / OpenAI Key
- For LiteLLM proxy: Get your proxy URL and API key
- For OpenAI directly: Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)

## How to Run

### Basic Execution
```bash
# Interactive mode (prompts for technology name)
python main.py

# Or with crewAI CLI
crewai run

# Direct execution with technology name
python main.py Supabase
python main.py "Next.js 14"
python main.py FastAPI
```

### Streamlit App (`app.py`)

A Streamlit frontend is included at the repository root as `app.py`. It provides a simple web UI where you can enter a technology name and run the CrewAI crew; the app will poll the Crew endpoint and display the crew's markdown output.

To run the Streamlit app:

```bash
# Activate your virtual environment, then:
streamlit run app.py
```

Configuration notes:
- The app reads `CREW_URL` and `BEARER_TOKEN` from Streamlit secrets (e.g. `.streamlit/secrets.toml`) via `st.secrets`.
- Ensure `CREW_URL` points to your deployed CrewAI endpoint and `BEARER_TOKEN` is set before running the app.


## Output

The system generates a comprehensive evaluation including:

- **Technology Overview** - Description and main features
- **Community Metrics** - GitHub stars, forks, activity
- **Project Health** - Recent commits, open issues, maintenance status
- **Repository Analysis** - Health score (1-10) with justification
- **Recommendation** - Clear verdict with strengths and concerns
- **Use Cases** - When to use or avoid the technology

All output is displayed in the terminal.

## Customization

Modify the system by editing:

- **`src/crewai_mcp_demo/config/agents.yaml`** - Agent roles, goals, and backstories
- **`src/crewai_mcp_demo/config/tasks.yaml`** - Task definitions and expected outputs
- **`src/crewai_mcp_demo/crew.py`** - Tools, LLM configuration, agent settings
- **`src/crewai_mcp_demo/main.py`** - Entry point and business logic
- **`src/crewai_mcp_demo/tools/github_tools.py`** - GitHub tool implementations

## Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `OPENAI_API_BASE` | LLM API endpoint | Yes | `https://api.openai.com/v1` |
| `OPENAI_API_KEY` | LLM API authentication | Yes | `sk-xxxxxxxx` |
| `MODEL` | LLM model identifier | Yes | `openai/gemini-2.5-flash` |
| `GOOGLE_SEARCH_MCP_URL` | Google Search endpoint | Yes | `https://kon-mcp-google-search-...` |
| `GOOGLE_SEARCH_MCP_KEY` | Search API key | Yes | `your-api-key-here` |
| `GITHUB_API_KEY` | GitHub access token | Yes | `ghp_xxxxxxxx` |

## Cost Control

The system is optimized for cost efficiency:

- **Max 3 iterations per agent** - Prevents excessive API calls
- **Max 3 tool calls for GitHub analysis** - Limits GitHub API usage
- **Sample-based analysis** - Uses last 10 commits/issues instead of full history
- **Efficient prompting** - Clear, concise task definitions

Estimated cost per evaluation: **< $0.10** (varies by LLM provider)

## Troubleshooting

### GitHub API Rate Limits
- **Problem:** "API rate limit exceeded"
- **Solution:** 
  - Authenticated requests get 5,000 requests/hour
  - Check your token is valid: `curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit`
  - Wait for rate limit reset or use a different token

### Missing API Keys
- **Problem:** "GITHUB_API_KEY not found" or similar
- **Solution:** 
  - Verify `.env` file is in project root
  - Check variable names match exactly (case-sensitive)
  - Restart terminal/IDE after updating `.env`

### Module Import Errors
- **Problem:** `ModuleNotFoundError: No module named 'crewai_mcp_demo'`
- **Solution:**
  - Run from project root directory
  - Ensure dependencies installed: `uv sync` or `crewai install`
  - Try: `pip install -e .`

## Project Structure
```
crewai_mcp_demo/
├── src/
│   └── crewai_mcp_demo/
│       ├── config/
│       │   ├── agents.yaml          # Agent definitions
│       │   └── tasks.yaml           # Task configurations
│       ├── tools/
│       │   ├── __init__.py          # Tool exports
│       │   └── github_tools.py      # GitHub native tools
│       ├── crew.py                  # Main crew logic
│       └── main.py                  # Entry point
├── app.py                           # Streamlit frontend (Tech Stack Validator)
├── .env                             # Environment variables
├── pyproject.toml                   # Project dependencies
└── README.md                        # This file
```


## Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [GitHub REST API](https://docs.github.com/en/rest)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [CrewAI Discord Community](https://discord.com/invite/X4JWnZnxPb)
