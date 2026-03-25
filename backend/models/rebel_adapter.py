from __future__ import annotations

import re
from itertools import count
from typing import Any

from transformers import pipeline

from app.schemas import Triple
from models.base import BaseExtractor
from services.heuristic_extraction import heuristic_triples
from services.model_loading import REBEL_MODEL_ID
from services.provenance import best_sentence_span


def parse_rebel_output(generated: str) -> list[tuple[str, str, str]]:
    triplets: list[tuple[str, str, str]] = []
    current_subject = ''
    current_relation = ''
    current_object = ''
    state = None

    tokens = generated.replace('<s>', '').replace('</s>', '').split()
    for token in tokens:
        if token == '<triplet>':
            if current_subject and current_relation and current_object:
                triplets.append((current_subject.strip(), current_relation.strip(), current_object.strip()))
            current_subject, current_relation, current_object = '', '', ''
            state = 'subject'
        elif token == '<subj>':
            state = 'object'
        elif token == '<obj>':
            state = 'relation'
        else:
            if state == 'subject':
                current_subject += f' {token}'
            elif state == 'object':
                current_object += f' {token}'
            elif state == 'relation':
                current_relation += f' {token}'

    if current_subject and current_relation and current_object:
        triplets.append((current_subject.strip(), current_relation.strip(), current_object.strip()))

    cleaned: list[tuple[str, str, str]] = []
    for subj, rel, obj in triplets:
        subj = re.sub(r'\s+', ' ', subj).strip()
        rel = re.sub(r'\s+', ' ', rel).strip()
        obj = re.sub(r'\s+', ' ', obj).strip()
        if subj and rel and obj:
            cleaned.append((subj, rel, obj))
    return cleaned


class RebelAdapter(BaseExtractor):
    model_name = 'REBEL'

    def __init__(self) -> None:
        self._generator: Any | None = None
        self._load_error: str | None = None
        try:
            self._generator = pipeline(
                'text2text-generation',
                model=REBEL_MODEL_ID,
                tokenizer=REBEL_MODEL_ID,
            )
        except Exception as exc:  # pragma: no cover - depends on runtime env
            self._load_error = str(exc)

    def extract(self, text: str) -> list[Triple]:
        if not self._generator:
            return heuristic_triples(text, self.model_name)

        generated = self._generator(text, max_length=256, truncation=True)[0]['generated_text']
        parsed = parse_rebel_output(generated)
        if not parsed:
            return heuristic_triples(text, self.model_name)

        triples: list[Triple] = []
        id_counter = count(1)
        for subject, relation, obj in parsed:
            sentence, start, end = best_sentence_span(text, subject, obj)
            triples.append(
                Triple(
                    id=f'rebel-{next(id_counter)}',
                    subject=subject,
                    relation=relation,
                    object=obj,
                    provenance_sentence=sentence,
                    provenance_char_start=start,
                    provenance_char_end=end,
                    confidence=0.75,
                    model_name=self.model_name,
                    raw_metadata={'generator': REBEL_MODEL_ID},
                )
            )
        return triples
