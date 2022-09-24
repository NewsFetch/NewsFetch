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
  * HuggingFace Transformers
  * Flair
  * AllenNLP
* Summarization (Abstractive)
  * HuggingFace Transformers
* Keyword Extraction
  * KeyBERT
* Topic Modeling
  * BERTopic
* Generative Question Answering
  * DocT5 

## Running an enrichment

### AllenNLP

To run AllenNLP NER, first install the requirements

```bash
pip install -r requirements-allennlp.txt
```

This installed a previous version of Spacy that AllenNLP needs.

After that, run the usual steps.


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
This directoy will be used to store the CommonCrawl data.

First use the docker image to download the latest CommonCrawl data.

```bash
docker run -e COMMON_CRAWL_DATA_DIR=/data -v $(pwd)/commoncrawl-data:/data -it --name newsfetch-download-warc newsfetch/newsfetch-common-crawl sh ./get_latest_warc.sh
```

This will download the latest WARC file to the `commoncrawl-data` directory.

Make a note of the name of the WARC file that was downloaded.
Let us say the name was `CC-NEWS-20220915230049-00936.warc.gz`.

Now use the image to extract the news articles from the WARC file.

Be sure to map the volumes correctly. 

In the following example, The `commoncrawl-data` directory is mapped to `/data` in the container.
The WARC file name is provided in reference to this volume name.
It will be `/data/CC-NEWS-20220915230049-00936.warc.gz`

```bash
docker run -e COMMON_CRAWL_DATA_DIR=/data -v $(pwd)/commoncrawl-data:/data -it --name newsfetch-extract-warc newsfetch/newsfetch-common-crawl sh ./extract_warc.sh /data/CC-NEWS-20220915230049-00936.warc.gz
```

Finally, process the extracted news articles.

```bash
docker run -e COMMON_CRAWL_DATA_DIR=/data -v $(pwd)/commoncrawl-data:/data -it --name newsfetch-process-warc newsfetch/newsfetch-common-crawl sh ./process_extracted_warc_files.sh /data/CC-NEWS-20220915230049-00936.warc.gz
```