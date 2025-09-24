"""
Takes a code snippet (file or pasted) and explains it in plain English using LangChain.
Usage:
    export OPENAI_API_KEY="sk-..."
    python code_explainer.py path/to/code.py
"""

import sys
from pathlib import Path
from langchain_openai import ChatOpenAI   # ✅ updated import
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

PROMPT = """You are an expert senior developer and teacher.
Explain the following code in clear, simple terms for a beginner.
Highlight:
- what the code does
- main functions/classes and responsibilities
- potential gotchas
- a one-sentence summary

Code:
{code}
"""
# Load environment variables from .env
load_dotenv()
def explain_code(code: str) -> str:
    """Run the LLM chain to explain code in plain English."""
    llm = ChatOpenAI(temperature=0)  # deterministic output
    prompt = PromptTemplate(input_variables=["code"], template=PROMPT)
    chain = LLMChain(llm=llm, prompt=prompt)
    try:
        # ✅ use .invoke instead of .run
        result = chain.invoke({"code": code})
        return result["text"] if "text" in result else str(result)
    except Exception as e:
        return f"Error while generating explanation: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python code_explainer.py path/to/code.py")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print("File not found:", path)
        sys.exit(1)

#    code_text = path.read_text()
    code_text = path.read_text(encoding="utf-8", errors="replace")
    explanation = explain_code(code_text)

    print("\n--- Explanation ---\n")
    print(explanation)
