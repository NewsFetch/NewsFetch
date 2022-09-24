import datetime
import uuid
from typing import Dict, List

import config
from common.datatypes import EntityAggregate, Entity, NERAggregate


def build_entity_key(entity):
    entity_key = entity.entity.lower() + entity.label
    return entity_key


class SingleModelNamedEntitiesAggregator():
    def __init__(self, composer_strategy = None):
        self.named_entities = []
        self.composer_strategy = composer_strategy

    def add(self, entity):
        self.named_entities.append(entity)

    def has_entities(self):
        return len(self.named_entities) > 0

    def aggregate(self):
        composed_named_entities = None
        entities_to_aggregate = self.named_entities
        if self.composer_strategy:
            composed_named_entities = self.composer_strategy.compose(self.named_entities)
            entities_to_aggregate = composed_named_entities

        entity_aggregates: Dict[str, EntityAggregate] = {}
        entity_interim_confidence_totals: Dict[str, float] = {}
        for entity in entities_to_aggregate:
            entity_key = build_entity_key(entity)
            if not entity_key in entity_aggregates:
                entity_aggregate = EntityAggregate(entity=entity.entity, label=entity.label)
                entity_aggregates.setdefault(entity_key, entity_aggregate)
                entity_interim_confidence_totals.setdefault(entity_key, 0.0)
            entity_aggregate = entity_aggregates[entity_key]
            entity_aggregate.count = entity_aggregate.count + 1
            entity_interim_confidence_totals[entity_key] = entity_interim_confidence_totals[entity_key] + entity.confidence

        for aggregate in entity_aggregates.values():
            entity_key = build_entity_key(aggregate)
            aggregate.confidence = entity_interim_confidence_totals[entity_key] / aggregate.count

        return composed_named_entities, entity_aggregates


class MultiModelNamedEntitiesAggregator():

    def aggregate(self, enrichments: List[dict]):

        for i in range(1, len(enrichments)):
            if enrichments[0]['dataset'] != enrichments[i]['dataset'] or \
                    enrichments[0]['dataset_id'] != enrichments[i]['dataset_id'] or \
                    enrichments[0]['detected_language'] != enrichments[i]['detected_language'] or \
                    enrichments[0]['title'] != enrichments[i]['title'] or \
                    enrichments[0]['uri'] != enrichments[i]['uri'] or \
                    enrichments[0]['category'] != enrichments[i]['category'] != config.NER:
                print("cannot aggregate enrichments as they aren't similar datasets...")
                print("check dataset, dataset_id, detected_language, title, uri and category are same!")
                return None

        aggregate_payload = {}
        aggregate_payload.update({
            "id": str(uuid.uuid4()),
            "enriched_by": config.NEWSFETCH,
            "enrichment_version": "1.0",
            "enriched_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "enrichment_type": config.ENRICHMENT_TYPE_INSIGHT,
            "category": config.NER_AGGREGATED,
            "dataset": enrichments[0]['dataset'],
            "dataset_id": enrichments[0]['dataset_id'],
            "detected_language": enrichments[0]['detected_language'],
            "title": enrichments[0]['title'],
            "uri": enrichments[0]['uri'],
            "model_source": config.NEWSFETCH,
            "insight_name": "multimodel-named-entities-aggregator"
        })

        model_details = []

        entity_aggregates: Dict[str, EntityAggregate] = {}
        entity_interim_confidence_totals: Dict[str, float] = {}

        for enrichment in enrichments:
            model_detail = {}
            model_detail['model_name'] = enrichment['model_name']
            model_detail['model_source'] = enrichment['model_source']
            model_detail['enrichment_id'] = enrichment['id']
            model_detail['enrichment_type'] = enrichment['enrichment_type']
            model_detail['enriched_by'] = enrichment['enriched_by']
            model_detail['enrichment_version'] = enrichment['enrichment_version']
            model_detail['enriched_date'] = enrichment['enriched_date']
            model_detail['category'] = enrichment['category']
            model_details.append(model_detail)

            entity_aggregates_from_enrichment_json = enrichment["entity_aggregates"]
            for entity_aggregate_from_enrichment_json in entity_aggregates_from_enrichment_json:
                entity_aggregate_from_enrichment = EntityAggregate.parse_obj(entity_aggregate_from_enrichment_json)
                entity_key = build_entity_key(entity_aggregate_from_enrichment)
                if not entity_key in entity_aggregates:
                    entity_aggregate = EntityAggregate(entity=entity_aggregate_from_enrichment.entity,
                                                       label=entity_aggregate_from_enrichment.label)
                    entity_aggregates.setdefault(entity_key, entity_aggregate)
                    entity_interim_confidence_totals.setdefault(entity_key, 0.0)
                entity_aggregate = entity_aggregates[entity_key]
                entity_aggregate.count = entity_aggregate.count + entity_aggregate_from_enrichment.count
                entity_interim_confidence_totals[entity_key] = entity_interim_confidence_totals[entity_key] +\
                                                               entity_aggregate_from_enrichment.confidence * entity_aggregate_from_enrichment.count

        for aggregate in entity_aggregates.values():
            entity_key = build_entity_key(aggregate)
            aggregate.confidence = entity_interim_confidence_totals[entity_key] / aggregate.count

        aggregate_payload.update({'aggregation_details': model_details})
        ner_aggregate = NERAggregate(entity_aggregates=list(entity_aggregates.values()))
        aggregate_payload.update(ner_aggregate.dict())
        return aggregate_payload


if __name__ == '__main__':
    single_model_aggregator = SingleModelNamedEntitiesAggregator()
    entities = [
        {'confidence': 0.95,
         'description': None,
         'end_offset': 72,
         'entity': 'Thursday , 13 January 2022',
         'label': 'DATE',
         'pos_tag': None,
         'start_offset': 47},
        {'confidence': 0.9,
         'description': None,
         'end_offset': 97,
         'entity': 'Glenn Beck',
         'label': 'PERSON',
         'pos_tag': None,
         'start_offset': 87},
        {'confidence': 0.8,
         'description': None,
         'end_offset': 182,
         'entity': 'Glenn Beck',
         'label': 'PERSON',
         'pos_tag': None,
         'start_offset': 172},
        {'confidence': 0.7,
         'description': None,
         'end_offset': 470,
         'entity': 'GLENN BECK',
         'label': 'PERSON',
         'pos_tag': None,
         'start_offset': 460}
    ]
    for entity in entities:
        single_model_aggregator.add(Entity.parse_obj(entity))

    print(single_model_aggregator.aggregate())

    multi_model_aggregator = MultiModelNamedEntitiesAggregator()
    enrichment1 = {
        "category": "ner",
        "dataset": "news-cc",
        "id": "c25dbc0b-be6b-401a-823a-de827ecda50a",
        "dataset_id": "c25dbc0b-be6b-401a-823a-de827ecda50e",
        "detected_language": "en",
        "title": "A tale of two cities",
        "uri": "https://google.com",
        "enriched_date": "2022-02-12T21:06:05Z",
        "enriched_by": "shukra.ai",
        "enrichment_version": "1.0",
        "enrichment_type": config.ENRICHMENT_TYPE_INFERENCE,
        "model_name": "one",
        "model_source": "one_src",
        "entity_aggregates": [
            {
                "confidence": 0.9,
                "count": 1,
                "entity": "Today",
                "label": "DATE"
            },
            {
                "confidence": 0.8,
                "count": 2,
                "entity": "Glenn Beck",
                "label": "PERSON"
            }
        ]
    }
    enrichment2 = {
        "category": "ner",
        "dataset": "news-cc",
        "id": "c25dbc0b-be6b-401a-823a-de827ecda50b",
        "dataset_id": "c25dbc0b-be6b-401a-823a-de827ecda50e",
        "detected_language": "en",
        "title": "A tale of two cities",
        "uri": "https://google.com",
        "enriched_date": "2022-02-12T21:06:05Z",
        "enriched_by": "shukra.ai",
        "enrichment_version": "1.0",
        "enrichment_type": config.ENRICHMENT_TYPE_INFERENCE,
        "model_name": "two",
        "model_source": "two_src",
        "entity_aggregates": [
            {
                "confidence": 0.8,
                "count": 2,
                "entity": "Today",
                "label": "DATE"
            },
            {
                "confidence": 0.7,
                "count": 3,
                "entity": "GLENN BECK",
                "label": "PERSON"
            }
        ]
    }
    enrichment3 = {
        "category": "ner",
        "dataset": "news-cc",
        "id": "c25dbc0b-be6b-401a-823a-de827ecda50c",
        "dataset_id": "c25dbc0b-be6b-401a-823a-de827ecda50e",
        "detected_language": "en",
        "title": "A tale of two cities",
        "uri": "https://google.com",
        "enriched_date": "2022-02-12T21:06:05Z",
        "enriched_by": "shukra.ai",
        "enrichment_version": "1.0",
        "enrichment_type": config.ENRICHMENT_TYPE_INFERENCE,
        "model_name": "three",
        "model_source": "three_src",
        "entity_aggregates": [
            {
                "confidence": 0.7,
                "count": 3,
                "entity": "Today",
                "label": "DATE"
            },
            {
                "confidence": 0.6,
                "count": 4,
                "entity": "Glenn",
                "label": "PERSON"
            }
        ]
    }

    aggregates = multi_model_aggregator.aggregate([enrichment1, enrichment2, enrichment3])
    print(aggregates)
