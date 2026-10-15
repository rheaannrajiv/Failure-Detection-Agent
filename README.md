# Failure Detective AI

A local, educational mechanical fault diagnosis assistant built with Streamlit, Python, and Ollama. It combines a conversational interface with a rule-based diagnostic knowledge base.

## Features
- Local language-model chat through Ollama (no paid API key required).
- Mechanical fault knowledge base covering 18 failure categories.
- Symptom-based candidate ranking and suggested inspection checks.
- Inspection workflow, investigation history, and downloadable diagnostic report.
- Dark industrial interface with animated CSS visuals.

## Requirements
- Windows, macOS, or Linux with Python installed.
- Ollama installed and running.
- The `llama3.2:3b` model (or the model configured in `app.py`).

## Setup on Windows
1. Install Ollama from https://ollama.com/download
2. In Command Prompt, download the model:
   ```bash
   ollama run llama3.2:3b
   ```
   After it responds, type `/bye`.
3. Open Command Prompt in this project folder and install packages:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   python -m streamlit run app.py
   ```
5. Open the local URL printed in the terminal, usually http://localhost:8501.

## How it works
1. The user describes a machine problem in the chat.
2. The app identifies symptoms it can recognize and updates the rule-based assessment.
3. The diagnostic engine ranks candidate failure modes and suggests inspection checks.
4. Ollama generates a conversational explanation using the current diagnostic context.
5. The user can record inspection findings and generate a report.

## Development schema
See `DEVELOPMENT_SCHEMA.md` for the workflow diagram.

## Important limitations
This is an educational prototype, not a certified maintenance or safety system. Diagnostic scores are heuristic rankings, not calibrated probabilities. Symptom extraction and coverage are limited to the implemented knowledge base. A qualified technician should verify findings before maintenance decisions. The local model's responses may be incorrect; do not use them as the sole basis for safety-critical actions.
