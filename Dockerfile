FROM python:3.6

WORKDIR /app

ENV FLASK_APP = model.py

COPY requirements.txt .
COPY tweet_models.pkl /app/tweet_models.pkl
COPY w2v_on_lems.model /app/w2v_on_lems.model
COPY d2v_on_lems.model /app/d2v_on_lems.model
# COPY ft_on_lems.tar.xz /app/ft_on_lems.tar.xz

RUN pip install -r requirements.txt
RUN pip install -U gensim
RUN python -m spacy download en_core_web_lg

COPY . .

EXPOSE 5000
EXPOSE 6666

CMD ["python", "model.py"]
