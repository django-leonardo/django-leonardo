FROM python:2.7.16-stretch

COPY . /source/leonardo
COPY ./docker/site /app/site
COPY ./docker/settings /app/settings

RUN apt-get -y update && \
    apt-get install -y gettext git python-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r /source/leonardo/requirements/default.txt && \
    pip install --no-cache-dir -r /source/leonardo/requirements/modules.txt && \
    pip install gunicorn Whoosh psycopg2-binary python-memcached sentry-sdk && \
    pip install -e /source/leonardo && \
    cd /src/leonardo-cookie-law/leonardo_cookie_law && python /app/site/manage.py compilemessages

RUN useradd --system leonardo && \
    chown -R leonardo:leonardo /app/

EXPOSE 8000
ENV PORT 8000