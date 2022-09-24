from newsfetch_enrichers.enricher import Enricher


class HuggingFaceEnricher(Enricher):
    def __init__(self, model_name: str):
        self.model_name = model_name
