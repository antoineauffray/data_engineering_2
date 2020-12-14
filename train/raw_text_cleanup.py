import pandas as pd

df = pd.read_csv("tweets.csv", index_col=0)

# Let's drop duplicates
df.drop_duplicates(inplace=True)
df.drop(columns=["id", "link", "retweet", "author"], inplace=True)
df.reset_index(drop=True, inplace=True)

df["tweet"] = df["text"].copy()

# The following is done because sometimes links or pictures urls are actually
# directly following text, without any form of space, leading to text being
# deleted at preprocessing time
df["tweet"] = df["tweet"].str.replace("pic.twitter.com/", " pic.twitter.com/")
df["tweet"] = df["tweet"].str.replace("http://", " http://")
df["tweet"] = df["tweet"].str.replace("https://", " https://")

# Let's take care of the hashtags
df["tweet"] = df["tweet"].str.replace('#MAGA', 'make america great again', case=False)

# Since hashtags are often camel case, we will split them in to words
def camel_case_split(string):
    sstr = ['']
    i=0
    j=0

    while i < len(string):

        if string[i].isupper():
            while (i+1) < len(string) and string[i+1].isupper():
                sstr[j] += string[i]
                i += 1

            if (i+1) >= len(string):
                sstr[j] += string[i]
                break

            j += 1
            sstr.append('')

            sstr[j] += string[i]
            i += 1

            while i < len(string) and string[i].islower():
                sstr[j] += string[i]
                i += 1
            j += 1
            sstr.append('')

        elif i < len(string) and string[i].isdigit():
            while i < len(string) and string[i].isdigit():
                sstr[j] += string[i]
                i += 1
            j += 1
            sstr.append('')

        elif i < len(string) and string[i].islower():
            while i < len(string) and string[i].islower():
                sstr[j] += string[i]
                i += 1
            j += 1
            sstr.append('')

        else:
            i += 1

    new_str = ' '.join(sstr)

    return new_str


for t in df["tweet"]:
    if '#' in t:
        i = 0
        tl = t.split()
        while i < len(tl):
            if tl[i].startswith('#'):
                sp = camel_case_split(tl[i][1:])
                tl.pop(i)
                tl[i:i] = sp
            i += 1
        t = ' '.join(tl)

df["tweet"] = df["tweet"].str.replace('#', '')

df["tweet"] = df["tweet"].str.lower()

df.to_csv("ppp_tweets.csv", index=False)
