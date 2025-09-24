#!/usr/bin/env python3
"""
code_explainer_chunked.py
Explain large code files by chunking (map → reduce) using LangChain.

Usage:
  python code_explainer_chunked.py .\amdgpu_Drv.c --encoding utf-8 --chunk-chars 8000 --overlap 400
  # or pick a section only:
  python code_explainer_chunked.py .\amdgpu_Drv.c --start-line 1 --end-line 800
"""

import os, sys, argparse
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

SYSTEM_PROMPT = (
    "You are an expert senior developer and patient teacher. "
    "Explain code clearly for a beginner without dumbing it down."
)

CHUNK_PROMPT = """You will explain a portion of a larger codebase.

Focus on this CHUNK only.
Provide:
- what this chunk does
- main functions/types and responsibilities
- any potential gotchas
- a one-sentence summary

Chunk (preserve formatting):
```text
{code_chunk}
```"""

REDUCE_PROMPT = """You are given multiple per-chunk explanations from the same file.
Synthesize a coherent, non-repetitive, beginner-friendly overall explanation.

Deliver:
1) High-level purpose of the file
2) Key components/functions and what each is responsible for
3) Notable flags/parameters or tricky areas (gotchas)
4) One-sentence summary

Per-chunk notes:
{chunk_summaries}
"""

def build_chain(model: str, temperature: float):
    llm = ChatOpenAI(model=model, temperature=temperature)
    return llm, StrOutputParser()

def explain_chunk(llm, parser, chunk_text: str) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("user", CHUNK_PROMPT)]
    )
    chain = prompt | llm | parser
    return chain.invoke({"code_chunk": chunk_text})

def reduce_summaries(llm, parser, summaries: list[str]) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("user", REDUCE_PROMPT)]
    )
    chain = prompt | llm | parser
    joined = "\n\n---\n\n".join(summaries)
    return chain.invoke({"chunk_summaries": joined})

def chunk_text_by_chars(text: str, chunk_chars: int, overlap: int) -> list[str]:
    if chunk_chars <= 0: return [text]
    chunks = []
    i = 0
    n = len(text)
    while i < n:
        end = min(i + chunk_chars, n)
        chunk = text[i:end]
        chunks.append(chunk)
        if end == n: break
        i = max(end - overlap, 0)
    return chunks

def maybe_slice_by_lines(text: str, start_line: int|None, end_line: int|None) -> str:
    if start_line is None and end_line is None: return text
    lines = text.splitlines()
    s = 1 if start_line is None else max(1, start_line)
    e = len(lines) if end_line is None else min(len(lines), end_line)
    return "\n".join(lines[s-1:e])

def parse_args():
    ap = argparse.ArgumentParser(description="Explain large code files by chunking.")
    ap.add_argument("path", help="Path to code file")
    ap.add_argument("--encoding", default="utf-8", help="File encoding (default utf-8)")
    ap.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    help="OpenAI chat model (default: gpt-4o-mini or OPENAI_MODEL env)")
    ap.add_argument("--temp", type=float, default=0.0, dest="temperature",
                    help="Sampling temperature (default 0.0)")
    ap.add_argument("--chunk-chars", type=int, default=8000,
                    help="Max characters per chunk (default 8000)")
    ap.add_argument("--overlap", type=int, default=400,
                    help="Overlap characters between chunks (default 400)")
    ap.add_argument("--start-line", type=int, help="Start line (1-based) to limit scope")
    ap.add_argument("--end-line", type=int, help="End line (inclusive) to limit scope")
    return ap.parse_args()

def main():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set (use .env or export it).", file=sys.stderr)
        sys.exit(2)

    args = parse_args()
    p = Path(args.path)
    if not p.exists():
        print(f"ERROR: file not found: {p}", file=sys.stderr)
        sys.exit(2)

    try:
        raw = p.read_text(encoding=args.encoding, errors="strict")
    except UnicodeDecodeError:
        # Graceful fallback if the encoding guess was wrong
        raw = p.read_text(encoding="latin-1", errors="replace")

    # Optional slice by line range to keep costs down / target a region
    text = maybe_slice_by_lines(raw, args.start_line, args.end_line)

    # Chunk
    chunks = chunk_text_by_chars(text, args.chunk_chars, args.overlap)

    llm, parser = build_chain(args.model, args.temperature)

    summaries = []
    for idx, c in enumerate(chunks, start=1):
        print(f"[map] Explaining chunk {idx}/{len(chunks)} (len={len(c)})...", file=sys.stderr)
        summaries.append(explain_chunk(llm, parser, c))

    print("\n--- Per-chunk Explanations (map) ---\n")
    for i, s in enumerate(summaries, start=1):
        print(f"### Chunk {i}\n{s}\n")

    print("\n--- Synthesis (reduce) ---\n")
    overall = reduce_summaries(llm, parser, summaries)
    print(overall)

if __name__ == "__main__":
    main()
