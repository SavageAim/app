FROM python:3

WORKDIR /savage-aim

COPY . .
RUN mv backend/settings_live.py backend/settings.py
RUN mv backend/urls_live.py backend/urls.py

# Install requirements
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

# Set the gunicorn to run the wsgi file
EXPOSE 443
ENTRYPOINT python3 manage.py migrate && python3 manage.py seed && gunicorn --bind=0.0.0.0:443 --access-logfile - --log-file - --log-level info --capture-output --enable-stdio-inheritance backend.wsgi
