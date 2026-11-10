"""Validate crawlable static-page metadata and sitemap consistency."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://matejsmutny.com/'

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta, self.canonical, self.schemas = {}, [], []
        self.in_schema = False
        self.schema = ''
        self.h1_count = 0
        self.titles = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            key = a.get('name', a.get('property'))
            if key:
                assert key not in self.meta, f'Duplicate metadata: {key}'
                self.meta[key] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a['href'])
        if tag == 'h1': self.h1_count += 1
        if tag == 'title': self.titles += 1
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.in_schema, self.schema = True, ''
    def handle_data(self, data):
        if self.in_schema: self.schema += data
    def handle_endtag(self, tag):
        if tag == 'script' and self.in_schema:
            self.schemas.append(json.loads(self.schema))
            self.in_schema = False

expected = set()
for path in sorted(ROOT.glob('*.html')):
    page = Page()
    page.feed(path.read_text())
    url = BASE if path.name == 'index.html' else BASE + path.name
    assert page.canonical == [url], path.name
    assert page.meta.get('description'), path.name
    assert page.meta.get('og:url') == url, path.name
    assert page.meta.get('og:title') and page.meta.get('og:description'), path.name
    assert page.titles == 1 and page.h1_count == 1, path.name
    assert len(page.schemas) == 1, path.name
    for node in page.schemas[0]['@graph']:
        if node['@type'] == 'MusicRecording':
            assert (ROOT / urlsplit(node['audio']['contentUrl']).path.lstrip('/')).is_file()
    if 'noindex' not in page.meta['robots']: expected.add(url)

ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = [node.text for node in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
assert len(urls) == len(set(urls)), 'Duplicate sitemap URLs'
assert set(urls) == expected, 'Sitemap does not match indexable canonical pages'
assert 'Sitemap: ' + BASE + 'sitemap.xml' in (ROOT / 'robots.txt').read_text()
print(f'PASS: {len(list(ROOT.glob("*.html")))} pages; metadata, canonicals, headings, JSON-LD, audio assets and {len(urls)} sitemap URLs.')
