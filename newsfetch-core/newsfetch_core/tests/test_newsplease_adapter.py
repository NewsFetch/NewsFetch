import datetime
import json

from newsfetch_core.api_schemas import Article
from newsfetch_core.newplease_adapter import NewsPleaseHtmlAdapter


class TestNewsPleaseHtmlAdapter():
    def test_get_article(self):
        with(open('warc_extract.json', 'r')) as f:
            html = json.loads(f.read())['article_html']
        newsplease_html_adapter = NewsPleaseHtmlAdapter(html, url="https://npr.org/article")
        article: Article = newsplease_html_adapter.get_article()
        assert article.title == "Fresh Air's summer music interviews: Isaac Hayes"
        assert article.url == 'https://npr.org/article'
        assert article.domain == 'npr.org'
        assert article.excerpt.startswith('Hayes helped shape the sound of Memphis soul in the 1960s')
        assert article.content.startswith("Fresh Air's summer music interviews: Isaac Hayes")
        assert article.content_length == 14355
        assert article.authors == ['Terry Gross']
        assert article.published_date == datetime.datetime.strptime('2022-09-02T13:52:20', '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc)
        assert article.language == 'en'
        assert article.media == 'https://media.npr.org/include/images/facebook-default-wide.jpg?s=1400'
        assert article.meta is None
