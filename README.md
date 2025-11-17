# CrewaiMcpDemo Crew

Welcome to the CrewaiMcpDemo Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/crewai_mcp_demo/config/agents.yaml` to define your agents
- Modify `src/crewai_mcp_demo/config/tasks.yaml` to define your tasks
- Modify `src/crewai_mcp_demo/crew.py` to add your own logic, tools and specific args
- Modify `src/crewai_mcp_demo/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the crewai-mcp-demo Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The crewai-mcp-demo Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the CrewaiMcpDemo Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.

## GitHub MCP Server (Official) — Cómo usarlo con esta demo

Si tienes activado el "Official GitHub MCP Server" (por ejemplo en Docker Desktop Extensions), puedes hacer que `mcp_github.py` apunte a ese servidor en lugar de llamar directamente a `api.github.com`.

- Qué hace el repositorio: la imagen oficial es `ghcr.io/github/github-mcp-server` (ver: https://github.com/github/github-mcp-server). Esta imagen actúa como un proxy/adapter para las APIs de GitHub y puede correr localmente en Docker.

- Pasos rápidos para probarlo (ejemplo usando PowerShell):

	1. Descargar y ejecutar la imagen Docker (ajusta la versión/puerto según la documentación de la imagen):

```powershell
docker pull ghcr.io/github/github-mcp-server:latest
docker run --rm -p 8080:8080 ghcr.io/github/github-mcp-server:latest
```

	2. Configurar las variables de entorno para que la herramienta use el MCP local (ejemplo):

```powershell
#$env:GITHUB_API_BASE debe apuntar a la URL base del MCP (ajusta el puerto/path si corresponde)
$env:GITHUB_API_BASE = 'http://localhost:8080'
#Si necesitas autenticar, pon tu token de GitHub (o el método que requiera tu MCP)
$env:GITHUB_TOKEN = 'ghp_xxxYOURTOKENxxx'
```

	3. Verificar que el MCP responde (opcional):

```powershell
Invoke-RestMethod -Uri "$env:GITHUB_API_BASE/repos/octocat/hello-world" -Method Get
```

	4. Ejecutar la demo (no interactiva) p. ej. para analizar un repositorio:

```powershell
python -m crewai_mcp_demo.main "facebook/react"
# o usar el CLI del proyecto si lo prefieres:
crewai run
```

- Notas útiles:
	- `mcp_github.py` en este repo ahora puede usar `GITHUB_API_BASE` (por defecto sigue siendo `https://api.github.com`). Ajusta esta variable para apuntar a tu MCP local.
	- Si el MCP exige rutas o cabeceras adicionales, es posible actualizar `mcp_github.py` para enviar los encabezados necesarios. Si quieres, puedo adaptar el cliente para un flujo de autenticación específico del MCP.
	- Si no quieres ejecutar Docker, también puedes usar la extensión de Docker Desktop (si ya la activaste) y arrancar el MCP desde ahí — revisa la URL que expone la extensión y usa esa URL en `GITHUB_API_BASE`.

Si quieres, implemento además:
- Detección automática del MCP local en puertos comunes y uso automático cuando esté activo.
- Un script de prueba integrado que haga una llamada de verificación al iniciar.
