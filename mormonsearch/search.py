import os
from dataclasses import dataclass

from whoosh import index
from whoosh.fields import Schema, TEXT, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser


INDEX_PATH = 'index'


@dataclass
class Verse:
    reference: str
    text: str

    def asdict(self):
        return {'reference': self.reference, 'text': self.text}


_verse_schema = Schema(
    reference=STORED(),
    text=TEXT(analyzer=StemmingAnalyzer(), stored=True),
)


if index.exists_in(INDEX_PATH):
    _index = index.open_dir(INDEX_PATH)
else:
    os.mkdir(INDEX_PATH)
    _index = index.create_in(INDEX_PATH, _verse_schema)


def add_verses(verses):
    writer = _index.writer()

    for verse in verses:
        writer.add_document(reference=verse.reference, text=verse.text)

    writer.commit()


def search_verses(query_text, limit):
    parser = QueryParser('text', schema=_verse_schema)
    query = parser.parse(query_text)

    with _index.searcher() as searcher:
        results = searcher.search(query, limit=limit)

        count = len(results)
        verses = [Verse(reference=hit['reference'], text=hit['text']) for hit in results]

    return verses, count
