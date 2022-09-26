import logging

import config
from newsfetch_enrichers.spacy_ner_enricher import SpacyNerEnricher
from newsfetch_enrichers.transformers_ner_enricher import TransformersNerEnricher
from newsfetch_enrichers.transformers_summarization_enricher import TransformersSummarizationEnricher
from newsfetch_enrichers.transformers_zeroshot_classification_enricher import TransformersZeroShotClassificationEnricher


class EnricherModelFactory():
    def __init__(self):
        self.enricher_models = {}

    def get_enricher(self, model_source, model_name, category):
        enricher_clazz = None
        enricher_model_key = model_source + model_name + category
        if enricher_model_key in self.enricher_models.keys():
            enricher_clazz = self.enricher_models[enricher_model_key]
        else:
            if model_source == config.SPACY and category == config.NER:
                enricher_clazz = SpacyNerEnricher(model_name)
            elif model_source == config.TRANSFORMERS and category == config.NER:
                enricher_clazz = TransformersNerEnricher(model_name)
            elif model_source == config.TRANSFORMERS and category == config.ZERO_SHOT_CLASSIFICATION:
                enricher_clazz = TransformersZeroShotClassificationEnricher(
                    model_name,
                    config.NEWS_HIGH_LEVEL_CATEGORIES)
            elif model_source == config.TRANSFORMERS and category == config.SUMMARIZATION:
                enricher_clazz = TransformersSummarizationEnricher(model_name)

            if enricher_clazz:
                self.enricher_models[enricher_model_key] = enricher_clazz
            else:
                logging.warn(f"Enricher not found for model_source: {model_source}, model_name: {model_name}, category: {category}")

        return enricher_clazz