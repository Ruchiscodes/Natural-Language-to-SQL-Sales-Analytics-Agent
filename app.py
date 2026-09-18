import streamlit as st
import plotly.io as pio
import json
from crew import run_sales_agent

st.set_page_config(page_title="NL-to-SQL Sales Agent", layout="wide")
st.title("📊 Natural Language Sales Analytics Agent")

query = st.text_input("Ask a question about 16M+ sales records:", "Show total sales by region for Q3 2024")

if st.button("Run Analytics"):
    with st.spinner("Orchestrating agents and executing query..."):
        result = run_sales_agent(query)
        st.subheader("Executive Insights")
        st.write(result.raw)
