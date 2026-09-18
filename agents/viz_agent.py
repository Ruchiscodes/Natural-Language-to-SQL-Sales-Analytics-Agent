from crewai import Agent

def create_viz_agent(llm, config: dict, tools: list = None) -> Agent:
    """Agent that creates interactive Plotly chart structures from SQL results."""
    return Agent(
        role=config["viz_agent"]["role"],
        goal=config["viz_agent"]["goal"],
        backstory=config["viz_agent"]["backstory"],
        llm=llm,
        tools=tools or [],
        verbose=True,
        allow_delegation=False
    )
