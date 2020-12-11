FROM python:3.6

WORKDIR /app

ENV FLASK_APP = model.py

COPY requirements.txt .
COPY tweets_model.csv /app/tweets_model.csv
COPY word2vec.model /app/word2vec.model

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg

COPY . .

EXPOSE 5000

CMD ["python", "model.py"]