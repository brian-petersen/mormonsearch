FROM python:3.7.4-alpine

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Build index
COPY data data
COPY mormonsearch/scripts mormonsearch/scripts
COPY mormonsearch/search.py mormonsearch/search.py
RUN python -m mormonsearch.scripts.indexverses

# Copy rest of app over
COPY mormonsearch mormonsearch

# Set default environment variables for flask
ENV FLASK_APP mormonsearch
ENV FLASK_RUN_PORT 80
ENV FLASK_RUN_HOST 0.0.0.0

CMD ["flask", "run"]
