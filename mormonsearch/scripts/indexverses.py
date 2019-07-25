import os
import json
from glob import glob

from mormonsearch.search import Verse, add_verses


def parse_verses(path):
    with open(path) as f:
        data = json.load(f)

    return data['verses']


if __name__ == '__main__':
    paths = list(
        map(lambda path: os.path.abspath(path), glob('./data/*.json'))
    )

    print(f"Importing verses from {', '.join(paths)}")

    books_verses = list(map(lambda path: parse_verses(path), paths))
    dict_verses = [verse
                   for book_verses in books_verses for verse in book_verses]
    verses = [Verse(reference=v['reference'], text=v['text'])
              for v in dict_verses]

    add_verses(verses)

    print(f'Imported {len(verses)} verses')

