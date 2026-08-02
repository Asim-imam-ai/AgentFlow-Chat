# AgentFlow Chat - Autonomous AI Dashboard

AgentFlow Chat is a high-performance backend server and responsive HTML frontend dashboard orchestrating multi-agent state machines using LangGraph, FastAPI, and SQLAlchemy.

## 🚀 Features
- **LangGraph Workflows**: Dynamically loop tool actions, evaluate system decisions, and manage contexts.
- **Persistent Databases**: Multi-layer state checkpointer persistent using SQLite and SQLAlchemy ORM models.
- **RAG Parser**: Chunk, parse, and similarity index documents (.txt, .md, .csv, .pdf) locally.
- **Multi-LLM Support**: Supports OpenAI GPT models and Google Gemini API out-of-the-box.
- **Stream SSE Responses**: Stream events and status outputs.
- **Modern Dashboard UI**: A fully interactive HTML5 template with Outfit typography and glassmorphic aesthetics.

## 📁 Directory Structure
```
AgentFlow_Chat/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   ├── upload.py
│   │   │   ├── conversation.py
│   │   │   ├── history.py
│   │   │   ├── health.py
│   │   │   └── thread.py
│   │   ├── schemas/
│   │   │   ├── chat.py
│   │   │   ├── upload.py
│   │   │   ├── conversation.py
│   │   │   ├── history.py
│   │   │   └── response.py
│   │   ├── router.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── settings.py
│   │   ├── constants.py
│   │   ├── prompts.py
│   │   ├── logging.py
│   │   ├── security.py
│   │   └── events.py
│   ├── database/
│   │   ├── session.py
│   │   └── models.py
│   ├── graph/
│   │   ├── nodes/
│   │   │   ├── chatbot.py
│   │   │   ├── tools.py
│   │   │   ├── planner.py
│   │   │   ├── memory.py
│   │   │   ├── rag.py
│   │   │   └── summarizer.py
│   │   ├── builder.py
│   │   ├── checkpoint.py
│   │   └── factory.py
│   ├── llms/
│   │   ├── gemini.py
│   │   └── models.py
│   ├── repositories/
│   │   ├── conversation_repository.py
│   │   ├── chat_repository.py
│   │   └── memory_repository.py
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── conversation_service.py
│   │   ├── upload_service.py
│   │   ├── stream_service.py
│   │   ├── rag_service.py
│   │   ├── memory_service.py
│   │   └── agent_service.py
│   ├── streaming/
│   │   ├── chunk_filter.py
│   │   └── response_builder.py
│   ├── tools/
│   │   ├── calculator.py
│   │   ├── memory.py
│   │   ├── rag.py
│   │   ├── search.py
│   │   └── registry.py
│   ├── thread.py
│   └── main.py
├── data/
│   ├── chatbot_memory.db
│   ├── langgraph_checkpoints.sqlite
│   └── chroma_db/
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── utils/
│   ├── file_utils.py
│   ├── validators.py
│   ├── model_utils.py
│   └── helpers.py
├── exceptions/
│   ├── handlers.py
│   └── custom.py
├── tests/
├── scripts/
├── docker/
├── docs/
├── main.py
└── pyproject.toml
```

## 🛠️ Getting Started
Please consult the [docs/deployment.md](docs/deployment.md) guide for details on installation and running locally or via Docker.
