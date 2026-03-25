# KG Arena

KG Arena is a web-based academic prototype for side-by-side relation extraction and knowledge graph comparison across **LUKE**, **REBEL**, and **KnowGL** adapter paths.

## What it does

Given input text, KG Arena:
- runs three extractor adapters on the same text,
- normalizes outputs into a shared triple schema,
- renders three interactive knowledge graphs,
- computes per-model metrics,
- shows overlap/diff groups,
- and supports provenance inspection from edge selection.

## Stack overview

- **Frontend**: React + Vite + TypeScript + Cytoscape.js
- **Backend**: FastAPI + Python + Hugging Face Transformers (where feasible)
- **Infra**: Docker Compose

## Monorepo structure

- `frontend/`
- `backend/`
  - `backend/models/` model adapters
  - `backend/services/` parsing, normalization, evaluation
  - `backend/examples/` example texts + provisional ground truth
- `docker-compose.yml`
- `README.md`

## Local setup (without Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Docker usage

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API docs: http://localhost:8000/docs


### Model caching and cold-start behavior

KG Arena now configures a shared Hugging Face cache directory (`HF_HOME`) and suppresses noisy symlink warnings.

For Docker builds, backend image creation pre-downloads LUKE + REBEL weights, so the first API extraction request does not spend extra time downloading multi-GB model files.

If you run on Windows outside Docker, you can further improve caching performance by enabling **Developer Mode** (symlink support) or running Python with administrator rights.

You can also prefetch models manually:

```bash
cd backend
python -m app.preload_models
```

## Example library

Examples are stored in `backend/examples/library.json`.

### Add a new example

1. Append a new object with `id`, `title`, `description`, `text`, and `ground_truth`.
2. Keep `ground_truth` in the same triple schema used by the API.

## How to add a new model adapter

1. Create a class in `backend/models/` that extends `BaseExtractor`.
2. Implement `extract(text: str) -> list[Triple]`.
3. Normalize all outputs into the shared `Triple` schema.
4. Register the adapter in `app/main.py` startup.

## API endpoints

- `GET /health`
- `GET /examples`
- `GET /examples/{id}`
- `POST /parse` (supports `.txt`, `.pdf`, `.docx`)
- `POST /extract`
- `POST /evaluate`

## Known limitations

- **KnowGL adapter currently uses a deterministic heuristic fallback**, pending a stable local inference wrapper.
- LUKE path currently uses LUKE NER + co-occurrence relation heuristic (not full LUKE relation-classification pipeline).
- REBEL model loading can be heavy on cold start.
- Provenance span mapping is heuristic sentence matching when exact spans are unavailable.
- No persistent storage (intended for v1).

## Suggested future improvements

- Replace KnowGL fallback with a true model integration.
- Improve LUKE relation extraction with entity-pair classification and candidate generation.
- Add batching/caching for long documents.
- Improve graph scalability controls for dense outputs.
- Add richer metric visualizations and filtering in diff panel.

## Testing

Backend unit tests:

```bash
cd backend
pytest
```

## Future deployment options

- Split deployment:
  - Frontend on **Vercel**
  - Backend on **Render**
- Unified deployment:
  - Single Docker image/compose-derived deployment (e.g., Hugging Face Spaces or VM)
