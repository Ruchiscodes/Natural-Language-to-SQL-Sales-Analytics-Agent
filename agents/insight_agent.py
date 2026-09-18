from crewai import Agent

def create_insight_agent(llm, config: dict, tools: list = None) -> Agent:
    """Agent that runs queries and translates data results into executive insights."""
    return Agent(
        role=config["insight_reporter"]["role"],
        goal=config["insight_reporter"]["goal"],
        backstory=config["insight_reporter"]["backstory"],
        llm=llm,
        tools=tools or [],
        verbose=True,
        allow_delegation=False
    )
