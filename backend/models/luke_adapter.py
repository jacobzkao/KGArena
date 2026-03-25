from __future__ import annotations

from itertools import count
from typing import Any

from transformers import pipeline

from app.schemas import Triple
from models.base import BaseExtractor
from services.heuristic_extraction import heuristic_triples
from services.model_loading import LUKE_MODEL_ID
from services.provenance import best_sentence_span


class LukeAdapter(BaseExtractor):
    model_name = 'LUKE'

    def __init__(self) -> None:
        self._ner: Any | None = None
        self._load_error: str | None = None
        try:
            self._ner = pipeline(
                'token-classification',
                model=LUKE_MODEL_ID,
                aggregation_strategy='simple',
            )
        except Exception as exc:  # pragma: no cover - environment-dependent
            self._load_error = str(exc)

    def extract(self, text: str) -> list[Triple]:
        if not self._ner:
            return heuristic_triples(text, self.model_name)

        entities = []
        for ent in self._ner(text):
            word = ent.get('word', '').strip()
            if word and word not in entities:
                entities.append(word)

        if len(entities) < 2:
            return heuristic_triples(text, self.model_name)

        triples: list[Triple] = []
        id_counter = count(1)
        for index, subject in enumerate(entities[:-1]):
            obj = entities[index + 1]
            sentence, start, end = best_sentence_span(text, subject, obj)
            triples.append(
                Triple(
                    id=f'luke-{next(id_counter)}',
                    subject=subject,
                    relation='mentions_with',
                    object=obj,
                    provenance_sentence=sentence,
                    provenance_char_start=start,
                    provenance_char_end=end,
                    confidence=0.55,
                    model_name=self.model_name,
                    raw_metadata={'pipeline': 'luke-ner-cooccurrence'},
                )
            )
        return triples
