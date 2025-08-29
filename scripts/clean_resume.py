import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(BASE_DIR, 'output', 'Resume - Kaushik Gayal_full.txt')
output_path = os.path.join(BASE_DIR, 'output', 'Resume - Kaushik Gayal_cleaned.txt')

def clean_resume(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Remove empty lines and strip whitespace
    lines = [line.strip() for line in lines if line.strip()]

    # Remove consecutive duplicate lines
    cleaned_lines = []
    prev_line = None
    for line in lines:
        if line != prev_line:
            cleaned_lines.append(line)
        prev_line = line

    # Remove repeated sections (e.g., repeated summaries, skills, experience blocks)
    # We'll use a set to track seen blocks
    seen_blocks = set()
    final_lines = []
    block = []
    for line in cleaned_lines:
        if line.isupper() and len(line.split()) < 6:  # likely a section header
            if block:
                block_text = '\n'.join(block)
                if block_text not in seen_blocks:
                    final_lines.extend(block)
                    seen_blocks.add(block_text)
                block = []
            block.append(line)
        else:
            block.append(line)
    if block:
        block_text = '\n'.join(block)
        if block_text not in seen_blocks:
            final_lines.extend(block)

    # Add extra line breaks after section headers for readability
    output_lines = []
    for i, line in enumerate(final_lines):
        output_lines.append(line)
        if line.isupper() and (i+1 == len(final_lines) or not final_lines[i+1].isupper()):
            output_lines.append('')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

if __name__ == "__main__":
    clean_resume(input_path, output_path)
    print("Cleaned resume created.")
