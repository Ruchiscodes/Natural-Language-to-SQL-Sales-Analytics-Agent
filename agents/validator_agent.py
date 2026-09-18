from crewai import Agent

def create_validator_agent(sqlcoder_llm, config: dict) -> Agent:
    """Validator agent leveraging SQLCoder-7B for syntax and schema correction."""
    return Agent(
        role=config["sql_validator"]["role"],
        goal=config["sql_validator"]["goal"],
        backstory=config["sql_validator"]["backstory"],
        llm=sqlcoder_llm,
        verbose=True,
        allow_delegation=False
    )
