import datetime
from typing import Optional, List, Any
from pydantic import BaseModel

import config


class Classification(BaseModel):
    label: str
    confidence: float

class Classifications(BaseModel):
    parent: Optional[str]
    classifications: list

class Summarization(BaseModel):
    summary: str

class EntityBase(BaseModel):
    entity: str
    label: str
    model_label: Optional[str]
    confidence: Optional[float] = 1.0

class Entity(EntityBase):
    start_offset: Optional[int]
    end_offset: Optional[int]

class ResolvedEntity(Entity):
    resolution_id: Optional[str]
    resolution_link: Optional[str]
    resolution_type: Optional[str]
    description: Optional[str]

class EntityAggregate(EntityBase):
    count: Optional[int] = 0

class NER(BaseModel):
    entities: List[Entity]
    entity_aggregates: List[EntityAggregate]
    entities_composed: Optional[List[Entity]] = None

class NERAggregate(BaseModel):
    entity_aggregates: List[EntityAggregate]

class EnrichmentInput(BaseModel):
    enricher_clazz: Any
    enrich_method_name: str = config.ENRICH_METHOD_NAME
    enriched_by: str = config.ENRICHED_BY
    enrichment_version: str = "1.0"
    model_source: Optional[str]
    model_name: Optional[str]
    category: Optional[str]
    target_languages: Optional[list] = ["en"]


class EnrichmentsResponse(BaseModel):
    total_results: int
    enrichments: list

class EnrichmentsPaginatedResponse(EnrichmentsResponse):
    total_results: int
    start: int
    size: int
    last_sourced_date: Optional[datetime.datetime]
    enrichments: list

class ApiKey(BaseModel):
    api_key: str
    created_date: datetime.datetime
    name: str
    email: str

class Keyword(BaseModel):
    keyword: str
    distance: float

class Keywords(BaseModel):
    keywords: List[Keyword]

class Topic(BaseModel):
    topic_words: list[tuple[str, float]]
    score: float

class Topics(BaseModel):
    topics: List[Topic]