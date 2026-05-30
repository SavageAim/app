# The builder image, used to build the virtual environment
FROM python:3.11-slim-buster AS builder

RUN pip3 install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /savage-aim

COPY . .

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --with cors,wsgi

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster AS runtime

ENV VIRTUAL_ENV=/savage-aim/.venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /savage-aim

COPY --from=builder /savage-aim /savage-aim
RUN mv backend/task_urls.py backend/urls.py && \
    mv backend/tasks_settings.py backend/settings.py

# Set the daphne to run the asgi file
EXPOSE 443
ENTRYPOINT python manage.py schedule_tasks && \
           python manage.py initialize_subscribers && \
           gunicorn --bind=0.0.0.0:443 -k gevent --timeout 600 --access-logfile - --log-file - --log-level info --capture-output --enable-stdio-inheritance backend.wsgi
