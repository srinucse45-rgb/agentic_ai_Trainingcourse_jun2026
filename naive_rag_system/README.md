# Naive RAG System

A simple Retrieval-Augmented Generation (RAG) setup over an HR support-desk
knowledge base, using pgvector for storage and OpenAI for embeddings.

## Vector DB

- **Engine:** Pgvector
- **Database name:** `hr_rag_db`
- **Credentials:**
  - username: `postgres`
  - password: `Pass@123`

## File to Ingest

```
data/HR_Support_Desk_KnowledgeBase.pdf
```

## Chunking Strategy

| Setting           | Value                        |
| ----------------- | ---------------------------- |
| Chunk size        | 1000 characters (up to 1000) |
| Chunk overlap     | 200 characters (up to 200)   |
| Vector dimensions | default (1536)               |

## Embedding Model

- **Model:** `text-embedding-3-small` (OpenAI)
- **OpenAI API key:** stored in `.env`

## Environment Setup

```bash
python -m venv .venv
.venv\Scripts\activate.bat   # Windows

uv add python-dotenv
```

## Missed

1. FastAPI endpoints
2. `create_agent` of LangChain

## Vectorization Notes

Vectorization is **not** recommended directly for the following file types:

```
.xls, .xlsx, .csv, .json, .html
```

For the above files, preprocessing is required — either enrich the file
content into plain text, or clean up the noise before ingesting.

## Index your DB

CREATE INDEX ON
langchain_pg_embedding
USING ivfflat
((embedding::vector(1536)) vector_cosine_ops) WITH (lists = 100);
