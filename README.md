# Tech Stack Validator with CrewAI

A multi-agent AI system that evaluates and analyzes technology stacks using MCP (Model Context Protocol) servers for web search, GitHub analysis, and file operations.

## Objective

Research and validate technology stacks by analyzing:
- **Web presence** and community engagement
- **GitHub repositories** (health, activity, maturity)
- **Project viability** and long-term sustainability

The system generates comprehensive evaluation reports in Markdown format.

## Technologies Used

- **CrewAI** (multi-agent orchestration)
- **MCP Servers** (Model Context Protocol)
  - Google Search MCP (web and image search)
  - GitHub Official MCP (repository analysis)
  - Filesystem MCP (file operations)
- **LiteLLM** (Gemini 2.5 Flash)
- **Docker** (MCP server hosting)
- **Python** (>=3.10 and <3.14)

## System Architecture

### AI Agents (3)

1. **Technology Researcher** - Web and image search for technology information
2. **GitHub Analyst** - Repository analysis, commits, and issues tracking
3. **Decision Advisor** - Report generation and recommendations

### MCP Servers

- **Google Search MCP** - Web search capabilities (HTTP)
- **GitHub MCP** - Repository data access (SSE via Docker)
- **Filesystem MCP** - Report file operations (SSE via Docker)

## Prerequisites

- Python >=3.10 and <3.14
- Docker Desktop installed and running
- API credentials:
  - LiteLLM Proxy API Key
  - GitHub Personal Access Token
  - Google Search MCP API Key

## Installation

### Step 1: Install Dependencies
```powershell
# Install UV package manager
pip install uv

# Install project dependencies
uv sync
```

Or using crewAI CLI:
```powershell
crewai install
```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root:
```env
# LiteLLM Configuration
OPENAI_API_BASE=your-api-base-here
OPENAI_API_KEY=sk-your-api-key-here
MODEL=your-model-here

# Google Search MCP
GOOGLE_SEARCH_MCP_URL=your-google-search-mcp-url-here
GOOGLE_SEARCH_MCP_KEY=your-google-search-key-here

# GitHub
GITHUB_TOKEN=your-github-token-here

# Output Directory
REPORTS_DIR=C:/Users/your-username/Documents/tech_stack_reports

# MCP Gateway (Docker)
GITHUB_MCP_URL=http://localhost:3000/sse/github-official
FILESYSTEM_MCP_URL=http://localhost:3000/sse/filesystem
MCP_KEY=Bearer your-token-here
```

### Step 3: Start MCP Gateway
```powershell
docker mcp gateway run --transport sse --port 3000
```

** IMPORTANT:** Copy the Bearer token from the terminal output and update `MCP_KEY` in your `.env` file:
```
MCP Gateway started on port 3000
Bearer token: Bearer 08ztlb3ipjr4q6qj6mjl4apv236uif3kdeeoo8nex9qjwilzt1
```

Copy the entire token (including "Bearer ") to your `.env` file.

## How to Run

### Basic Execution
```powershell
# Interactive mode (prompts for technology name)
crewai run
```

Keep the Docker gateway running in a separate terminal while executing the crew.

## Output

The system generates a comprehensive Markdown report including:

- **Technology Overview** - Description and main features
- **Community Metrics** - GitHub stars, forks, contributors
- **Project Health** - Commits, issues, release frequency
- **Repository Analysis** - Code quality, documentation
- **Pros & Cons** - Balanced evaluation
- **Use Cases** - Recommended scenarios
- **Final Decision** - Confidence score and recommendation

Reports are saved to the `REPORTS_DIR` specified in your `.env` file.

## Customization

Modify the system by editing:

- **`src/crewai_mcp_demo/config/agents.yaml`** - Agent roles, goals, and backstories
- **`src/crewai_mcp_demo/config/tasks.yaml`** - Task definitions and expected outputs
- **`src/crewai_mcp_demo/crew.py`** - Tools, LLM configuration, MCP servers
- **`src/crewai_mcp_demo/main.py`** - Custom inputs and business logic

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_BASE` | LiteLLM proxy endpoint | `https://litellm-proxy-...run.app` |
| `OPENAI_API_KEY` | LLM API authentication | `sk-xxxxxxxx` |
| `MODEL` | LLM model identifier | `openai/gemini-2.5-flash` |
| `GOOGLE_SEARCH_MCP_URL` | Google Search endpoint | `https://kon-mcp-google-search-...` |
| `GOOGLE_SEARCH_MCP_KEY` | Search API key | `c056b48168956702f4...` |
| `GITHUB_TOKEN` | GitHub access token | `ghp_xxxxxxxx` |
| `REPORTS_DIR` | Report output directory | `C:/Users/.../tech_stack_reports` |
| `GITHUB_MCP_URL` | GitHub MCP endpoint | `http://localhost:3000/sse/github-official` |
| `FILESYSTEM_MCP_URL` | Filesystem MCP endpoint | `http://localhost:3000/sse/filesystem` |
| `MCP_KEY` | MCP authentication token (**regenerated each Docker session**) | `Bearer 08ztlb3ipjr4q6qj...` |

## Troubleshooting

### MCP_KEY Issues (Most Common)
- **Problem:** Authentication errors with MCP servers
- **Solution:** The `MCP_KEY` is regenerated every time you start the Docker gateway
  1. Stop the Docker gateway
  2. Restart it: `docker mcp gateway run --transport sse --port 3000`
  3. Copy the new Bearer token from terminal
  4. Update `.env` with the new token

## Project Structure
```
crewai_mcp_demo/
├── src/
│   └── crewai_mcp_demo/
│       ├── config/
│       │   ├── agents.yaml      # Agent definitions
│       │   └── tasks.yaml       # Task configurations
│       ├── crew.py              # Main crew logic
│       └── main.py              # Entry point
├── .env                         # Environment variables
├── pyproject.toml              # Project dependencies
└── README.md                   # This file
```

## Resources

- [crewAI Documentation](https://docs.crewai.com)
- [MCP Documentation](https://modelcontextprotocol.io)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [crewAI Discord Community](https://discord.com/invite/X4JWnZnxPb)