import os
from typing import Any, List

import yaml
from dotenv import load_dotenv

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.mcp import MCPServerStdio, MCPServerHTTP
from crewai.mcp.filters import create_static_tool_filter


# Load .env from project root
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path=env_path, override=True)

@CrewBase
class CrewaiMcpDemo():
    """CrewaiMcpDemo crew for technology stack validation"""
    
    # paths to config files
    agents_config_path = os.path.join(os.path.dirname(__file__), "config", "agents.yaml")
    tasks_config_path = os.path.join(os.path.dirname(__file__), "config", "tasks.yaml")

    agents: Any = None
    tasks: Any = None

    def __init__(self):
        """Initialize the crew with custom LLM configuration"""
        
        # Debug: print current working directory and env vars
        print(f"🔍 Current directory: {os.getcwd()}")
        print(f"🔍 .env path: {env_path}")
        print(f"🔍 GOOGLE_SEARCH_MCP_KEY exists: {bool(os.getenv('GOOGLE_SEARCH_MCP_KEY'))}")
        
        # Load YAML configs for agents and tasks
        try:
            with open(self.agents_config_path, "r", encoding="utf-8") as f:
                self.agents_config = yaml.safe_load(f) or {}
        except Exception:
            self.agents_config = {}

        try:
            with open(self.tasks_config_path, "r", encoding="utf-8") as f:
                self.tasks_config = yaml.safe_load(f) or {}
        except Exception:
            self.tasks_config = {}
            
        # Configure LLM model
        self.llm_model = os.getenv("MODEL", "openai/gemini-2.5-flash")
        
        # Get API keys from environment
        self.google_search_key = os.getenv("GOOGLE_SEARCH_MCP_KEY")
        if not self.google_search_key:
            print("WARNING: GOOGLE_SEARCH_MCP_KEY not found. Google Search agent may not work.")
            self.google_search_key = ""
        
        # Get paths
        self.reports_dir = os.getenv("REPORTS_DIR", r"C:\Users\ssansalvador\Documents\Projects\tech_stack_reports")
    
    @agent
    def technology_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['technology_researcher'],
            mcps=[
                # Google Search via HTTP/Streamable
                MCPServerHTTP(
                    url=os.getenv("GOOGLE_SEARCH_MCP_URL", "https://kon-mcp-google-search-805102662749.us-central1.run.app/mcp"),
                    headers={"Authorization": f"{self.google_search_key}"},
                    streamable=True,
                    tool_filter=create_static_tool_filter(
                        allowed_tool_names=["search_web", "search_images"]
                    ),
                    cache_tools_list=True,
                ),
            ],
            verbose=True,
            llm=self.llm_model,
            allow_delegation=False,
        )
    
    @agent
    def github_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['github_analyst'],
            mcps=[
                # GitHub MCP via Docker Stdio (sin Gateway)
                MCPServerStdio(
                    command="docker",
                    args=[
                        "run",
                        "-i",
                        "--rm",
                        "-e", f"GITHUB_PERSONAL_ACCESS_TOKEN={os.getenv('GITHUB_API_KEY')}",
                        "mcp/github"
                    ],
                    tool_filter=create_static_tool_filter(
                        allowed_tool_names=["get_repository", "list_commits", "list_issues"]
                    ),
                    cache_tools_list=True,
                ),
            ],
            verbose=True,
            llm=self.llm_model,
            allow_delegation=False,
        )
    
    @agent
    def decision_advisor(self) -> Agent:
        # Asegurar que la carpeta existe
        reports_path = r"C:\Users\ssansalvador\Documents\Projects\tech_stack_reports"
        os.makedirs(reports_path, exist_ok=True)
        
        # Convertir path de Windows a formato Docker
        docker_path = reports_path.replace("\\", "/")
        
        print(f"📁 Filesystem mount: {reports_path}")
        print(f"📁 Docker path: {docker_path}:/mnt/reports")
        
        return Agent(
            config=self.agents_config['decision_advisor'],
            mcps=[
                # Filesystem MCP via Docker Stdio
                MCPServerStdio(
                    command="docker",
                    args=[
                        "run",
                        "-i",
                        "--rm",
                        "-v", f"{docker_path}:/mnt/reports",
                        "mcp/filesystem",
                        "/mnt/reports"
                    ],
                    tool_filter=create_static_tool_filter(
                        allowed_tool_names=["write_file", "read_file", "list_directory", "create_directory"]
                    ),
                    cache_tools_list=True,
                ),
            ],
            verbose=True,
            llm=self.llm_model,
            allow_delegation=False,
        )
    
    @task
    def research_technology(self) -> Task:
        cfg = self.tasks_config.get('research_technology', {})
        return Task(
            description=cfg.get('description', ''),
            expected_output=cfg.get('expected_output', ''),
            config=cfg,
        )
    
    @task
    def analyze_github_health(self) -> Task:
        cfg = self.tasks_config.get('analyze_github_health', {})
        return Task(
            description=cfg.get('description', ''),
            expected_output=cfg.get('expected_output', ''),
            config=cfg,
        )
    
    @task
    def generate_recommendation(self) -> Task:
        cfg = self.tasks_config.get('generate_recommendation', {})
        return Task(
            description=cfg.get('description', ''),
            expected_output=cfg.get('expected_output', ''),
            config=cfg,
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiMcpDemo crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
    