import os

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO")

SPACY = "spacy"
SPACY_NER_EN_CORE_WEB_SM = "en_core_web_sm"
SPACY_NER_EN_CORE_WEB_MD = "en_core_web_md"
SPACY_NER_EN_CORE_WEB_LG = "en_core_web_lg"
SPACY_NER_EN_CORE_WEB_TRF = "en_core_web_trf"

NEWSFETCH = "NewsFetch"
ENRICHED_BY = os.environ.get("ENRICHED_BY", NEWSFETCH)
ENRICH_METHOD_NAME = "enrich"
ENRICHMENT_TYPE_INFERENCE = "inference"
ENRICHMENT_TYPE_INSIGHT = "insight"

NER = "ner"
NER_AGGREGATED = "ner-aggregated"
ZERO_SHOT_CLASSIFICATION = "zeroshot-classification"
LANGUAGE_DETECTION = "language-detection"
SUMMARIZATION = "summarization"

BUSINESS_AND_FINANCE = 'business'
SCIENCE_AND_TECHNOLOGY = 'science'
ARTS_AND_ENTERTAINMENT = 'entertainment'

NEWS_HIGH_LEVEL_CATEGORIES = [BUSINESS_AND_FINANCE, 'travel', 'politics', 'religion', 'sport', ARTS_AND_ENTERTAINMENT,
                              SCIENCE_AND_TECHNOLOGY]
BUSINESS_AND_FINANCE_SUB_CATEGORIES = ['markets', 'economy', 'finance', 'housing']
SCIENCE_AND_TECHNOLOGY_SUB_CATEGORIES = ['climate', 'health', 'technology', 'coronavirus', 'space', 'astronomy']
ARTS_AND_ENTERTAINMENT_SUB_CATEGORIES = ['film', 'music', 'TV', 'theatre', 'books', 'dance', 'art']
NEWS_REGIONS = ['USA', 'North America', 'Middle East', 'Americas', 'Europe', 'Asia', 'Australia', 'Africa', 'India',
                'Germany', 'France', 'Netherlands', 'Dubai']

TRANSFORMERS = "transformers"
TRANSFORMERS_NER_PIPELINE_NAME = "ner"
TRANSFORMERS_ZERO_SHOT_CLASSIFICATION_PIPELINE_NAME = "zero-shot-classification"
TRANSFORMERS_SUMMARIZATION_PIPELINE_NAME = "summarization"
TRANSFORMERS_QNA_PIPELINE_NAME = "question-answering"


TRANSFORMERS_NER_DSLIM_BERT_BASE_NER = "dslim/bert-base-NER"
TRANSFORMERS_NER_XML_ROBERTA_LARGE_FINETUNED_CONLL03_ENGLISH = "xlm-roberta-large-finetuned-conll03-english"
TRANSFORMERS_NER_ELASTIC_DISTILBERT_BASE_UNCASED_FINETUNED_CONLL03_ENG_NER = "elastic/distilbert-base-uncased-finetuned-conll03-english"
TRANSFORMERS_NER_ELASTIC_DISTILBERT_BASE_CASED_FINETUNED_CONLL03_ENG_NER = "elastic/distilbert-base-cased-finetuned-conll03-english"
TRANSFORMERS_NER_DAVLAN_DISTILBERT_BASE_MULTILINGUAL_CASED_NER = "Davlan/distilbert-base-multilingual-cased-ner-hrl"
TRANSFORMERS_NER_DAVLAN_DISTILBERT_BASE_MULTILINGUAL_CASED_NER_LANGUAGES = ["ar", "de", "en", "es", "fr", "it", "lv", "nl", "pt", "zh"]

TRANSFORMERS_CLASSIFICATION_VALHALLA_DISTILBART_MNLI_12_1 = "valhalla/distilbart-mnli-12-1"
TRANSFORMERS_CLASSIFICATION_CROSS_ENCODER_NLI_DISTILROBERTA_BASE = "cross-encoder/nli-distilroberta-base"

TRANSFORMERS_SUMMARIZATION_SSHLEIFER_DISTILBART_CNN_6_6 = "sshleifer/distilbart-cnn-6-6"
TRANSFORMERS_SUMMARIZATION_GOOGLE_PEGASUS_XSUM = "google/pegasus-xsum"

TRANSFORMERS_DOC2QUERY_T5_BASE_MSMACRO = "castorini/doc2query-t5-base-msmarco"

TRANSFORMERS_QNA_DEEPSET_TINYROBERTA_SQUAD2 = "deepset/tinyroberta-squad2"

FLAIR_NER_ENGLISH_ONTONOTES_LARGE = "flair/ner-english-ontonotes-large"

ALLENAI_NER_ELMO_KEY = "allenai/ner-elmo.2021-02-12"
ALLENAI_NER_ELMO_DICT = {
    ALLENAI_NER_ELMO_KEY: "https://storage.googleapis.com/allennlp-public-models/ner-elmo.2021-02-12.tar.gz"}

KEYBERT_ALL_MINI_LM_L6_V2 = "all-MiniLM-L6-v2"

SPACY_FLAIR_ENTITY_LABEL_MAPPINGS = {
    'CARDINAL': 'CARDINAL',
    'DATE': 'DATE',
    'EVENT': 'EVENT',
    'FAC': 'FAC',
    'GPE': 'GPE',
    'LANGUAGE': 'LANGUAGE',
    'LAW': 'LAW',
    'LOC': 'LOC',
    'MONEY': 'MONEY',
    'NORP': 'NORP',
    'ORDINAL': 'ORDINAL',
    'ORG': 'ORG',
    'PERCENT': 'PERCENT',
    'PERSON': 'PERSON',
    'PRODUCT': 'PRODUCT',
    'QUANTITY': 'QUANTITY',
    'TIME': 'TIME',
    'WORK_OF_ART': 'WORK_OF_ART'
}

TRANSFORMERS_ALLENAI_ENTITY_LABEL_MAPPINGS = {
    'B-LOC': 'LOC',
    'I-LOC': 'LOC',
    'L-LOC': 'LOC',
    'U-LOC': 'LOC',
    'LOC': 'LOC',
    'B-ORG': 'ORG',
    'I-ORG': 'ORG',
    'L-ORG': 'ORG',
    'U-ORG': 'ORG',
    'ORG': 'ORG',
    'B-PER': 'PERSON',
    'I-PER': 'PERSON',
    'L-PER': 'PERSON',
    'U-PER': 'PERSON',
    'PER': 'PERSON',
    'B-MISC': 'MISC',
    'I-MISC': 'MISC',
    'L-MISC': 'MISC',
    'U-MISC': 'MISC',
    'MISC': 'MISC',
    'O': ''
}

EXCLUDED_KEYS = []
JSON_OUT_FILE_EXT = ".json"