import pandas as pd

from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from gensim.models.fasttext import FastText

df = pd.read_pickle("pp_tweets.pkl")

# Creating Word2Vec model on lemmas list
w2v_model = Word2Vec(min_count=1, size=100, window=2, negative=2, workers=6)
w2v_model.build_vocab(df["tweet_lems_list"])
w2v_model.train(df["tweet_lems_list"], total_examples=w2v_model.corpus_count, epochs=20)

w2v_model.save("../w2v_on_lems.model")

w2v_vectors = []

for row in df["tweet_lems_list"]:
    w2v_vectors.append(sum([w2v_model.wv[word] for word in row]) / len(row))

df["tweet_lems_w2v"] = w2v_vectors

# Function to tag documents
def tag_documents(serie):
    tagged = []

    for i in range(len(serie)):
        tagged.append(TaggedDocument(serie[i], [i]))

    return tagged


# Creating Doc2Vec model on lemmas list
s = tag_documents(df["tweet_lems_list"])

d2v_model = Doc2Vec(min_count=1, vector_size=100, window=3, negative=3, workers=6, epochs=50)
d2v_model.build_vocab(s)
d2v_model.train(s, total_examples=d2v_model.corpus_count, epochs=d2v_model.epochs)

d2v_model.save("../d2v_on_lems.model")

vectors = []

for i in range(len(df)):
    vectors.append(d2v_model.docvecs[i])

df["tweet_lems_d2v"] = vectors


# Creating FastText model on lemmas list
ft_model = FastText(min_count=1, size=100, window=3, negative=3, workers=6, iter=50, min_n=1, max_n=9)
ft_model.build_vocab(df["tweet_lems_list"])
ft_model.train(df["tweet_lems_list"], epochs=ft_model.epochs, total_examples=ft_model.corpus_count)

ft_model.save("../ft_on_lems.model")

vectors = []

for row in df["tweet_lems_list"]:
    vectors.append(sum([ft_model.wv[word] for word in row]) / len(row))

df["tweet_lems_ft"] = vectors

df.to_pickle("../tweet_models_lems.pkl")
