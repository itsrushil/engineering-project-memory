# \# Engineering Project Memory

# 

# Engineering Project Memory is an AI-based knowledge assistant for software engineering projects.

# 

# The project helps users find information from project documents, source code and other files by asking questions in normal language. It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information before generating an answer.

# 

# \## Problem Statement

# 

# In a software project, information is usually spread across different files, documentation and source code. Finding a specific piece of information manually can take time.

# 

# For example:

# 

# \- Where is authentication implemented?

# \- Why was a particular database selected?

# \- What happens when a user registers?

# \- Which components are connected to the payment system?

# 

# This project provides a single interface where users can ask these questions and get answers based on the available project information.

# 

# \## Features

# 

# \- Upload project documents and source files

# \- Ask questions using natural language

# \- RAG-based question answering

# \- Show sources used to generate answers

# \- Ingest public GitHub repositories

# \- Analyze architecture diagrams using multimodal AI

# \- Simple AI agent/query planner

# \- Gradio web interface

# \- FastAPI backend

# \- Local vector storage

# 

# \## How It Works

# 

# ```text

# Documents / Source Code / GitHub

# &#x20;             |

# &#x20;             v

# &#x20;       File Ingestion

# &#x20;             |

# &#x20;             v

# &#x20;          Chunking

# &#x20;             |

# &#x20;             v

# &#x20;     Gemini Embeddings

# &#x20;             |

# &#x20;             v

# &#x20;     Local Vector Store

# &#x20;             |

# &#x20;             v

# &#x20;       User Question

# &#x20;             |

# &#x20;             v

# &#x20;     AI Agent / Planner

# &#x20;             |

# &#x20;             v

# &#x20;    Relevant Information

# &#x20;             |

# &#x20;             v

# &#x20;         Gemini LLM

# &#x20;             |

# &#x20;             v

# &#x20;       Answer + Sources

For architecture diagrams, the uploaded image is processed using Gemini's multimodal capabilities to understand the components and connections.

Technologies Used

\- Python

\- Google Gemini API

\- NumPy

\- FastAPI

\- Gradio

\- PyPDF

\- GitHub REST API

\- Python-dotenv

A local vector store is used instead of a separate paid vector database.

Project Structure

engineering-project-memory/

|

├── app/

│   ├── agent.py

│   ├── api.py

│   ├── config.py

│   ├── ingest.py

│   ├── models.py

│   ├── ui.py

│   └── vector\_store.py

|

├── data/

│   └── knowledge/

│       └── project\_memory.md

|

├── .env.example

├── .gitignore

├── README.md

└── requirements.txt



Setup

1\. Clone the Repository

git clone https://github.com/itsrushil/engineering-project-memory.git

cd engineering-project-memory



2\. Create a Virtual Environment

For Windows:

py -3.13 -m venv .venv

.venv\\Scripts\\Activate.ps1



3\. Install the Packages

python -m pip install -r requirements.txt



4\. Configure the Gemini API

Create a file named .env in the project folder.

GEMINI\_API\_KEY=your\_gemini\_api\_key

GEMINI\_MODEL=your\_supported\_gemini\_model

EMBEDDING\_MODEL=gemini-embedding-001

TOP\_K=5

GITHUB\_TOKEN=



Do not upload the .env file to GitHub.

Running the Project

Start the Gradio Interface

python -m app.ui



Open:

http://127.0.0.1:7860



Start the FastAPI Server

Open another terminal in the project folder and run:

uvicorn app.api:app --host 127.0.0.1 --port 8000



Main Features

Project Memory

Documents can be uploaded through the Knowledge section.

The system processes the files, creates embeddings and stores them in the local vector store.

When a question is asked, relevant information is retrieved and sent to Gemini to generate the answer.

GitHub Repository Ingestion

A public GitHub repository can be entered into the GitHub section.

The application processes the repository files and adds their content to the project memory.

This allows users to ask questions about the repository without manually searching through its files.

AI Agent

The project includes a simple AI agent/query planner.

It checks the user's question and decides whether project information needs to be retrieved before generating the response.

Multimodal AI

An architecture diagram can be uploaded through the Multimodal section.

Gemini analyzes the image and explains the components and connections shown in the diagram.

Knowledge Upload

Users can upload project files such as:

\- Text files

\- Markdown files

\- PDF documents

\- Source-code files

The files are processed and added to the project memory.

Example Questions

Why did we choose PostgreSQL?



Where is authentication implemented?



What happens when a user registers?



Which components depend on payment?



How does a request move through the architecture?



Screenshots

Main Interface

The main dashboard provides access to project memory, GitHub ingestion, multimodal analysis and knowledge management.



GitHub Repository Ingestion

Public GitHub repositories can be indexed and added to the project memory.



System Architecture

The architecture shows the flow between the Gradio interface, FastAPI backend, AI agent, RAG pipeline, local vector store and Gemini.



Demo Video

Add the 2–5 minute project demonstration video here.

Demo Link: VIDEO\_LINK\_HERE

The demonstration should cover:

1\. Project introduction

2\. Project Memory / RAG question answering

3\. GitHub repository ingestion

4\. AI agent/query planning

5\. Multimodal architecture analysis

6\. Technologies used

Limitations

\- The project depends on the Gemini API.

\- Gemini free-tier limits can affect the number of requests.

\- The vector store is local and is mainly intended for small projects.

\- GitHub ingestion currently focuses on public repositories.

\- The AI agent is implemented as a simple query planner.

Future Improvements

\- Automatic GitHub synchronization

\- GitHub issue and pull-request support

\- Cloud vector database

\- Better document management

\- More advanced AI agents

\- User authentication

\- Cloud deployment

Conclusion

Engineering Project Memory combines RAG, prompt engineering, multimodal AI and a simple AI agent into one application.

The main goal is to make information inside a software project easier to find without manually searching through multiple files.

Team

Academic engineering project.

