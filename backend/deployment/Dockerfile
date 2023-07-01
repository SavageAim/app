FROM python:3

WORKDIR /savage-aim

# Copy and install requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn


# Copy rest of files, and set up proper live file links
COPY . .
RUN mv backend/urls_live.py backend/urls.py && \
    mv backend/settings_live.py backend/settings.py

# Set the gunicorn to run the wsgi file
EXPOSE 443
ENTRYPOINT python3 manage.py migrate && python3 manage.py seed && gunicorn --bind=0.0.0.0:443 --access-logfile - --log-file - --log-level info --capture-output --enable-stdio-inheritance backend.wsgi
