import pandas as pd
import spacy

nlp = spacy.load("en_core_web_lg")

df = pd.read_csv("ppp_tweets.csv")

preproc_tweets = []

for tweet in df["tweet"]:
    doc = nlp(tweet)

    words = [token.text for token in doc if token.is_alpha and not (token.is_oov or token.is_stop)]
    pp_tweet = ' '.join(words)

    preproc_tweets.append(pp_tweet)

df["tweet_pp"] = pd.Series(preproc_tweets)
df = df[~df["tweet_pp"].str.len().eq(0)]
df = df.reset_index(drop=True)

lemma_tweets = []

for tweet in df["tweet_pp"]:
    doc = nlp(tweet)

    lemmas = [token.lemma_ if token.lemma_ != '-PRON-' else token.text for token in doc]
    lemma_tweet = ' '.join(lemmas)

    lemma_tweets.append(lemma_tweet)

df["tweet_lems"] = pd.Series(lemma_tweets)

df["tweet_pp_list"] = ''
df["tweet_lems_list"] = ''

for i in range(len(df)):
    df["tweet_pp_list"].iloc[i] = df["tweet_pp"].iloc[i].split()
    df["tweet_lems_list"].iloc[i] = df["tweet_lems"].iloc[i].split()

df.to_pickle("pp_tweets.pkl")
