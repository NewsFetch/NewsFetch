import json

from newsfetch_core.newplease_adapter import NewsPleaseHtmlAdapter


class TestNewsPleaseHtmlAdapter():
    def test_get_article(self):
        with(open('warc_extract.json', 'r')) as f:
            html = json.loads(f.read())['article_html']
        newsplease_html_adapter = NewsPleaseHtmlAdapter(html, url="google.com")
        news = newsplease_html_adapter.get_news()
        assert news['url'] == 'google.com'
