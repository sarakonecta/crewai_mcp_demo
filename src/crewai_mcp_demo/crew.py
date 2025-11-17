from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import yaml
from typing import Any
from crewai_mcp_demo.tools.mcp_google_search import MCPGoogleSearchTool
from crewai_mcp_demo.tools.mcp_github import MCPGitHubTool
from crewai_mcp_demo.tools.mcp_filesystem import MCPFilesystemTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@CrewBase
class CrewaiMcpDemo():
    """CrewaiMcpDemo crew for technology stack validation"""
    
    # paths to config files (relative to this package)
    agents_config_path = os.path.join(os.path.dirname(__file__), "config", "agents.yaml")
    tasks_config_path = os.path.join(os.path.dirname(__file__), "config", "tasks.yaml")
    # runtime attributes created by the decorators; annotate to satisfy type checkers
    agents: Any = None
    tasks: Any = None
    
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
        # Configure LiteLLM
        self.llm_config = {
            "model": os.getenv("LITELLM_MODEL", "gemini-2.5-flash"),
            "api_base": os.getenv("LITELLM_API_BASE"),
            "api_key": os.getenv("LITELLM_API_KEY"),
        }
        
        # Initialize tools
        self.google_search_tool = MCPGoogleSearchTool()
        self.github_tool = MCPGitHubTool()
        self.filesystem_tool = MCPFilesystemTool()
    
    @agent
    def technology_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['technology_researcher'],
            tools=[self.google_search_tool],
            verbose=True,
            llm=self.llm_config
        )
    
    @agent
    def github_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['github_analyst'],
            tools=[self.github_tool, self.google_search_tool],
            verbose=True,
            llm=self.llm_config
        )
    
    @agent
    def risk_assessor(self) -> Agent:
        return Agent(
            config=self.agents_config['risk_assessor'],
            tools=[self.google_search_tool],
            verbose=True,
            llm=self.llm_config
        )
    
    @agent
    def decision_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['decision_advisor'],
            tools=[self.filesystem_tool],
            verbose=True,
            llm=self.llm_config
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
    def assess_risks(self) -> Task:
        cfg = self.tasks_config.get('assess_risks', {})
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