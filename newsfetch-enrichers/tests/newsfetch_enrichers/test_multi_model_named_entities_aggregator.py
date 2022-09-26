import pytest

import config
from newsfetch_enrichers.named_entities_aggregator import MultiModelNamedEntitiesAggregator


def test_multi_model_aggregator_entity_aggregates_validations():
    multi_model_aggregator = MultiModelNamedEntitiesAggregator()

    enrichment1 = {
        "category": "ner",
        "dataset": "news-cc",
        "dataset_id": "c25dbc0b-be6b-401a-823a-de827ecda50e",
        "detected_language": "en",
        "title": "A tale of two cities",
        "uri": "https://google.com"
    }

    # validations success on copy - fails further on key error as enrichment data is dummy above
    try:
        enrichment2 = enrichment1.copy()
        aggregates = multi_model_aggregator.aggregate([enrichment1, enrichment2])
        pytest.fail()
    except KeyError as ke:
        pass

    # tests for various validation failures
    enrichment2 = enrichment1.copy()
    enrichment2["category"] = "changed"
    aggregates = multi_model_aggregator.aggregate([enrichment1, enrichment2])
    assert aggregates is None

    enrichment2 = enrichment1.copy()
    enrichment2["dataset"] = "changed"
    aggregates = multi_model_aggregator.aggregate([enrichment1, enrichment2])
    assert aggregates is None

    enrichment2 = enrichment1.copy()
    enrichment2["dataset_id"] = "changed"
    aggregates = multi_model_aggregator.aggregate([enrichment1, enrichment2])
    assert aggregates is None

    enrichment2 = enrichment1.copy()
    enrichment2["detected_language"] = "changed"
    aggregates = multi_model_aggregator.aggregate([enrichment1, enrichment2])
    assert aggregates is None

    enrichment2 = enrichment1.copy()
    enrichment2["title"] = "changed"
    aggregates = multi_model_aggregator.aggregate([enrichment1, enrichment2])
    assert aggregates is None

    enrichment2 = enrichment1.copy()
    enrichment2["uri"] = "changed"
    aggregates = multi_model_aggregator.aggregate([enrichment1, enrichment2])
    assert aggregates is None


def test_multi_model_aggregator_entity_aggregates():
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
        "enriched_by": "newsfetch",
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
        "enriched_by": "newsfetch",
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
        "enriched_by": "newsfetch",
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
    assert aggregates["category"] == config.NER_AGGREGATED
    assert len(aggregates["aggregation_details"]) == 3
    model_detail = aggregates["aggregation_details"][0]
    assert model_detail["enrichment_id"] == enrichment1["id"]
    model_detail = aggregates["aggregation_details"][1]
    assert model_detail["enrichment_id"] == enrichment2["id"]
    model_detail = aggregates["aggregation_details"][2]
    assert model_detail["enrichment_id"] == enrichment3["id"]

    assert len(aggregates["entity_aggregates"]) == 3
    entity_aggregate = aggregates["entity_aggregates"][0]
    assert entity_aggregate['entity'] == 'Today'
    assert entity_aggregate['label'] == 'DATE'
    assert entity_aggregate['confidence'] == pytest.approx((0.9*1 + 0.8*2 + 0.7*3) / (1+2+3))
    assert entity_aggregate['count'] == 1 + 2 + 3
    entity_aggregate = aggregates["entity_aggregates"][1]
    assert entity_aggregate['entity'] == 'Glenn Beck'
    assert entity_aggregate['label'] == 'PERSON'
    assert entity_aggregate['confidence'] == pytest.approx((0.8*2 + 0.7*3)/(2+3))
    assert entity_aggregate['count'] == 2 + 3
    entity_aggregate = aggregates["entity_aggregates"][2]
    assert entity_aggregate['entity'] == 'Glenn'
    assert entity_aggregate['label'] == 'PERSON'
    assert entity_aggregate['confidence'] == pytest.approx(0.6)
    assert entity_aggregate['count'] == 4
