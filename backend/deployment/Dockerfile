# The builder image, used to build the virtual environment
FROM python:3.11-slim-buster AS builder

RUN pip3 install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /savage-aim

COPY . .

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --with wsgi,cors

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster AS runtime

ENV VIRTUAL_ENV=/savage-aim/.venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /savage-aim

COPY --from=builder /savage-aim /savage-aim
RUN mv backend/urls_live.py backend/urls.py && \
    mv backend/settings_live.py backend/settings.py

# Set the gunicorn to run the wsgi file
EXPOSE 443
ENTRYPOINT python3 manage.py migrate &&  \
           python3 manage.py seed && \ 
           gunicorn --bind=0.0.0.0:443 -k gevent --timeout 300 --access-logfile - --log-file - --log-level info --capture-output --enable-stdio-inheritance backend.wsgi
