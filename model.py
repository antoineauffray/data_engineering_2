import sys
import tarfile
import random
import spacy
import time

from flask import Flask, request, render_template

from similar_tweets import get_similar_tweets

from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary

REQUESTS = Counter('flask_app_calls_total', 'Number of user requests')
EXCEPTIONS = Counter('flask_app_exceptions_total', 'Number of exceptions trigger by the app')
INPROGRESS = Gauge('flask_app_inprogress', 'Number of requests in progress')
LAST = Gauge('flask_app_last_time_seconds','The last time our app was called')
LATENCY = Summary('lask_app_latency_seconds', 'The time needed for the request')

nlp = spacy.load('en_core_web_lg')

try:
    template = "index.html"

    with tarfile.open("ft_on_lems.tar.xz", "r:xz") as tar:
        tar.extractall()
except:
    template = "index_bis.html"

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def predict():
    LAST.set(time.time())
    REQUESTS.inc()
    start = time.time()
    with EXCEPTIONS.count_exceptions():
            if random.random() < 0.2:
                raise Exception

    INPROGRESS.inc()
    if request.method == 'POST':
        word = request.form['word_to_analyse']
        
        try:
            model = request.form['model']
        except:
            model = 'w2v'

        if word != "":
            result = get_similar_tweets(word, model, nlp)
            
            INPROGRESS.dec()
            LATENCY.observe(time.time() - start)
            return render_template(template, similar_tweets=[result.to_html(classes='data', header="true")], word=word)
    INPROGRESS.dec()    
    return render_template(template)


if __name__ == '__main__':
    start_http_server(8010)
    app.run(host='0.0.0.0')
