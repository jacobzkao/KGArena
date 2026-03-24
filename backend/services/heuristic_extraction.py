from __future__ import annotations

import re
from itertools import count

from app.schemas import Triple
from services.provenance import best_sentence_span

ENTITY_PATTERN = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b")
VERB_PATTERN = re.compile(r"\b(is|was|are|were|founded|born|located|works|led|acquired|developed|studied)\b", re.IGNORECASE)


def heuristic_triples(text: str, model_name: str, limit: int = 25) -> list[Triple]:
    entities = list(dict.fromkeys(match.group(1) for match in ENTITY_PATTERN.finditer(text)))
    triples: list[Triple] = []
    id_counter = count(1)

    for idx, subj in enumerate(entities):
        for obj in entities[idx + 1:]:
            sentence, start, end = best_sentence_span(text, subj, obj)
            verb_match = VERB_PATTERN.search(sentence)
            relation = verb_match.group(1).lower() if verb_match else 'related_to'
            triples.append(
                Triple(
                    id=f"{model_name.lower()}-{next(id_counter)}",
                    subject=subj,
                    relation=relation,
                    object=obj,
                    provenance_sentence=sentence,
                    provenance_char_start=start,
                    provenance_char_end=end,
                    confidence=0.35,
                    model_name=model_name,
                    raw_metadata={"source": "heuristic_fallback"},
                )
            )
            if len(triples) >= limit:
                return triples
    return triples
