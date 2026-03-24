from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas import Triple


class BaseExtractor(ABC):
    model_name: str

    @abstractmethod
    def extract(self, text: str) -> list[Triple]:
        raise NotImplementedError
