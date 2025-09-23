"""
Resume vs Job Description Matching using LangChain embeddings.

Supports: .txt, .pdf, .doc/.docx resumes
Usage:
    export OPENAI_API_KEY="sk-..."
    python resume_jd_match.py resume.pdf job_description.txt
"""

import re
from pathlib import Path
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import docx
from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import OpenAIEmbeddings

# Load .env variables
load_dotenv()

# -------------------------
# Step 1: Read resume file
# -------------------------
def read_resume(file_path):
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"{file_path} not found")
    
    if p.suffix.lower() == ".txt":
        return p.read_text()
    
    elif p.suffix.lower() == ".pdf":
        text = ""
        reader = PdfReader(str(p))
        for page in reader.pages:
            text += page.extract_text() + " "
        return text
    
    elif p.suffix.lower() in [".doc", ".docx"]:
        doc = docx.Document(str(p))
        text = " ".join([para.text for para in doc.paragraphs])
        return text
    
    else:
        raise ValueError(f"Unsupported file type: {p.suffix}")

# -------------------------
# Step 2: Preprocess text
# -------------------------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = text.split()
    return " ".join(words)

# -------------------------
# Step 3: Semantic similarity using LangChain embeddings
# -------------------------
def compute_similarity(resume_text, jd_text):
    emb = OpenAIEmbeddings()
    resume_vec = emb.embed_query(resume_text)
    jd_vec = emb.embed_query(jd_text)

    # cosine similarity
    score = cosine_similarity([resume_vec], [jd_vec])[0][0]
    return score

# -------------------------
# Step 4: Main
# -------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python resume_jd_match.py resume_file jd_file")
        sys.exit(1)

    resume_file = sys.argv[1]
    jd_file = sys.argv[2]

    resume_text = read_resume(resume_file)
    jd_text = Path(jd_file).read_text()

    # Preprocess
    resume_text_clean = preprocess_text(resume_text)
    jd_text_clean = preprocess_text(jd_text)

    # Compute semantic similarity
    similarity_score = compute_similarity(resume_text_clean, jd_text_clean)
    print(f"\nSemantic Match Score (0-1): {similarity_score:.2f}")

    # Optional: simple keyword overlap for reference
    resume_words = set(resume_text_clean.split())
    jd_words = set(jd_text_clean.split())
    matching_keywords = resume_words.intersection(jd_words)

    print(f"Matching keywords ({len(matching_keywords)}): {matching_keywords}")
    print(f"Resume-only keywords ({len(resume_words - jd_words)}): {resume_words - jd_words}")
    print(f"JD-only keywords ({len(jd_words - resume_words)}): {jd_words - resume_words}")
