# AGENTS.md — KG Arena

## Project Overview
KG Arena is a web-based academic demo that compares knowledge graph extraction models side by side.

Given a text input, the system runs:
- LUKE
- REBEL
- KnowGL

It then produces:
- Three interactive knowledge graphs (one per model)
- A metrics panel comparing outputs
- A diff/overlap view across models
- A source text viewer with provenance highlighting

This project is part of a capstone focused on evaluating relation extraction pipelines and knowledge graph quality.

---

## Core Principles

### 1. Clarity over cleverness
- Prefer readable, modular code
- Avoid unnecessary abstraction
- Optimize for long-term research extensibility

### 2. End-to-end functionality first
- Always prioritize a working vertical slice
- Avoid leaving partially connected systems

### 3. Consistent data contracts
- All models must output normalized triples
- Frontend should never depend on raw model output formats

### 4. Temporary processing only
- Do not persist uploaded user data
- No database required for v1

### 5. Clean academic demo
- UI should be simple, structured, and informative
- Avoid flashy or startup-style design

---

## Tech Stack

### Frontend
- React
- Vite
- TypeScript
- Cytoscape.js (for graph visualization)

### Backend
- Python
- FastAPI
- Hugging Face Transformers

### Infrastructure
- Docker Compose (local development)
- No auth
- No persistent storage

---

## Repository Structure
/frontend
/backend
/backend/models # model adapters
/backend/services # parsing, normalization, evaluation
/backend/examples # example texts + ground truth
/docker-compose.yml
/README.md


---

## Coding Workflow for Agents

### Always follow this sequence:
1. Inspect repository
2. Summarize current state
3. Propose implementation plan
4. State assumptions
5. Implement in phases
6. Keep app runnable after each phase
7. Provide final summary

Do not stop after planning.

---

## Model Integration Requirements

Each model must be implemented as an adapter with a shared interface: 

extract(text: str) -> List[Triple]


Where Triple is normalized to:

- id
- subject
- relation
- object
- provenance_sentence
- provenance_char_start
- provenance_char_end
- confidence (optional)
- model_name
- raw_metadata

### Important:
- Do not expose raw model outputs directly to frontend
- Normalize everything before returning

---

## Input Requirements

Users must be able to:
- Paste text
- Upload:
  - .txt
  - .pdf
  - .docx
- Select from example library
- Optionally upload ground truth triples

---

## Graph Requirements

Each model output must be rendered as an interactive graph with:

- Pan and zoom
- Node and edge selection
- Highlighting
- Triple detail display

### Edge interaction:
When an edge is selected:
- Show triple details
- Show provenance sentence
- Highlight relevant text in source viewer

---

## Metrics Requirements

When ground truth is available, compute:

- Precision
- Recall
- F1
- Exact match rate
- Relaxed match rate
- Hallucination proxy

Always compute:
- Triple count
- Unique entities
- Unique relations
- Overlap counts

---

## Diff / Overlap Logic

Must support:

- Triples common to all models
- Triples unique to each model
- Pairwise overlaps
- Differences vs ground truth (if available)

Return structured data for frontend table display.

---

## Normalization Rules

Implement a normalization pipeline that:
- Trims whitespace
- Optionally lowercases
- Removes trivial punctuation
- Supports:
  - exact matching
  - relaxed matching

Preserve original text for UI.

---

## Backend API Guidelines

Suggested endpoints:

- GET /health
- GET /examples
- GET /examples/{id}
- POST /parse
- POST /extract
- POST /evaluate

### Key requirement:
Model loading must happen once at startup, not per request.

---

## Frontend UI Layout

- Header: KG Arena
- Left panel: input controls
- Center: 3 graph views side-by-side
- Bottom: metrics + diff panels
- Right: source text + selected triple details

---

## Performance Guidelines

- Avoid reloading models per request
- Handle partial failures gracefully
- Return partial results if one model fails
- Keep graphs readable (limit excessive node explosion)

---

## Error Handling

- Unsupported file types → clear error
- Model failure → return available outputs + warning
- Empty input → block execution with message

---

## Documentation Requirements

README must include:
- What KG Arena does
- Tech stack
- Setup instructions
- Docker usage
- How to add:
  - new models
  - new example texts
- Known limitations
- Future work

---

## Testing Expectations

At minimum:
- Test normalization functions
- Test evaluation logic
- Verify one full pipeline run works end-to-end

---

## Deployment Guidance

Design for future deployment:
- Frontend → Vercel
- Backend → Render

OR

- Single Docker deployment (e.g., Hugging Face Spaces)

---

## Known Challenges

Agents should anticipate:

- Different output formats across LUKE, REBEL, KnowGL
- Missing provenance spans → requires heuristic mapping
- Heavy model loading times
- Graph visualization scaling issues
- Inconsistent entity naming → requires normalization

---

## Non-Goals (for now)

- Authentication
- Persistent storage
- User accounts
- Large-scale production optimization
- Perfect evaluation metrics

---

## Definition of Done

The app is complete when:

- It runs locally via Docker
- User can input or select text
- All 3 models produce outputs
- Graphs render side-by-side
- User can inspect triples and provenance
- Metrics and diff views work
- Codebase is clean and extensible

---

## Agent Behavior Expectations

- Be proactive
- Do not block on small uncertainties
- Make reasonable assumptions and document them
- Prefer working systems over partial implementations
- Keep code clean and modular
- Think like a researcher building a tool, not a startup building a product

---

## Final Note

KG Arena is both:
- a research tool
- a visualization interface

Every design decision should support:
**understanding how model choices affect knowledge graph structure and quality**
