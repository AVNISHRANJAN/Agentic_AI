from fastmcp import FastMCP
import subprocess
mcp =FastMCP("Docker MCP Server")

@mcp.tool
def show_running_containers():
    """Tool1: Show running Docker containers."""
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    return result.stdout 

@mcp.tool
def show_docker_logs_by_name(container_name: str):
    """Tool2: Show logs of a specific Docker container."""
    result = subprocess.run(["docker", "logs", container_name], capture_output=True, text=True)
    return result.stdout


if __name__ == "__main__":
    mcp.run()