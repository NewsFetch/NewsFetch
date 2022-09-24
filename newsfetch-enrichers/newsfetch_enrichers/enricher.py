from abc import ABC
from typing import Any


class Enricher(ABC):
    def enrich(self, text: str) -> Any:
        raise NotImplementedError