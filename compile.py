#!/usr/bin/env python3
import os
import re

def compile_booklet():
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    chapters_dir = os.path.join(workspace_dir, "chapters")
    output_file = os.path.join(workspace_dir, "booklet.md")

    if not os.path.exists(chapters_dir):
        print(f"Error: 'chapters/' directory not found at {chapters_dir}")
        print("Please create individual chapter files under the 'chapters/' folder first.")
        return

    # Find and sort chapter files
    chapter_files = []
    for f in os.listdir(chapters_dir):
        if f.endswith(".md") and re.match(r"^\d+_", f):
            chapter_files.append(f)
    
    chapter_files.sort(key=lambda x: int(x.split("_")[0]))

    if not chapter_files:
        print("No chapter files found in 'chapters/' directory matching pattern '\d+_*'")
        return

    print(f"Found {len(chapter_files)} chapters to compile...")

    # Write Master Booklet
    with open(output_file, "w", encoding="utf-8") as out:
        # Title Page
        out.write("# The Ultimate Interview Preparation Booklet\n\n")
        out.write("### Data Science, Generative AI, AI/ML, and Software Engineering Roles\n\n")
        out.write("**A Professional Technical Handbook & Interview Mentor**\n\n")
        out.write("---\n\n")
        out.write("<div style='page-break-after: always;'></div>\n\n")

        # Table of Contents placeholder
        out.write("## Table of Contents\n\n")
        toc_lines = []

        # Read and compile chapters
        compiled_content = []
        for file_name in chapter_files:
            file_path = os.path.join(chapters_dir, file_name)
            print(f"Processing: {file_name}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            
            # Extract main chapter title (first # header)
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            else:
                title = file_name.replace(".md", "").replace("_", " ").title()

            chapter_num = int(file_name.split("_")[0])
            anchor = title.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "")
            toc_lines.append(f"{chapter_num}. [{title}](#{anchor})")
            
            # Format compiled content
            chapter_data = f"\n\n<div style='page-break-before: always;'></div>\n\n"
            chapter_data += content
            compiled_content.append(chapter_data)

        # Write TOC
        for line in toc_lines:
            out.write(f"- {line}\n")
        out.write("\n---\n\n")

        # Write Chapters
        for block in compiled_content:
            out.write(block)

    print(f"\nSuccess! Compiled booklet saved to: {output_file}")

if __name__ == "__main__":
    compile_booklet()
