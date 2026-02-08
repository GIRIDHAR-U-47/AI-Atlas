import os
import time
import argparse
from pathlib import Path
import google.generativeai as genai

# -------------------------------
# CONFIG
# -------------------------------
ROOT_DIR = "Docs"   # Directory containing the markdown files
MIN_CHARS_TO_SKIP = 300  # if file already has content, skip it
GEMINI_API_KEY = "AIzaSyDjgydQ9zWtsB6HzYnEQ_YfXvgq84VRh4s"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
# Using gemini-flash-latest for accessibility in this environment
model = genai.GenerativeModel('gemini-flash-latest')

def build_prompt(file_path: Path):
    """
    Creates a strong research-grade prompt based on the file name + folder context.
    """
    # Get parts relative to the ROOT_DIR if possible
    try:
        relative_path = file_path.relative_to(Path(ROOT_DIR))
    except ValueError:
        relative_path = file_path

    parts = relative_path.parts
    
    # Example:
    # ('01-Foundations-of-AI', '01-What-is-Intelligence', '01-definition-of-intelligence.md')
    chapter = parts[0] if len(parts) >= 1 else "Unknown Chapter"
    section = parts[1] if len(parts) >= 2 else "Unknown Section"
    topic = file_path.stem.replace("-", " ").title()

    prompt = f"""
You are writing a deeply researched university-level Markdown document
for an open-source project called AI-Atlas.

Context:
- Chapter: {chapter}
- Section: {section}
- Topic: {topic}
- File path: {file_path}

Requirements:
- Write in MIT/Stanford lecture note style
- Must be clear for students and useful for researchers
- Use clean Markdown headings
- Include formal definitions
- Include equations in LaTeX where required (use $ for inline and $$ for block)
- Include intuitive explanations and real-world examples
- Include misconceptions and common pitfalls
- Include connections to modern AI and LLMs where relevant
- Include a "Summary" section
- Include a "Mini Quiz" section (3-5 questions)
- Include a "Research Bibliography" section with well-known books and papers (APA or similar format)
- Avoid vague statements, make it detailed and structured
- Output ONLY Markdown (no extra commentary, no triple backticks at start/end unless they are part of content)

Write the full content of the document now.
"""
    return prompt.strip()

def call_llm(prompt: str):
    """
    Calls Gemini API to generate content.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text
        # Strip potential markdown code block markers if the model adds them
        if text.startswith("```markdown"):
            text = text[12:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    except Exception as e:
        raise Exception(f"Gemini API Error: {e}")

def fill_md_files(limit=None, dry_run=False):
    root = Path(ROOT_DIR)

    if not root.exists():
        print(f"❌ Root directory not found: {ROOT_DIR}")
        return

    # Find all .md files, excluding README.md
    md_files = [f for f in root.rglob("*.md") if f.name.lower() != "readme.md"]
    print(f"📄 Found {len(md_files)} markdown files (excluding READMEs).")

    processed_count = 0
    for file in md_files:
        if limit and processed_count >= limit:
            print(f"⏹️ Reached limit of {limit} files.")
            break

        try:
            existing_text = file.read_text(encoding="utf-8").strip()

            if len(existing_text) >= MIN_CHARS_TO_SKIP:
                print(f"✅ Skipping (already filled): {file}")
                continue

            print(f"⚡ Generating content for: {file}")

            if dry_run:
                print(f"🔍 [Dry Run] Would generate content for: {file}")
                processed_count += 1
                continue

            prompt = build_prompt(file)
            content = call_llm(prompt)

            file.write_text(content, encoding="utf-8")
            print(f"💾 Updated: {file}")
            processed_count += 1
            
            # Rate limiting / Sleep to avoid hitting quotas too fast
            time.sleep(2)

        except Exception as e:
            print(f"❌ Error processing {file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fill empty AI-Atlas documentation files using Gemini API.")
    parser.add_argument("--limit", type=int, help="Limit the number of files to process.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be done without making changes.")
    parser.add_argument("--file", type=str, help="Process a specific markdown file.")
    
    args = parser.parse_args()
    
    if args.file:
        file_path = Path(args.file)
        if file_path.exists():
            print(f"⚡ Generating content for specific file: {file_path}")
            prompt = build_prompt(file_path)
            content = call_llm(prompt)
            file_path.write_text(content, encoding="utf-8")
            print(f"💾 Updated: {file_path}")
        else:
            print(f"❌ File not found: {args.file}")
    else:
        fill_md_files(limit=args.limit, dry_run=args.dry_run)
