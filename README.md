# CrewaiMcpDemo Crew

Welcome to the CrewaiMcpDemo Crew project, powered by [crewAI](https://crewai.com). This application uses a multi-agent AI system to evaluate and analyze technology stacks by leveraging MCP (Model Context Protocol) servers for web search, GitHub analysis, and file operations.

## Project Overview

This project implements a **Technology Stack Validator** that:
- **Researches** technologies across the web and GitHub
- **Analyzes** repository health, community activity, and project maturity
- **Generates** comprehensive evaluation reports in Markdown format

The system uses three specialized AI agents:
1. **Technology Researcher** — Web and image search for tech information
2. **GitHub Analyst** — Repository analysis, commits, and issues
3. **Decision Advisor** — Report generation and recommendations

These agents communicate via MCP servers that provide access to various tools.

## Prerequisites

- **Python**: >=3.10 and <3.14
- **Docker Desktop** (for running MCP servers via Docker containers)
- **API Credentials**:
  - LiteLLM Proxy API Key (for LLMs)
  - GitHub Token (for GitHub API access)
  - Google Search MCP API Key (for web search)

## 🔧 Installation

### 1. Install Dependencies

This project uses [UV](https://docs.astral.sh/uv/) for dependency management:

```powershell
# Install UV if not already installed
pip install uv

# Navigate to project directory and install dependencies
uv sync
```

Or using the crewAI CLI:

```powershell
crewai install
```

### 2. Configure Environment Variables

Create or update the `.env` file in the project root with the following variables:

```env
# LiteLLM API Configuration
OPENAI_API_BASE=your-api-base-here
OPENAI_API_KEY=sk-your-api-key-here
MODEL=your-model-here

# Google Search MCP Configuration
GOOGLE_SEARCH_MCP_URL=your-google-search-mcp-url-here
GOOGLE_SEARCH_MCP_KEY=your-google-search-key-here

# GitHub Configuration
GITHUB_TOKEN=your-github-token-here

# Output Directory (where reports will be saved)
REPORTS_DIR=C:/Users/your-username/Documents/tech_stack_reports

# GitHub MCP and Filesystem MCP (local Docker Desktop gateway)
GITHUB_MCP_URL=http://localhost:3000/sse/github-official
FILESYSTEM_MCP_URL=http://localhost:3000/sse/filesystem
MCP_KEY=your-mcp-key-here

```

> **IMPORTANT: About MCP_KEY**
> 
> The `MCP_KEY` value is **generated dynamically** each time you start the Docker MCP gateway. 
> 
> When you run `docker mcp gateway run --transport sse --port 3000`, a new Bearer token will appear in the terminal output. You **must copy this token** and update the `MCP_KEY` value in your `.env` file before running the crew.
>
> Example terminal output:
> ```
> MCP Gateway started on port 3000
> Bearer token: Bearer 08ztlb3ipjr4q6qj6mjl4apv236uif3kdeeoo8nex9qjwilzt1
> ```
> Copy the entire Bearer token (including "Bearer ") and paste it as the `MCP_KEY` value.

## Running with Docker (MCP Servers)

This project uses MCP servers for enhanced functionality. To run the MCP servers via Docker Desktop:

### 1. Start MCP Servers in Docker

```powershell
# Start the MCP gateway (this will generate a new MCP_KEY in the terminal)
docker mcp gateway run --transport sse --port 3000
```

### 2. Update Your .env File

**CRITICAL STEP**: After starting the Docker gateway, you'll see a Bearer token in the terminal. Copy this token and update your `.env` file:

```env
MCP_KEY=Bearer <the-token-shown-in-terminal>
```

### 3. Keep Docker Container Running

Keep the terminal with the Docker gateway running while you execute the crew in a separate PowerShell window.

## Running the Project

### Basic Usage

Run the crew with a specific technology to evaluate:

```powershell
# Interactive mode (you'll be prompted for technology name)
crewai run

```

## Output

The crew generates a comprehensive Markdown report that includes:
- Technology overview and description
- Community and project health metrics
- GitHub repository analysis (stars, forks, issues, commits)
- Pros and cons evaluation
- Use case recommendations
- Final decision and confidence score

Reports are saved to the directory specified in `REPORTS_DIR` environment variable.

## Customization

Modify the crew behavior by editing:

- **`src/crewai_mcp_demo/config/agents.yaml`** — Define agent roles, goals, and backstories
- **`src/crewai_mcp_demo/config/tasks.yaml`** — Configure tasks and expected outputs
- **`src/crewai_mcp_demo/crew.py`** — Add custom tools, change LLM, modify MCP server configurations
- **`src/crewai_mcp_demo/main.py`** — Add custom inputs and business logic

## MCP Server Configuration

The project connects to multiple MCP servers via HTTP/SSE:

```python
mcp_server_params = [
    # Google Search MCP (Streamable HTTP)
    {"url": "https://kon-mcp-google-search-805102662749.us-central1.run.app/mcp", ...},
    
    # GitHub Official MCP (SSE over Docker)
    {"url": "http://localhost:3000/sse/github-official", ...},
    
    # Filesystem MCP (SSE over Docker)
    {"url": "http://localhost:3000/sse/filesystem", ...}
]
```

## Environment Variables Explained

| Variable | Purpose | Example |
|----------|---------|---------|
| `OPENAI_API_BASE` | LiteLLM proxy endpoint | `https://litellm-proxy-....run.app` |
| `OPENAI_API_KEY` | API key for LLM access | `sk-xxxxxxxx` |
| `MODEL` | LLM model to use | `openai/gemini-2.5-flash` |
| `GOOGLE_SEARCH_MCP_URL` | Google Search MCP endpoint | `https://kon-mcp-google-search-...` |
| `GOOGLE_SEARCH_MCP_KEY` | Google Search API key | `c056b48168956702f4...` |
| `GITHUB_TOKEN` | GitHub Personal Access Token | `ghp_xxxxxxxx` |
| `REPORTS_DIR` | Output directory for reports | `C:/Users/.../tech_stack_reports` |
| `GITHUB_MCP_URL` | GitHub MCP SSE endpoint (local gateway) | `http://localhost:3000/sse/github-official` |
| `FILESYSTEM_MCP_URL` | Filesystem MCP SSE endpoint (local gateway) | `http://localhost:3000/sse/filesystem` |
| `MCP_KEY` | Authentication key for MCP endpoints (**regenerated each Docker session**) | `Bearer 08ztlb3ipjr4q6qj6mjl4apv...` |

## Troubleshooting

### Docker Container Won't Stay Running
- Ensure Docker Desktop is open and running
- Use `-d` flag to run in background: `docker run -d ...`
- Check Docker logs: `docker logs <container-id>`

### MCP Server Connection Errors
- Verify Docker container is running: `docker ps`
- Test connection: `curl http://localhost:3000/sse/github-official`
- Check firewall/port availability (port 3000)
- **Verify you've updated the `MCP_KEY` in `.env` with the token from the terminal**

### Authentication Errors with MCP
- **Most common issue**: The `MCP_KEY` in your `.env` file is outdated
- Stop the Docker gateway, restart it, and copy the new Bearer token
- Update `.env` with the new token before running the crew again

### API Errors
- Verify all `.env` variables are set correctly
- Check API key validity and permissions
- Ensure GitHub token has necessary scopes
- Test LiteLLM endpoint connectivity

### Module Not Found Errors
- Run `uv sync` to ensure all dependencies are installed
- Verify Python version is >=3.10: `python --version`
- Check virtual environment activation

## Further Resources

- [crewAI Documentation](https://docs.crewai.com)
- [MCP Documentation](https://modelcontextprotocol.io)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [LiteLLM Documentation](https://docs.litellm.ai/)

## Support

For issues or questions:
- Check the [crewAI GitHub repository](https://github.com/joaomdmoura/crewai)
- Visit [crewAI Discord Community](https://discord.com/invite/X4JWnZnxPb)
- Review the [LiteLLM Documentation](https://docs.litellm.ai/)