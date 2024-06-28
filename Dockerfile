FROM python:3.10-alpine
WORKDIR ~/Projects/lovebot
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY loveBot.py comps.txt .
CMD python loveBot.py
