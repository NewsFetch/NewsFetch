from keybert import KeyBERT

import config
from common.datatypes import Keywords, Keyword
from newsfetch_enrichers.enricher import Enricher


class KeyBertKeywordExtractionEnricher(Enricher):
    def __init__(self, model_name: str):
        self.model_name = model_name

    def enrich(self, text: str) -> Keywords:
        kw_model = KeyBERT(model=self.model_name)
        extracted_keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), use_mmr=True, diversity=0.5, top_n=10)

        keywords = [] # type: list[Keyword]
        for extracted_keyword in extracted_keywords:
            keywords.append(Keyword(keyword=extracted_keyword[0], distance=extracted_keyword[1]))

        return Keywords(keywords=keywords)

if __name__ == '__main__':
    content = '''
    The ongoing Russia Ukraine war has a new player – the Anonymous hacker collective. Amidst Russia’s offensive against Ukraine, Anonymous hackers have claimed to have taken down several Russian government websites, and RT.com, the website of the state-controlled television network.
    The hacker collective made an announcement on Twitter yesterday, stating that they’re engaged in a ‘cyber war’ against the Russian government.

    Some of the websites that were either taken down by Anonymous or were slowed down include those of the Russian government, the Kremlin, Duma and the Ministry of Defence.
    Apart from RT.com, the hacker collective also launched distributed denial of service (DDoS) attacks against websites of Russian internet service providers Com2Com, Relcom, Sovam Teleport and PTT-Teleport Moscow.
    Various Anonymous accounts were found using the #OpRussia and #OpKremlin hashtags on Twitter, similar to the #OpISIS campaign that was launched earlier in an attempt to take down the terrorist organisation’s online propaganda attempts.
    '''
    sents = [sent.strip() for sent in content.split("\n") if sent]
    keybert_keyword_extractor_enricher = KeyBertKeywordExtractionEnricher(model_name=config.KEYBERT_ALL_MINI_LM_L6_V2)
    results = keybert_keyword_extractor_enricher.enrich(content)
    print(results)

