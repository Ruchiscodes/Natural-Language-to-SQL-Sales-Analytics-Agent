import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import tool
import sqlite3
import plotly.express as px
import pandas as pd

load_dotenv()

# Azure GPT-4.1 configuration
azure_llm = LLM(
    model="azure/gpt-4.1",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-15-preview"
)

# SQLCoder-7B validation fallback model
sqlcoder_llm = LLM(
    model="ollama/sqlcoder:7b",
    base_url="http://localhost:11434"
)

@tool("Database Query Tool")
def execute_sql(query: str) -> str:
    """Executes a SQL query against the SQLite 16M+ record sales database."""
    conn = sqlite3.connect("sales_data.db")
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.to_json(orient="records")
    except Exception as e:
        conn.close()
        return f"Error: {str(e)}"

# Agents
sql_generator = Agent(
    role="Senior SQL Engineer",
    goal="Translate user natural language intent into efficient SQLite queries.",
    backstory="Expert in ANSI SQL and performance optimization over multi-million row databases.",
    llm=azure_llm,
    verbose=True
)

sql_validator = Agent(
    role="SQL Validator & Context Corrector",
    goal="Validate syntax, optimize indexes, and correct SQL errors using specialized domain context.",
    backstory="Specialized in SQLCoder-7B parsing rules and structural schema verification.",
    llm=sqlcoder_llm,
    verbose=True
)

insight_reporter = Agent(
    role="Sales Strategy Analyst",
    goal="Analyze query execution output and formulate executive summary reports.",
    backstory="Experienced data strategist skilled at spotting trend anomalies and KPIs.",
    llm=azure_llm,
    verbose=True
)

viz_agent = Agent(
    role="Data Visualization Engineer",
    goal="Convert JSON query results into Plotly dashboard configuration specifications.",
    backstory="Expert UI designer specializing in automated Plotly chart generation.",
    llm=azure_llm,
    tools=[execute_sql],
    verbose=True
)

def run_sales_agent(user_prompt: str):
    task_sql = Task(
        description=f"Generate an optimized SQL query for: '{user_prompt}'",
        expected_output="Valid SQL query string.",
        agent=sql_generator
    )

    task_validate = Task(
        description="Verify query against schema, check syntax errors, and return validated SQL.",
        expected_output="Syntactically valid SQL query.",
        agent=sql_validator
    )

    task_insight = Task(
        description="Execute query via DB tool and extract key business insights.",
        expected_output="Executive summary with bulleted KPIs.",
        agent=insight_reporter
    )

    task_viz = Task(
        description="Generate Plotly chart payload from query output.",
        expected_output="Python dictionary representing Plotly figure specs.",
        agent=viz_agent
    )

    crew = Crew(
        agents=[sql_generator, sql_validator, insight_reporter, viz_agent],
        tasks=[task_sql, task_validate, task_insight, task_viz],
        process=Process.sequential
    )

    return crew.kickoff()
