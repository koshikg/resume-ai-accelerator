# ResumeAI Accelerator

ResumeAI Accelerator is a workflow to extract, clean, and elevate your resume using AI. It automates resume processing and leverages Large Language Models (LLMs) to take your CV to the next level. This guide includes prerequisites, scripts, and status update conventions for LLM agents.


## Who Can Use This?

ResumeAI Accelerator is designed for:

- **Developers & Tech Professionals:** Effortlessly extract, clean, and enhance your resume for job applications, promotions, or professional branding.
- **Recruiters & Talent Acquisition Teams:** Quickly extract and analyze candidate information from resumes for streamlined screening and evaluation.
- **Anyone Seeking a Better Resume:** Whether you’re a student, career changer, or professional in any field, ResumeAI Accelerator helps you create a polished, AI-enhanced CV with minimal effort.

No advanced technical skills are required—if you can run a Python script, you can use ResumeAI Accelerator.

## Prerequisites

**Recommended:** Use the provided Dev Container for a fully configured environment (see next section). All dependencies are pre-installed.

**Manual setup (only if not using the Dev Container):**
- Ensure your resume (in .docx format) is present in the `data/` directory.
- Python 3.7+ environment with the following packages installed:
  - `python-docx`
  - `docx2txt`

## Development Container (Dev Container) Usage

You can develop and run ResumeAI Accelerator in a fully configured, reproducible environment using VS Code Dev Containers.

**To use the Dev Container:**

1. Install [Visual Studio Code](https://code.visualstudio.com/) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2. Open this project folder in VS Code.
3. When prompted, or via the Command Palette (`Ctrl+Shift+P`), select **Dev Containers: Reopen in Container**.
4. VS Code will build and open the project inside a container with all dependencies pre-installed.
5. Run scripts and develop as usual—your environment is ready to go!

This ensures consistency and eliminates "works on my machine" issues.

## Prompt for LLM Agents
After confirming the prerequisite, prompt the LLM as follow:
 
You are an AI agent tasked with automating and enhancing resume processing. Please follow these steps:
- Read and understand the contents of the instructions.md file in the root directory.
- Based on the instructions, create a taskmaster.md file in the root directory. This file should list all required tasks for the workflow, each with a status field (e.g., New, InProgress, Complete).
- For every query or operation you perform, always keep the context of both instructions.md and taskmaster.md in memory. Refer to these files before taking any action.
- As you start, progress, or complete any task, update the status of that task in taskmaster.md accordingly.
- Continue this process for all tasks, ensuring that taskmaster.md always reflects the current state of the workflow.

  ---

## This template on Overleaf

<a href="https://www.overleaf.com/latex/templates"><img alt="Overleaf" src="https://img.shields.io/badge/Overleaf-47A141.svg?style=for-the-badge&logo=Overleaf&logoColor=white"/></a>

Also, if you have a premium subscription to Overleaf, you can use Overleaf's GitHub integration to push changes to your GitHub repo directly from Overleaf.

## How to populate template with your data
Use LLM to generate `data.txt` file.
Execute below script to generate the tex file.
`scripts/render_resume.py --data "output/Resume - Kaushik Gayal_data.txt" --output cv.generated.tex`

## Compiling the CV on your local computer
- type `make` in the `root` directory to produce file `cv.pdf`
- you can optionally type `make clean` or `make distclean` to remove intermediate files


By following these steps, ResumeAI Accelerator helps you automate extraction, cleaning, and AI-powered enhancement of your resume for job applications or professional use.
