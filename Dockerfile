FROM tiangolo/meinheld-gunicorn:python3.7

COPY $FOLDER/requirements.txt   /config/
RUN pip install --no-cache-dir -r /config/requirements.txt
COPY $FOLDER/code   /app
