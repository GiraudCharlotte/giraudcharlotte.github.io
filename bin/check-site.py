"""Check the built bilingual site using only Python's standard library."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
routes = ['', 'recherche', 'enseignement', 'parcours', 'publications', 'conferences', 'cv']

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

count = 0
for language in ['fr', 'en']:
    prefix = '' if language == 'fr' else 'en/'
    for route in routes:
        path = root / prefix / route / 'index.html'
        assert path.is_file(), path
        text = path.read_text()
        parsed = Page(text)
        html = next(attrs for tag, attrs in parsed.tags if tag == 'html')
        assert html.get('lang') == language, (path, html)
        assert sum(tag == 'h1' for tag, _ in parsed.tags) == 1, path
        current = [attrs for tag, attrs in parsed.tags if attrs.get('aria-current') == 'page']
        assert len(current) == 1, (path, current)
        switch = next(attrs for tag, attrs in parsed.tags if 'language-switch' in attrs.get('class', ''))
        expected = ('/en/' if language == 'fr' else '/') + (route + '/' if route else '')
        assert switch['href'] == expected, (path, switch, expected)
        for forbidden in ['safelinks.protection.outlook.com', 'Pour les publications,', 'remettre les liens', 'Your City', 'Albert Einstein']:
            assert forbidden not in text, (path, forbidden)
        assert '&lt;section class=' not in text, ('HTML rendered as code', path)
        for tag, attrs in parsed.tags:
            if tag == 'img':
                assert attrs.get('alt'), (path, 'missing alt')
            value = attrs.get('href') if tag == 'a' else attrs.get('src') if tag in ['img', 'script'] else attrs.get('href') if tag == 'link' and attrs.get('rel') == 'stylesheet' else None
            if not value or not value.startswith('/'):
                continue
            target = unquote(urlparse(value).path)
            local = root / target.lstrip('/')
            if target.endswith('/'):
                local /= 'index.html'
            assert local.is_file(), (path, value)
        if route == 'conferences':
            pdfs = [attrs['href'] for tag, attrs in parsed.tags if tag == 'a' and attrs.get('href', '').endswith('.pdf')]
            assert set(pdfs) == {'/assets/pdf/Invisible_Finance_2026.pdf', '/assets/pdf/colloque_genre_et_argent.pdf'}, (path, pdfs)
            assert ('panel en cours d’évaluation' if language == 'fr' else 'panel under review') in text, path
        if route == 'publications':
            assert '173' in text and '2027' in text, path
        if route == 'cv':
            assert '/assets/pdf/CV_Charlotte_Giraud.pdf' in text, path
        count += 1
    assert (root / prefix / '404.html').is_file()
print(f'PASS: {count} academic pages, 2 error pages, language switches, local links, portrait alt text, CV and conference programmes.')
