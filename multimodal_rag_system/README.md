=======
Ingestion
=======
Multimodal RAG
====
2 ways to implement multimodal RAG ingestion layer

1. using Cloud Solutions (ex: LlamaIndex)
2. Custom ingestion layer (ex: using Docling)

====

```
multimodal-rag-system1/
├── main.py                        ← FastAPI app entry point
├── schema.sql                     ← Database schema (run once to set up DB)
├── pyproject.toml                 ← Dependencies
├── .env.example                   ← Template — copy to .env
├── .env                           ← Your actual secrets (never commit this)
├── data/
│   ├── *.pdf                      ← Source PDFs to ingest
│   └── images/                    ← Extracted images saved here during ingesion
├── references/
│   └── multimodal-rag-implementation-guide.md  ← This file
└── src/
    ├── core/
    │   └── db.py                  ← DB connection, embeddings, store/search
    ├── ingestion/
    │   ├── docling_parser.py      ← PDF → structured chunks
    │   └── ingestion.py           ← Orchestrates parse → embed → store
    └── api/
        └── v1/
            ├── routes/
            │   └── query.py       ← POST /api/v1/query endpoint
            ├── schemas/
            │   └── query_schema.py ← Pydantic request/response models
            └── services/
                └── query_service.py ← RAG logic: retrieve + build prompt + call LLM

```

===
