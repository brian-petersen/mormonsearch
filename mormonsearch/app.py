import csv
import io

from mormonsearch.search import search_verses

from flask import Flask, request


DEFAULT_LIMIT = 10
VALID_FORMATS = ('json', 'csv')


app = Flask(
    __name__,
    static_folder='www',
    static_url_path='/'
)


@app.route('/')
def _root():
    return app.send_static_file('index.html')


@app.route('/api/search')
def _search():
    def _format_json(verses, count):
        return {'totalCount': count, 'verses': verses}

    def _format_csv(verses):
        verses = [verse.asdict() for verse in verses]

        output = io.StringIO()

        writer = csv.DictWriter(output, fieldnames=['reference', 'text'])
        writer.writerows(verses)

        return output.getvalue()

    query = request.args.get('query')
    limit = request.args.get('limit', 10, type=int)
    _format = request.args.get('format', 'json')

    if not query:
        return {'error': 'Query not provided'}, 400

    if _format not in VALID_FORMATS:
        return {'error': 'Invalid format'}, 400        

    verses, count = search_verses(query, limit)

    if _format == 'json':
        return _format_json(verses, count)
    elif _format == 'csv':
        return _format_csv(verses), {'Content-Type': 'text/plain'}
    else:
        return {'error': 'Server error'}, 500
