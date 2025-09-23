"""
Given a list of article URLs, fetch (via newspaper3k), summarize each article,
and produce a short digest.

Usage:
    export OPENAI_API_KEY="sk-..."
    python news_summarizer.py https://example.com/article1 https://example.com/article2
"""

import sys
from dotenv import load_dotenv
from newspaper import Article

# ✅ Updated imports
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables from .env
load_dotenv()

SUMMARY_PROMPT = """You are a concise news summarizer.
Given the article text, produce:
1) Headline (single line)
2) 2-3 sentence summary
3) 1-sentence "why it matters"

Article:
{article}
"""

def fetch_article(url: str) -> str:
    art = Article(url)
    art.download()
    art.parse()
    return art.title + "\n\n" + art.text

def summarize_text(text: str) -> str:
    llm = ChatOpenAI(temperature=0.2)
    prompt = PromptTemplate(input_variables=["article"], template=SUMMARY_PROMPT)
    chain = LLMChain(llm=llm, prompt=prompt)

    # ✅ use invoke instead of run
    result = chain.invoke({"article": text})
    return result["text"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python news_summarizer.py <article_url> [article_url...]")
        sys.exit(1)

    urls = sys.argv[1:]
    for u in urls:
        print(f"\nFetching: {u}")
        try:
            text = fetch_article(u)
            print("Summarizing...")
            out = summarize_text(text)
            print("\n--- Summary ---\n", out)
        except Exception as e:
            print("Failed for", u, e)
