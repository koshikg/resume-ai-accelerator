import docx2txt
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, 'data', 'Resume - Kaushik Gayal.docx')
output_path = os.path.join(BASE_DIR, 'output', 'Resume - Kaushik Gayal_full.txt')

if __name__ == "__main__":
    text = docx2txt.process(data_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Full extraction complete.")
