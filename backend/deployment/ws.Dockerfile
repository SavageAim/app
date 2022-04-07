FROM python:3-slim

WORKDIR /savage-aim

COPY . .
RUN mv backend/settings_live.py backend/settings.py
RUN mv backend/urls_live.py backend/urls.py

# Install requirements
RUN pip3 install -r requirements.txt
RUN pip3 install daphne

# Set the gunicorn to run the wsgi file
EXPOSE 443
ENTRYPOINT daphne -b 0.0.0.0 -p 443 backend.asgi:application
