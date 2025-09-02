
# Project Purpose: Automate and Enhance Resume Processing with LLMs

This project aims to automate the extraction, cleaning, and enhancement of resume content using Large Language Models (LLMs). The workflow enables LLMs and agents to:
- Extract all relevant text from .docx resumes
- Clean and deduplicate the extracted content
- Track progress and tasks using a taskmaster file
- Apply further improvements such as grammar, formatting, and content enrichment

All steps are designed to be performed in small, manageable chunks, with status tracking and clear instructions for both scripts and LLMs.

## Folder Structure

```
resume/
├── data/           # Place your .docx resume file here
├── output/         # All extracted and cleaned files will be saved here
├── scripts/        # All Python scripts for extraction and cleaning
├── instructions.md      # This instructions file (keep in root)
├── taskmaster.md        # Task tracking file (keep in root)
```

## Step 1: Extract Text from the Resume
1. Place your `.docx` resume file in the `data/` directory.
2. Run the extraction script from the `scripts/` folder:
  ```sh
  python scripts/extract_docx2txt.py
  ```
  - This will create a file named `<resume>_full.txt` in the `output/` directory containing all extractable text, including paragraphs, tables, and text boxes.

## Step 1.5: Initialize Taskmaster and LLM Workflow
1. Prompt the LLM using `prompt.md`

## Step 2: Clean and Deduplicate the Extracted Text
1. Run the cleaning script from the `scripts/` folder to remove redundant information and improve readability:
  ```sh
  python scripts/clean_resume.py
  ```
  - This will generate `<resume>_cleaned.txt` in the `output/` directory, a more readable and concise version of your resume.

## Step 3: Use template to inject data from output in step 2
- Read the `data-template.txt` file in the root directory, to determine what details needs to be extracted from step 2 output.
- Create a new data file using the template in `data-template.txt` and insert all the required data that is available from output in step 2.

## Step 4: (Optional) Further Enhancement with LLMs
- Pass the new data text file to an LLM for:
  - Grammar and style improvements
  - Formatting suggestions
  - Content enhancement (e.g., quantifying achievements, improving clarity)  
- Provide clear instructions to the LLM about the desired improvements. Do not change the original content drastically.

## Task Tracking and Status Updates (taskmaster.md file)

- Keep both `instructions.md` and `taskmaster.md` in the root of your `resume` workspace directory (alongside the `data`, `output`, and `scripts` folders).
- All work and status updates must be tracked in a separate file named `taskmaster.md` in the root directory.
- Before starting any operation, always read the `taskmaster.md` file to understand the current state and pending/completed tasks.
- As you progress, update the statuses of each task in the `taskmaster.md` file:
  - **New**: TasPk has not been started.
  - **InProgress**: Task is currently being worked on.
  - **Complete**: Task is finished.
- Continue to update the `taskmaster.md` file throughout the workflow to ensure transparency and traceability for all agents and users.
