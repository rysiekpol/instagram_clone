FROM python:3.10.6

WORKDIR /code

COPY requirements.txt requirements.txt
COPY app app
COPY migrations migrations
COPY instagram.py config.py boot.sh ./    

RUN python -m venv venv && \
    venv/bin/pip install -r requirements.txt && \
    chmod +x boot.sh

ENV FLASK_APP instagram.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]