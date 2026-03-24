from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Triple(BaseModel):
    id: str
    subject: str
    relation: str
    object: str
    provenance_sentence: str
    provenance_char_start: int
    provenance_char_end: int
    confidence: float | None = None
    model_name: str
    raw_metadata: dict[str, Any] = Field(default_factory=dict)


class ModelOutput(BaseModel):
    model_name: str
    triples: list[Triple]
    warning: str | None = None


class ExtractRequest(BaseModel):
    text: str
    ground_truth: list[Triple] | None = None


class ParseResponse(BaseModel):
    text: str


class ExtractResponse(BaseModel):
    text: str
    outputs: list[ModelOutput]
    warnings: list[str] = Field(default_factory=list)


class Metrics(BaseModel):
    triple_count: int
    unique_entities: int
    unique_relations: int
    overlap_count: int
    precision: float | None = None
    recall: float | None = None
    f1: float | None = None
    exact_match_rate: float | None = None
    relaxed_match_rate: float | None = None
    hallucination_proxy: float | None = None


class DiffGroup(BaseModel):
    label: str
    triples: list[Triple]


class EvaluationRequest(BaseModel):
    outputs: list[ModelOutput]
    ground_truth: list[Triple] | None = None


class EvaluationResponse(BaseModel):
    metrics_by_model: dict[str, Metrics]
    diff: list[DiffGroup]


class ExampleRecord(BaseModel):
    id: str
    title: str
    description: str


class ExampleDetail(BaseModel):
    id: str
    title: str
    description: str
    text: str
    ground_truth: list[Triple]
