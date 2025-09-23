import os
import PyPDF2
import argparse
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # ✅ updated import
from langchain.prompts import ChatPromptTemplate
import json
import traceback

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Extract text from PDF
def extract_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Convert resume text/PDF to JSON
def resume_to_json(input_path=None, resume_text=None):
    if input_path:
        resume_text = extract_pdf_text(input_path)
    elif not resume_text:
        raise ValueError("Either input_path or resume_text must be provided.")

    # Prompt template
    prompt_template = """
    Extract the following information from this resume text and return it strictly as valid JSON:
    {{
      "Name": "",
      "Email": "",
      "Phone": "",
      "Education": "",
      "Experience": [],
      "Skills": []
    }}

    Resume Text:
    {text}

    IMPORTANT: 
    - Return ONLY valid JSON.
    - Do not include ```json or any extra text.
    """
    chat_prompt = ChatPromptTemplate.from_template(prompt_template)

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

    # Run pipeline
    pipeline = chat_prompt | llm
    output_message = pipeline.invoke({"text": resume_text})
    return output_message.content.strip()  # ensure clean string

# Main function with CLI
def main():
    parser = argparse.ArgumentParser(description="Extract resume info to JSON using gpt-4o-mini")
    parser.add_argument("--pdf", type=str, help="Path to the PDF resume")
    parser.add_argument("--text", type=str, help="Direct resume text")
    parser.add_argument("--output", type=str, default="resume_output.json", help="Output JSON file name")
    args = parser.parse_args()

    try:
        result_str = resume_to_json(input_path=args.pdf, resume_text=args.text)

        # Try parsing JSON safely
        try:
            data = json.loads(result_str)
        except json.JSONDecodeError:
            print("⚠️ Model returned invalid JSON. Cleaning response...")
            # Auto-fix common cases like ```json wrappers
            cleaned = result_str.strip().replace("```json", "").replace("```", "")
            data = json.loads(cleaned)

        # Pretty print
        pretty_json = json.dumps(data, indent=4)
        print(pretty_json)

        # Save JSON
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(pretty_json)
        print(f"\n✅ Saved JSON to {args.output}")

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()

if __name__ == "__main__":
    main()
