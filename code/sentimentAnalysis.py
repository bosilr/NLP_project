from afinn import Afinn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from textblob import TextBlob


# -: enemy ; +: friendly

# -4 -> 4
def vaderSentiment(sentences, main_characters):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = [sid_obj.polarity_scores(sentence) for sentence in sentences]
    score = [sent['compound'] for sent in sentiment_dict]
    alignment = np.sum(score) / len(np.nonzero(score)[0]) * (-2)

    nc = CountVectorizer(vocabulary=main_characters, binary=True)
    freq = nc.fit_transform(sentences).toarray()

    sentiment_mtx = np.dot(freq.T, (freq.T * score).T)
    cooccur_mtx = np.dot(freq.T, freq)

    sentiment_mtx += alignment * cooccur_mtx
    sentiment_mtx, cooccur_mtx = np.tril(sentiment_mtx), np.tril(cooccur_mtx)

    cooccur_mtx[[range(cooccur_mtx.shape[0])], [range(cooccur_mtx.shape[0])]] = 0
    sentiment_mtx[[range(sentiment_mtx.shape[0])], [range(sentiment_mtx.shape[0])]] = 0

    return sentiment_mtx, cooccur_mtx


# -6 -> 6
def afinnSentiment(sentences, main_characters):
    afinn = Afinn()
    score = [afinn.score(s) for s in sentences]
    alignment = np.sum(score) / len(np.nonzero(score)[0]) * (-2)

    nc = CountVectorizer(vocabulary=main_characters, binary=True)
    freq = nc.fit_transform(sentences).toarray()

    sentiment_mtx = np.dot(freq.T, (freq.T * score).T)
    cooccur_mtx = np.dot(freq.T, freq)

    sentiment_mtx += alignment * cooccur_mtx
    sentiment_mtx, cooccur_mtx = np.tril(sentiment_mtx), np.tril(cooccur_mtx)

    np.fill_diagonal(cooccur_mtx, 0)
    np.fill_diagonal(sentiment_mtx, 0)
    # cooccur_mtx[[range(cooccur_mtx.shape[0])], [range(cooccur_mtx.shape[0])]] = 0
    # sentiment_mtx[[range(sentiment_mtx.shape[0])], [range(sentiment_mtx.shape[0])]] = 0

    return sentiment_mtx, cooccur_mtx


# -1 -> 1
def textblobSentiment(sentences, main_characters):
    sentiment_dict = [TextBlob(sentence) for sentence in sentences]
    score = [sent.sentiment.polarity for sent in sentiment_dict]
    alignment = np.sum(score) / len(np.nonzero(score)[0]) * (-2)

    nc = CountVectorizer(vocabulary=main_characters, binary=True)
    freq = nc.fit_transform(sentences).toarray()

    sentiment_mtx = np.dot(freq.T, (freq.T * score).T)
    cooccur_mtx = np.dot(freq.T, freq)

    sentiment_mtx += alignment * cooccur_mtx
    sentiment_mtx, cooccur_mtx = np.tril(sentiment_mtx), np.tril(cooccur_mtx)

    cooccur_mtx[[range(cooccur_mtx.shape[0])], [range(cooccur_mtx.shape[0])]] = 0
    sentiment_mtx[[range(sentiment_mtx.shape[0])], [range(sentiment_mtx.shape[0])]] = 0

    return sentiment_mtx, cooccur_mtx