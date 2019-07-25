FROM python:3.7.4-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY data data
COPY mormonsearch/scripts mormonsearch/scripts
COPY mormonsearch/search.py mormonsearch/search.py
RUN python -m mormonsearch.scripts.indexverses

COPY mormonsearch mormonsearch

ENV FLASK_APP mormonsearch
ENV FLASK_RUN_PORT 80
ENV FLASK_RUN_HOST 0.0.0.0

CMD ["flask", "run"]
