FROM luckydonald/telegram-bot:python3.6-stretch

COPY $FOLDER/requirements.txt   /config/
RUN pip install --no-cache-dir -r /config/requirements.txt
COPY $FOLDER/code   /app
