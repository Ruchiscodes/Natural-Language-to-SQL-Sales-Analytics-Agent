# Natural Language to SQL Sales Analytics Agent

An enterprise multi-agent analytics system capable of processing 16M+ records under 14 seconds query latency.

## Architecture & Features
- **Data Pipeline:** DuckDB + PyArrow for fast ingestion from Parquet into SQLite with targeted indexing.
- **Agent Orchestration:** CrewAI workflow leveraging Azure GPT-4.1 for SQL generation and insight reporting.
- **Validation Layer:** Integrated SQLCoder-7B validator for schema verification and error correction.
- **Auto-Dashboards:** Automated Plotly payload construction from SQL results.

 
