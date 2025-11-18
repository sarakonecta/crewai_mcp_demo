import os
from typing import Any, List

import yaml
from dotenv import load_dotenv

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import BaseTool

from crewai_mcp_demo.tools.mcp_filesystem import MCPFilesystemTool
from crewai_mcp_demo.tools.mcp_github import MCPGitHubTool

load_dotenv()

@CrewBase
class CrewaiMcpDemo():
    """CrewaiMcpDemo crew for technology stack validation"""
    
    # paths to config files
    agents_config_path = os.path.join(os.path.dirname(__file__), "config", "agents.yaml")
    tasks_config_path = os.path.join(os.path.dirname(__file__), "config", "tasks.yaml")

    agents: Any = None
    tasks: Any = None

    mcp_server_params = [
        # Google Search MCP Server (Streamable HTTP)
        {
            "url": "https://kon-mcp-google-search-805102662749.us-central1.run.app/mcp",
            "transport": "streamable-http",
            "headers": {"Authorization": "c056b48160256702f4b54b3ddab4df8a7c0affbdef6b80a63d39f1534f6939f9"},
        }]
    
    def get_mcp_tools(self, *tool_names: str) -> list[BaseTool]:
        ...

    def __init__(self):
        """Initialize the crew with custom LLM configuration"""
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
        # Configure LLM model (use LiteLLM proxy with openai/ prefix for non-OpenAI models)
        self.llm_model = os.getenv("MODEL", "openai/gemini-2.5-flash")
        
        # Initialize tools
        self.github_tool = MCPGitHubTool()
        self.filesystem_tool = MCPFilesystemTool()
    
    @agent
    def technology_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['technology_researcher'],
            tools=self.get_mcp_tools("search_web", "search_images"),
            verbose=True,
            llm=self.llm_model
        )
    
    @agent
    def github_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['github_analyst'],
            tools=[self.github_tool, *self.get_mcp_tools("search_web", "search_images")],
            verbose=True,
            llm=self.llm_model
        )

    
    @agent
    def decision_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['decision_advisor'],
            tools=[self.filesystem_tool],
            verbose=True,
            llm=self.llm_model
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
            agents=self.agents,  # Automatically created by @agent decorator
            tasks=self.tasks,    # Automatically created by @task decorator
            process=Process.sequential,
            verbose=True,
        )