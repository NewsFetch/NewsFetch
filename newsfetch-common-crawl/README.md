# Installation

Follow instructions in the [parent directory](../README.md).

# Usage

Copy `.env.example` to `.env` and update the required values.

The scripts in this directory are used to download the CommonCrawl data and extract the news articles from the data.

```.env
# The directory where the CommonCrawl data will be downloaded to
COMMON_CRAWL_DATA_DIR = "./commoncrawl-data"

# The directory where the extracted WARC files will be saved to
WARC_EXTRACT_DIR = "warc-extract"

# The directory where the extracted news articles will be saved to
PROCESSED_CONTENT_DIR = "processed-content"

```

## Downloading the CommonCrawl data

`./get_latest_warc.sh` downloads the latest CommonCrawl WARC file.

`./extract_warc.sh` extracts the news articles from the WARC file.

`./process_extracted_warc_files.sh` processes the article html in each extracted WARC file.

## Docker

### Build 

Run this from the root directory of the project.

```bash
docker build -t newsfetch-common-crawl -f ./Dockerfile-commoncrawl .
```

If you are on M1 Mac, or any other platform, you can use the following command to build the image for the platform you are on.

`docker build -t newsfetch-common-crawl -f ./Dockerfile-commoncrawl . --platform linux/amd64`

### Run

For the next commands, it is assumed that there is a directory named `commoncrawl-data` in the current directory.
This directoy will be used to store the CommonCrawl data.

First use the docker image to download the latest CommonCrawl data.

```bash
docker run -e COMMON_CRAWL_DATA_DIR=/data -v $(pwd)/commoncrawl-data:/data -it --name newsfetch newsfetch-common-crawl sh ./get_latest_warc.sh```
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
docker run -e COMMON_CRAWL_DATA_DIR=/data -v $(pwd)/commoncrawl-data:/data -it --name newsfetch newsfetch-common-crawl sh ./extract_warc.sh /data/CC-NEWS-20220915230049-00936.warc.gz
```

Finally, process the extracted news articles.

```bash
docker run -e COMMON_CRAWL_DATA_DIR=/data -v $(pwd)/commoncrawl-data:/data -it --name newsfetch newsfetch-common-crawl sh ./process_extracted_warc_files.sh /data/CC-NEWS-20220915230049-00936.warc.gz
```