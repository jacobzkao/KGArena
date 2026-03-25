from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    EvaluationRequest,
    EvaluationResponse,
    ExtractRequest,
    ExtractResponse,
    ModelOutput,
    ParseResponse,
)
from models.knowgl_adapter import KnowGLAdapter
from models.luke_adapter import LukeAdapter
from models.rebel_adapter import RebelAdapter
from services.evaluation import compute_diff, compute_metrics
from services.examples import get_example, list_examples
from services.model_loading import configure_huggingface_environment
from services.parsing import UnsupportedFileTypeError, parse_uploaded_file

app = FastAPI(title='KG Arena API', version='0.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
def startup_event() -> None:
    configure_huggingface_environment()
    app.state.adapters = [LukeAdapter(), RebelAdapter(), KnowGLAdapter()]


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}


@app.get('/examples')
def get_examples():
    return list_examples()


@app.get('/examples/{example_id}')
def get_example_detail(example_id: str):
    try:
        return get_example(example_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail='Example not found') from exc


@app.post('/parse', response_model=ParseResponse)
async def parse(file: UploadFile = File(...)) -> ParseResponse:
    content = await file.read()
    try:
        text = parse_uploaded_file(file.filename or '', content)
    except UnsupportedFileTypeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ParseResponse(text=text)


@app.post('/extract', response_model=ExtractResponse)
def extract(request: ExtractRequest) -> ExtractResponse:
    if not request.text.strip():
        raise HTTPException(status_code=400, detail='Input text is empty')

    outputs: list[ModelOutput] = []
    warnings: list[str] = []
    for adapter in app.state.adapters:
        try:
            triples = adapter.extract(request.text)
            outputs.append(ModelOutput(model_name=adapter.model_name, triples=triples))
        except Exception as exc:  # pragma: no cover - runtime failure path
            message = f'{adapter.model_name} failed: {exc}'
            warnings.append(message)
            outputs.append(ModelOutput(model_name=adapter.model_name, triples=[], warning=message))

    return ExtractResponse(text=request.text, outputs=outputs, warnings=warnings)


@app.post('/evaluate', response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest) -> EvaluationResponse:
    metrics = compute_metrics(request.outputs, request.ground_truth)
    diff = compute_diff(request.outputs, request.ground_truth)
    return EvaluationResponse(metrics_by_model=metrics, diff=diff)
