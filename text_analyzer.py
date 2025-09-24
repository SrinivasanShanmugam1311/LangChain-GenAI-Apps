"""
Text Analyzer using LangChain and OpenAI Chat API.

This script reads text from a file, sends it to an LLM for analysis,
and returns the number of characters, words, paragraphs, and sentences
in JSON format.
"""
from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables from .env
load_dotenv()

# Load text from file
txt_file = Path("sample.txt")  # replace with your file path
text = txt_file.read_text()
# Load environment variables from .env
load_dotenv()
# Prompt template for counting
PROMPT = """
You are an expert text analyzer. Given the text below, return:
1) Number of characters include everything
2) Number of words
3) Number of paragraphs
4) Number of sentences

Text:
{text}

Provide the output in JSON format with keys: characters, words, paragraphs, sentences
"""

prompt = PromptTemplate(input_variables=["text"], template=PROMPT)

# Initialize LLM
llm = ChatOpenAI(temperature=0)

# Build chain
chain = LLMChain(llm=llm, prompt=prompt)

# Get result
result = chain.invoke({"text": text})
print(result)
