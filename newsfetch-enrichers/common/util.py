import json
import os
import uuid
from datetime import datetime
from typing import List

import config
from common.datatypes import EnrichmentInput


def build_enrichment_payload(processed_content, enrichment_input: EnrichmentInput):
    enrichment_payload =  {k:v for k,v in processed_content.items() if k not in config.EXCLUDED_KEYS}
    id = str(uuid.uuid4())
    enrichment_payload.update({
        "id": id,
        "enriched_by": enrichment_input.enriched_by,
        "enrichment_version": enrichment_input.enrichment_version,
        "enriched_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "enrichment_type": config.ENRICHMENT_TYPE_INFERENCE,
        "model_source": enrichment_input.model_source,
        "model_name": enrichment_input.model_name,
        "category": enrichment_input.category,
    })
    return enrichment_payload

def write_json_to_file(dirs: List, file_name, data):
    dir_path = os.path.join(*dirs)
    os.makedirs(dir_path, exist_ok=True)
    path = os.path.join(dir_path, file_name)
    print(f"saving data to {path}...")
    with(open(path, "w+")) as out_file:
        out_file.writelines(json.dumps(data))
