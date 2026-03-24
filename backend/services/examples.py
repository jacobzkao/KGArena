from __future__ import annotations

import json
from pathlib import Path

from app.schemas import ExampleDetail, ExampleRecord

EXAMPLES_PATH = Path(__file__).resolve().parent.parent / 'examples' / 'library.json'


def load_examples() -> list[ExampleDetail]:
    data = json.loads(EXAMPLES_PATH.read_text(encoding='utf-8'))
    return [ExampleDetail.model_validate(item) for item in data]


def list_examples() -> list[ExampleRecord]:
    return [ExampleRecord(id=e.id, title=e.title, description=e.description) for e in load_examples()]


def get_example(example_id: str) -> ExampleDetail:
    for example in load_examples():
        if example.id == example_id:
            return example
    raise KeyError(example_id)
