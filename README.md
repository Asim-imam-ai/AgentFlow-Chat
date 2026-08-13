# AgentFlow Chat

An AI-powered conversational agent platform built with **FastAPI**, **Streamlit**, **SQLite**, and **ChromaDB**. The application provides a modular architecture for building and interacting with AI-driven workflows, with persistent conversation data and retrieval-augmented generation (RAG) capabilities.

---

## Overview

**AgentFlow Chat** is designed as a full-stack AI application with a separate backend API and interactive frontend.

The project consists of:

* **FastAPI** — backend API and application services
* **Streamlit** — interactive web frontend
* **SQLite** — persistent application and conversation data
* **ChromaDB** — persistent vector storage for RAG
* **Docker** — containerized application deployment
* **Nginx** — optional reverse proxy for production deployments
* **GitHub Actions** — automated testing and CI/CD workflows

The architecture keeps the frontend and backend independently deployable while allowing them to communicate through the backend API.

---

## Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Streamlit      │
                         │      Frontend       │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP API
                                    ▼
                         ┌─────────────────────┐
                         │       FastAPI       │
                         │       Backend       │
                         └──────┬───────┬──────┘
                                │       │
                    ┌───────────┘       └────────────┐
                    ▼                                ▼
             ┌─────────────┐                  ┌─────────────┐
             │   SQLite    │                  │  ChromaDB   │
             │ Application │                  │ Vector DB   │
             │    Data     │                  │    / RAG    │
             └─────────────┘                  └─────────────┘

                         Optional Production Layer

                         ┌─────────────────────┐
                         │       Nginx         │
                         │   Reverse Proxy     │
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                    FastAPI API           Streamlit UI
```

---

## Project Structure

```text
AgentFlow-Chat/
│
├── .github/
│   └── workflows/
│       └── ...                 # CI/CD workflows
│
├── app/                        # Backend application
├── frontend/                   # Streamlit frontend
├── docker/                     # Docker configuration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── exceptions/                 # Application exceptions
├── scripts/                    # Utility and automation scripts
├── tests/                      # Automated tests
├── utils/                      # Shared utilities
│
├── .dockerignore
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Technology Stack

| Component          | Technology     |
| ------------------ | -------------- |
| Backend            | FastAPI        |
| Frontend           | Streamlit      |
| Language           | Python 3.12    |
| Database           | SQLite         |
| Vector Database    | ChromaDB       |
| Containerization   | Docker         |
| Orchestration      | Docker Compose |
| Reverse Proxy      | Nginx          |
| Package Management | uv             |
| Testing            | pytest         |
| Linting            | Ruff           |
| CI/CD              | GitHub Actions |

---

## Requirements

Before running the project locally, install:

* Python 3.12
* Docker
* Docker Compose
* Git
* `uv`

Depending on the AI and search integrations enabled by the application, API credentials may also be required.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Asim-imam-ai/AgentFlow-Chat.git
cd AgentFlow-Chat
```

Create the environment configuration:

```bash
cp .env.example .env
```

Edit `.env` and provide the required configuration values.

---

## Environment Variables

The application can use external AI and search services through environment variables.

Typical configuration includes:

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
TAVILY_API_KEY=

DATABASE_URL=sqlite:///./data/chatbot_memory.db
CHROMA_DB_PATH=./data/chroma_db
```

> Never commit `.env` or API credentials to GitHub. Use `.env.example` for documenting required variables.

---

# Local Development

## Install Dependencies

The project uses `uv` for Python dependency management.

```bash
uv sync
```

Install the required Python version if necessary:

```bash
uv python install 3.12
```

---

## Run Tests

Run the complete test suite:

```bash
uv run pytest tests -v
```

For a shorter output:

```bash
uv run pytest tests
```

---

## Run Linting

Run Ruff:

```bash
uv run ruff check .
```

---

# Run the Backend

The FastAPI backend can be started with:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The exact application entry point should match the backend module configured in the project.

The backend exposes the application's API and health endpoint.

Health check:

```text
/api/health
```

When running locally, the API is available on:

```text
http://localhost:8000
```

---

# Run the Frontend

The Streamlit frontend communicates with the FastAPI backend.

Set the backend URL:

```bash
export BACKEND_URL=http://localhost:8000
```

Then start Streamlit:

```bash
streamlit run frontend/app.py
```

The frontend is normally available at:

```text
http://localhost:8501
```

---

# Docker Deployment

The project includes Docker configuration for running the complete application stack.

The Docker Compose configuration contains:

* FastAPI backend
* Streamlit frontend
* Nginx reverse proxy
* SQLite persistent storage
* ChromaDB persistent storage
* Upload storage
* Nginx logs

Build the images:

```bash
docker compose -f docker/docker-compose.yml build
```

Start the application:

```bash
docker compose -f docker/docker-compose.yml up -d
```

Check the running containers:

```bash
docker compose -f docker/docker-compose.yml ps
```

View logs:

```bash
docker compose -f docker/docker-compose.yml logs -f
```

Stop the application:

```bash
docker compose -f docker/docker-compose.yml down
```

---

## Docker Services

### Backend

The FastAPI service runs on:

```text
8000
```

Container-to-container communication uses:

```text
http://backend:8000
```

### Frontend

The Streamlit service runs on:

```text
8501
```

### Nginx

Nginx acts as the optional reverse proxy and can expose the application through:

```text
80
443
```

---

# Data Persistence

The application uses file-based persistent storage.

### SQLite

SQLite stores application and conversation data.

Docker volume:

```text
sqlite_data
```

Mounted inside the backend container at:

```text
/app/data
```

### ChromaDB

ChromaDB stores vector data used by retrieval functionality.

Docker volume:

```text
chroma_data
```

Mounted at:

```text
/app/chroma_db
```

### Uploaded Files

Uploaded documents are persisted using:

```text
uploads_data
```

mounted at:

```text
/app/uploads
```

---

# RAG / Vector Search

AgentFlow Chat supports retrieval-oriented workflows using ChromaDB as the persistent vector database.

The general flow is:

```text
Document
   │
   ▼
Processing
   │
   ▼
Chunking / Embedding
   │
   ▼
ChromaDB
   │
   ▼
Similarity Search
   │
   ▼
Relevant Context
   │
   ▼
AI Model
   │
   ▼
Response
```

This allows application workflows to use relevant stored information when generating responses.

---

# Configuration

Application configuration is controlled through environment variables.

For local development, use:

```text
.env
```

For production deployments, provide the required environment variables through the deployment environment rather than committing secrets to the repository.

---

# CI / GitHub Actions

The repository uses GitHub Actions to automate software quality checks.

The CI pipeline can run:

* Dependency installation
* Automated tests
* Ruff linting
* Other repository validation steps

Pull requests and pushes should be validated through the configured GitHub Actions workflows.

---

# Security

Security-sensitive configuration must never be committed to source control.

Do not commit:

```text
.env
*.pem
*.key
credentials.json
API keys
AWS credentials
```

Use environment variables and GitHub Actions Secrets where appropriate.

If an API key or cloud credential is accidentally committed, revoke and rotate it immediately.

---

# Development Guidelines

When contributing to the project:

1. Create a dedicated branch.
2. Make focused changes.
3. Add or update tests when appropriate.
4. Run the test suite locally.
5. Run Ruff before committing.
6. Keep secrets out of source control.
7. Use clear and descriptive commit messages.

Example:

```bash
git checkout -b feature/my-feature

uv run pytest tests -v

uv run ruff check .

git add .
git commit -m "Add my feature"

git push origin feature/my-feature
```

---

# Troubleshooting

## Backend is not responding

Check the backend logs:

```bash
docker compose -f docker/docker-compose.yml logs backend
```

Check the container status:

```bash
docker compose -f docker/docker-compose.yml ps
```

---

## Frontend cannot connect to backend

Verify the backend URL:

```env
BACKEND_URL=http://backend:8000
```

When using Docker Compose, the frontend should communicate with the backend using the Docker service name:

```text
backend
```

rather than `localhost`.

---

## Containers are unhealthy

Check service logs:

```bash
docker compose -f docker/docker-compose.yml logs
```

Then inspect the individual service:

```bash
docker compose -f docker/docker-compose.yml logs backend
```

or:

```bash
docker compose -f docker/docker-compose.yml logs frontend
```

---

# Production Considerations

For a production deployment, consider:

* HTTPS/TLS configuration
* Secure secret management
* Restricted network access
* Database backups
* Persistent storage backups
* Monitoring and logging
* Authentication and authorization
* Rate limiting
* Resource limits
* Container image scanning
* Regular dependency updates

The included Docker configuration provides the foundation for containerized deployment but should be reviewed and hardened according to the target production environment.

---

# License

Add the appropriate license for the project here.

For example:

```text
This project is proprietary unless otherwise specified by the repository owner.
```

---

# Author

**Asim Imam**

GitHub:

https://github.com/Asim-imam-ai

---

## Status

This project is under active development.

The repository contains the application source code, testing infrastructure, Docker configuration, and development tooling required to run and extend AgentFlow Chat.
