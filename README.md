# Astro Reading

Personal tool that generates astrology readings (natal chart, solar return and transits) and delivers them to the user as a downloadable file.

## Input

- Birth date, time and country
- Place where the solar return takes place

## Output

A file (Markdown or PDF) with the natal chart reading, the solar return reading and the transits report.

## Privacy

- No user data is stored in any database.
- Inputs exist only for the duration of the request and are not logged.
- The vector database holds only the astrology knowledge base, never user data.

## Architecture

```
user input ──> n8n workflow ──> Python calculation (ephemeris)
                    │                    │
                    │                    └─> planetary positions, aspects
                    └─> Qdrant (RAG over astrology knowledge base)
                    └─> LLM drafts the reading ──> output file
```

| Part | Tool |
|------|------|
| Orchestration | n8n |
| Chart calculations | Python (ephemeris library) |
| Knowledge base | Qdrant (local, Docker) |
| Output | Markdown / PDF |

## Structure

```
src/astro/        Chart calculations and file generation
scripts/          Knowledge base ingestion (PDF -> Qdrant)
workflows/        Exported n8n workflows (JSON)
data/knowledge/   Source PDFs for the RAG (not committed)
output/           Generated readings (not committed)
```

## Run locally

```bash
cp .env.example .env
docker compose up -d
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/ingest_pdfs.py
```

- n8n: http://localhost:5678
- Qdrant: http://localhost:6333/dashboard

## Knowledge base

The PDFs used by the RAG go in `data/knowledge/`. They are excluded from git (see `.gitignore`).

## Status

Early skeleton. Work in progress.

## License

To be decided. Note that some ephemeris libraries (e.g. Swiss Ephemeris, Kerykeion) are AGPL or dual-licensed, which affects the license of this project.
# astro-reading
