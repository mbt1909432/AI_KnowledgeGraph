# AI_KnowledgeGraph
LLM-based knowledge graph constructor and query system


## Overview

This project is designed to provide a backend and frontend application for knowledege graph query system. 
The backend is built using FastAPI and the frontend is served using a simple HTTP server.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Start the Backend](#start-the-backend)
  - [Start the Frontend](#start-the-frontend)
  - [Build Knowledge Graph](#build-knowledge-graph)
- [Configuration](#configuration)
- [Notes](#notes)

## Installation

1. Clone the repository:

2. Install all dependencies listed in requirements.txt:

pip install -r requirements.txt

## Usage

# Start the Backend
Navigate to the BackendCode directory:

cd BackendCode
Run the backend service:

uvicorn app:app --reload --host 0.0.0.0

# Start the Frontend
In another terminal window, run the following command to start the frontend:

python -m http.server 5173 --directory .\FrontendCode\code

Open your browser and go to the following address to view the frontend:

http://127.0.0.1:5173/graph_visualization.html


# Build Knowledge Graph

If you want to build your own knowledge graph, run the graph_rag.py script:

python graph_rag.py 


if __name__ == "__main__":

    insert(CURRENT_DATA_PATH)

Make sure to manually modify the CURRENT_DATA_PATH to point to the correct data location.


## Configuration

In the BackendCode/config/settings.py file, enter your API key:

DEEPSEEK_API_KEY = 'your_api_key_here'
You can purchase the API key at https://www.deepseek.com/.

Configure the OpenAI key by adding it to your system environment variables for embedding retrieval. This can typically be done in your operating system's environment settings.


