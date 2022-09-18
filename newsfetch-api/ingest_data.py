import json
import logging
import os

import requests

import config

class Ingester():
    def __init__(self,
                 api_endpoint = config.API_ENDPOINT,
                 source_folder = config.SOURCE_FOLDER):
        self.api_endpoint = api_endpoint
        self.source_folder = source_folder

    def ingest(self):
        logging.info("Ingesting data from " + self.source_folder + " to " + self.api_endpoint)
        for root, dirs, files in os.walk(self.source_folder):
            for name in files:
                if name.endswith((".json")):
                    full_path = os.path.join(root, name)
                    logging.info("Ingesting " + full_path)
                    with open(full_path) as f:
                        data = json.load(f)
                        requests.post(self.api_endpoint + "/article", json=data)


if __name__ == "__main__":
    ingester = Ingester()
    ingester.ingest()