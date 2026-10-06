# 🧠 Engineering Project Memory

AI-powered project knowledge assistant demonstrating **LLM, Prompt Engineering, RAG, Embeddings, AI Agents, Multimodal AI, FastAPI and Gradio**.

## Problem
Software project knowledge is distributed across code, documentation, meeting notes, PDFs and architecture diagrams. This project creates an AI memory layer that retrieves relevant information and answers engineering questions with sources.

## Features
- RAG question answering
- Gemini embeddings and local vector search
- Prompt-engineered grounded responses
- Lightweight AI agent/query planner
- GitHub source-code ingestion
- PDF/Markdown/TXT/code ingestion
- Meeting-decision memory
- Multimodal architecture-diagram analysis
- FastAPI API
- Gradio UI
- Source display

## Setup
1. Create a Gemini API key in Google AI Studio.
2. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.
3. Install:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
4. Add knowledge files to `data/knowledge/`.
5. Build memory:
```bash
python -m app.ingest
```
6. Start API:
```bash
uvicorn app.api:app --reload
```
7. In another terminal:
```bash
python -m app.ui
```

## Demo Questions
- Why did we choose PostgreSQL?
- Where is authentication implemented?
- What happens when a user registers?
- Which components depend on the payment module?
- How does a request move through the architecture?

## Architecture
```text
Project Files / Docs / Notes
            ↓
         Chunking
            ↓
    Gemini Embeddings
            ↓
     Local Vector Store
            ↓
       AI Agent
            ↓
       RAG Retrieval
            ↓
   Prompt Engineering
            ↓
       Gemini LLM
            ↓
      Answer + Sources
```

## Submission
Make the GitHub repository public, include screenshots and a 2–5 minute demo video, and submit the repository link before **7 October 2026, 11:59 PM**.

Never commit `.env` or API keys.
