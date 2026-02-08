import os
import subprocess
from pathlib import Path

# -------------------------------
# CONFIG
# -------------------------------
START_PATH = r"D:\AI-Atlas\Docs\01-Foundations-of-AI\02-Intelligent-Agents\01-agents-and-environments.md"
END_PATH = r"D:\AI-Atlas\Docs\08-Responsible-Explainable-AI\05-Governance-and-Regulation\04-summary.md"
DOCS_DIR = r"D:\AI-Atlas\Docs"

def get_all_md_files(root_dir):
    md_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md") and file.lower() != "readme.md":
                md_files.append(os.path.join(root, file))
    # Sort them to ensure consistent range identification
    md_files.sort()
    return md_files

def main():
    md_files = get_all_md_files(DOCS_DIR)
    
    try:
        start_index = md_files.index(START_PATH)
    except ValueError:
        print(f"❌ Could not find start path: {START_PATH}")
        # Try relative or variations if needed, but let's assume absolute works first
        return

    try:
        end_index = md_files.index(END_PATH)
    except ValueError:
        print(f"❌ Could not find end path: {END_PATH}")
        return

    target_files = md_files[start_index : end_index + 1]
    total = len(target_files)
    print(f"🚀 Found {total} files in the specified range.")

    for i, file_path in enumerate(target_files, 1):
        print(f"[{i}/{total}] Processing: {file_path}")
        # Run the fill_docs script for each file
        # We use subprocess to avoid any potential namespace pollution or issues
        try:
            subprocess.run(["python", "fill_docs.py", "--file", file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()
