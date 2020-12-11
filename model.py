from flask import Flask, request, render_template
import pandas as pd
import spacy

import numpy as np
from gensim.models import Word2Vec
from scipy.spatial import distance

nlp = spacy.load('en_core_web_lg')

app = Flask(__name__)


def model(word):
    df = df = pd.read_pickle("tweets_model.csv")
    model = Word2Vec.load("word2vec.model")   

    pp = ' '.join([token.text for token in nlp(word) if token.is_alpha and not (token.is_oov or token.is_stop)])
    lem = ' '.join([token.lemma_ if token.lemma_ != '-PRON-' else token.text for token in nlp(pp)])

    slp = pp.split()
    sll = lem.split()

    vec = sum([model.wv[word] for word in sll]) / len(sll)   

    dist = []
    for i in range(len(df)):
        dist.append((df["text"].iloc[i], distance.cosine(df["tweet_vlems"].iloc[i], vec)))
    
    dff = pd.DataFrame(dist)
    dff.rename(columns = {0 : 'tweet', 1 : 'distance'}, inplace = True)
    dff = dff.sort_values(by=['distance'], ascending=True).head(20)
    
    return dff



@app.route('/', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        
        word = request.form['word_to_analyse']
        result = model(word)

        return render_template('index.html', similar_tweets=[result.to_html(classes='data', header="true")], word=word)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')