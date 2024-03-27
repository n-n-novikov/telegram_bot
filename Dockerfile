FROM python:3.9-alpine
WORKDIR ~/Projects/lovebot
COPY loveBot.py comps.txt requirements.txt .
RUN pip install -r requirements.txt
CMD python loveBot.py
