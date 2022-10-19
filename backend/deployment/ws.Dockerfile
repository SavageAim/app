FROM python:3

WORKDIR /savage-aim

COPY . .

# Install requirements and move live files to the correct spot
RUN pip3 install -r requirements.txt && \
    pip3 install daphne && \
    mv backend/urls_live.py backend/urls.py && \
    mv backend/settings_live.py backend/settings.py

# Set the gunicorn to run the wsgi file
EXPOSE 443
ENTRYPOINT daphne -b 0.0.0.0 -p 443 backend.asgi:application
