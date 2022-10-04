# Installation

Follow instructions in the [parent directory](../README.md).

# Usage

Copy `.env.example` to `.env` and update the required values.

The scripts in this directory are used to download the CommonCrawl data and extract the news articles from the data.

```.env
# The directory where the CommonCrawl data will be downloaded to
COMMON_CRAWL_DATA_DIR = "./commoncrawl-data"

# The directory where the extracted news articles will be saved to
PROCESSED_CONTENT_DIR = "processed-content"

```

## Avialable Enrichers

* NER - Named Entity Recognition
  * Spacy
  * Transformer NER models
  * Flair
  * AllenNLP
* Summarization (Abstractive)
  * Transformer summarization models
* Keyword Extraction
  * KeyBERT
  * Transformer keyword extraction models
* Topic Modeling
  * BERTopic
* Question Answering
  * Transformer QnA models 
* Generative Question Answering
  * DocT5 

## Running an enrichment

Each enrichment that has been implemented has a main() function that can be run from the command line. The main() function that shows the usage.

### AllenNLP

To run AllenNLP NER, first install the requirements

```bash
pip install -r requirements-allennlp.txt
```

This installed a previous version of Spacy that AllenNLP needs.

After that, run the main() function.

### Run

For the next commands, the data in `sample-data` sub folder under the project root is used.
This directoy has the processed CommonCrawl News, and this will be further enriched.

`PYTHONPATH=. python run_enrichers.py --newsfetch-processed-base-dir=../sample-data/CC-NEWS-20220918140302-00985/`

This will run all the enrichers, and save the output in the `enrichments` sub folder under the directory specified in the
`newsfetch-processed-base-dir` argument.

The output strcutrue will look like:

    |-- sample-data
        |-- CC-NEWS-20220915230049-00936
        |-- CC-NEWS-20220918140302-00985
            |-- enrichments
            |   |-- ner
            |   |   |-- spacy
            |   |   |   |-- en_core_web_md
            |   |   |   |   |-- abc7.com
            |   |   |   |   |   |-- 3ffa69ee-66f1-4cb9-b13e-31ceb912b5af.json
            |   |   |   |   |-- chicago.suntimes.com
            |   |   |   |   |   |-- 0eae59b8-6ea4-4db9-9236-ee535f6d3619.json
            |   |   |   |   |-- www.npr.org
            |   |   |   |       |-- 22bce741-521d-4568-a08c-9596ed713c4b.json
            |   |   |   |-- en_core_web_trf
            |   |   |       |-- abc7.com
            |   |   |       |   |-- 3ffa69ee-66f1-4cb9-b13e-31ceb912b5af.json
            |   |   |       |-- chicago.suntimes.com
            |   |   |       |   |-- 0eae59b8-6ea4-4db9-9236-ee535f6d3619.json
            |   |   |       |-- www.npr.org
            |   |   |           |-- 22bce741-521d-4568-a08c-9596ed713c4b.json
            |   |   |-- transformers
            |   |       |-- elastic
            |   |           |-- distilbert-base-cased-finetuned-conll03-english
            |   |               |-- abc7.com
            |   |               |   |-- 3ffa69ee-66f1-4cb9-b13e-31ceb912b5af.json
            |   |               |-- chicago.suntimes.com
            |   |               |   |-- 0eae59b8-6ea4-4db9-9236-ee535f6d3619.json
            |   |               |-- www.npr.org
            |   |                   |-- 22bce741-521d-4568-a08c-9596ed713c4b.json
            |   |-- summarization
            |   |   |-- transformers
            |   |       |-- sshleifer
            |   |           |-- distilbart-cnn-6-6
            |   |               |-- chicago.suntimes.com
            |   |               |   |-- 0eae59b8-6ea4-4db9-9236-ee535f6d3619.json
            |   |               |-- www.npr.org
            |   |                   |-- 22bce741-521d-4568-a08c-9596ed713c4b.json
            |   |-- zeroshot-classification
            |       |-- transformers
            |           |-- valhalla
            |               |-- distilbart-mnli-12-1
            |                   |-- abc7.com
            |                   |   |-- 3ffa69ee-66f1-4cb9-b13e-31ceb912b5af.json
            |                   |-- chicago.suntimes.com
            |                   |   |-- 0eae59b8-6ea4-4db9-9236-ee535f6d3619.json
            |                   |-- www.npr.org
            |                       |-- 22bce741-521d-4568-a08c-9596ed713c4b.json
            |-- processed-content
            |   |-- abc7.com
            |   |   |-- 3ffa69ee-66f1-4cb9-b13e-31ceb912b5af.json
            |   |-- chicago.suntimes.com
            |   |   |-- 0eae59b8-6ea4-4db9-9236-ee535f6d3619.json
            |   |-- www.npr.org
            |       |-- 22bce741-521d-4568-a08c-9596ed713c4b.json
            |-- warc-extract
                |-- abc7.com
                |   |-- 3ffa69ee-66f1-4cb9-b13e-31ceb912b5af.json
                |-- chicago.suntimes.com
                |   |-- 0eae59b8-6ea4-4db9-9236-ee535f6d3619.json
                |-- www.npr.org
                    |-- 22bce741-521d-4568-a08c-9596ed713c4b.json



## Docker

### Build 

Run this from the root directory of the project.

```bash
docker build -t newsfetch/newsfetch-enrichers -f ./Dockerfile-enrichers .
```

If you are on M1 Mac, or any other platform, you can use the following command to build the image for the platform you are on.

`docker build -t newsfetch/newsfetch-enrichers -f ./Dockerfile-enrichers . --platform linux/amd64`

### Pull from DockerHub

The image is also available on DockerHub.

```bash
docker pull newsfetch/newsfetch-enrichers
```

