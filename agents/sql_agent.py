from crewai import Agent

def create_sql_agent(llm, config: dict) -> Agent:
    """Agent responsible for initial Natural Language to SQL translation."""
    return Agent(
        role=config["sql_generator"]["role"],
        goal=config["sql_generator"]["goal"],
        backstory=config["sql_generator"]["backstory"],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
