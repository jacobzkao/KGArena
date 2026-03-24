from __future__ import annotations

from app.schemas import Triple
from models.base import BaseExtractor
from services.heuristic_extraction import heuristic_triples


class KnowGLAdapter(BaseExtractor):
    """Temporary adapter.

    A direct, production-ready local Hugging Face KnowGL extraction pipeline is not
    currently available in this prototype. The adapter preserves the same contract
    and uses a deterministic heuristic extraction fallback so the system remains
    end-to-end runnable.
    """

    model_name = 'KnowGL'

    def extract(self, text: str) -> list[Triple]:
        triples = heuristic_triples(text, self.model_name)
        for triple in triples:
            triple.raw_metadata['note'] = 'temporary_heuristic_fallback'
        return triples
