"""
Create a Pandas agent that answers natural language questions about a CSV.
Uses LangChain's create_pandas_dataframe_agent helper.

Usage:
    export OPENAI_API_KEY="sk-..."
    python csv_analyst.py data.csv
"""

import sys
import pandas as pd
from dotenv import load_dotenv

# ✅ Updated imports (newer LangChain structure)
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# Load environment variables from .env
load_dotenv()

def run_agent(csv_path: str):
    # ✅ Load CSV into Pandas DataFrame
    df = pd.read_csv(csv_path)
    print(f"CSV loaded successfully with shape {df.shape} and columns {list(df.columns)}")

    # ✅ Create LLM and agent
    llm = ChatOpenAI(temperature=0)
    agent = create_pandas_dataframe_agent(
        llm, 
        df, 
        verbose=False, 
        allow_dangerous_code=True   # <--- required!
    )

    print("Ask questions about the data (type 'exit' to quit).")

    while True:
        q = input("\nQuestion: ").strip()
        if q.lower() in ("exit", "quit"):
            break
        try:
            res = agent.invoke(q)   # invoke returns a dict
            print("\nAnswer:\n", res["output"])
        except Exception as e:
            print("Agent error:", e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python csv_analyst.py data.csv")
        sys.exit(1)
    run_agent(sys.argv[1])
