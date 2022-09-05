from urllib.parse import urlparse

from newsplease import NewsPlease, NewscrawlerItem

from newsfetch_core.api_schemas import Article


class NewsPleaseAdapter():
    def __init__(self, article: NewscrawlerItem, url: str):
        self.article = article
        self.url = url
        self.domain = urlparse(url).netloc


    def _process_article(self) -> dict:
        published_date = None
        if self.article.date_publish:
            published_date = self.article.date_publish.strftime('%Y-%m-%dT%H:%M:%SZ')

        return {
            'title': self.article.title,
            'authors': self.article.authors,
            'content': self.article.maintext,
            'excerpt': self.article.description,
            'content_length': len(self.article.maintext),
            'published_date': published_date,
            'url': self.url,
            'domain': self.domain,
            'media': self.article.image_url,
            'language': self.article.language,
        }

    def get_article(self) -> Article:
        return Article(**self._process_article())

class NewsPleaseUrlAdapter(NewsPleaseAdapter):
    def __init__(self, url):
        super().__init__(NewsPlease.from_url(url, timeout=60), url=url)

class NewsPleaseHtmlAdapter(NewsPleaseAdapter):
    def __init__(self, html, url):
        super().__init__(NewsPlease.from_html(html, fetch_images=False), url=url)
