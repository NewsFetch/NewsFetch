# NewsFetch

## Sub-projects

This repository contains the following sub-projects:

* [newsfetch-core](./newsfetch-core): The core library for the NewsFetch project
* [newsfetch-common-crawl](./newsfetch-common-crawl): Various utilities that NewsFetch project uses in interfacing with CommonCrawl
* [newsfetch-api](./newsfetch-api): An example API for the NewsFetch project

## Projects that NewsFetch depends on

* [CommonCrawl](https://commoncrawl.org): The CommonCrawl project is a large-scale web crawl that is used by NewsFetch to collect news articles
  * https://commoncrawl.org/2016/10/news-dataset-available/ 
* [NewsPlease](https://github.com/fhamborg/news-please): NewsPlease is a Python library that NewsFetch uses to extract news articles from HTML pages

For enriching the news articles, NewsFetch uses the following projects:
* [Spacy](https://spacy.io): Spacy is a Python library for natural language processing
* [HuggingFace](https://huggingface.co): HuggingFace hosts pre-trained ML models that is used in NewsFetch for natural language processing


## Setup

First install the following:

* Python 3.9
* [Poetry](https://python-poetry.org/docs/#installation)

Recommended, use pyenv to manage your python versions.

* [pyenv](https://github.com/pyenv/pyenv)

### Virtual environment

It is highly recommended to use a virtual environment. This is done to avoid conflicts with other projects.

To create a virtual environment, run the following command:

In each sub-project, run the following command:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate
```
### Install dependencies

Poetry is used to install and manage dependencies. It is also used to package the modules/libraries.

Note: The sub-projects use relative paths to import the other sub-projects/libraries. 
This is done to make it easier to develop the sub-projects. 

To install the dependencies, run the following command:

```bash
poetry install
```