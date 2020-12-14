import tarfile

import spacy

from flask import Flask, request, render_template

from similar_tweets import get_similar_tweets

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
    if request.method == 'POST':
        
        word = request.form['word_to_analyse']
        try:
            model = request.form['model']
        except:
            model = "w2v"
        
        result = get_similar_tweets(word, model, nlp)

        return render_template(template, similar_tweets=[result.to_html(classes='data', header="true")], word=word)
    else:
        return render_template(template)


if __name__ == '__main__':
    app.debug = True

    app.run(host='0.0.0.0')
