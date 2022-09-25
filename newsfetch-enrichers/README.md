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

### Run

For the next commands, it is assumed that there is a directory named `commoncrawl-data` in the current directory.
This directoy has the processed CommonCrawl News which is further enriched.

