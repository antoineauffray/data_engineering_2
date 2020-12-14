from scipy.spatial import distance

from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec
from gensim.models.fasttext import FastText

def get_similar_tweets(sentence, model, nlp):
    pp = ' '.join([token.text for token in nlp(sentence) if token.is_alpha and not (token.is_stop or token.is_oov)])
    lem = ' '.join([token.lemma_ if token.lemma_ != '-PRON-' else token.text for token in nlp(pp)])

    sll = lem.split()

    dist = []

    df = pd.read_pickle("tweet_models.pkl")

    if model == "w2v":
        w2v_model = Word2Vec.load("w2v_on_lems.model")
        vec = sum([w2v_model.wv[word] for word in sll]) / len(sll)

        for i in range(len(df)):
            dist.append((df["tweet"].iloc[i], distance.cosine(df["tweet_lems_w2v"].iloc[i], vec)))

    if model == "d2v":
        d2v_model = Doc2Vec.load("d2v_on_lems.model")
        vec = d2v_model.infer_vector(sll)

        for i in range(len(df)):
             dist.append((df["tweet"].iloc[i], distance.cosine(df["tweet_lems_d2v"].iloc[i], vec)))
             
    if model == "ft":
        ft_model = FastText.load("ft_on_lems.model")
        vec = sum([ft_model.wv[word] for word in sll]) / len(sll)
        
        for i in range(len(df)):
            dist.append((df["tweet"].iloc[i], distance.cosine(df["tweet_lems_ft"].iloc[i], vec)))
        
        
    dff = pd.DataFrame(dist)
    dff.rename(columns = {0 : 'tweet', 1 : 'distance'}, inplace = True)
    dff = dff.sort_values(by=['distance'], ascending=True).head(20)

    return dff
