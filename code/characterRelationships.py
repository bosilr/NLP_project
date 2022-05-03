import numpy as np
import pandas as pd
import os
import spacy
import nltk
from afinn import Afinn
import itertools
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import networkx as nx


def get_common_english_words(path):
    words = []
    with open(path) as f:
        for word in f.readlines():
            words.append(word.strip())

    return words


def read_text(path):
    with open(path) as f:
        text = f.read().replace('\r', ' ').replace('\n', ' ').replace("\'", "'")

    return text


def NER(s):
    named_entities = []
    accepted_labels = ['PERSON']
    entities = nlp(s).ents
    for e in entities:
        if e.label_ in accepted_labels:
            named_entities.append(str(e).lower().replace("'s", "").split(' '))

    return list(itertools.chain(*named_entities))


def get_named_entities(sentences):
    threshold = 0.0001
    named_entities = []
    named_entities_thresholded = []
    for s in sentences:
        named_entities += NER(s)

    named_entities = [ne for ne in named_entities if ne not in common_english_words]
    named_entities = Counter(named_entities)
    for ne in named_entities:
        if named_entities[ne] >= threshold * len(sentences):
            named_entities_thresholded.append(ne)

    return named_entities_thresholded


def get_main_characters(book, characters, number_of_characters):
    cv = CountVectorizer(vocabulary=characters, stop_words='english')
    freq = cv.fit_transform([book.lower()])
    freq = pd.DataFrame(freq.toarray(), columns=cv.get_feature_names())
    freq = freq.T
    freq = freq.sort_values(by=0, ascending=False)
    freq = freq[0:number_of_characters]

    characters = list(freq.index)
    return freq, characters


def get_mtx(sentences, main_characters):
    afinn = Afinn()
    score = [afinn.score(s) for s in sentences]
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


if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')
    common_english_words = get_common_english_words('../data/common_english_words.txt')

    book = read_text('../data/books/HungerGames/hungergames_1.txt')
    sentences = nltk.sent_tokenize(book)
    
    characters = get_named_entities(sentences)
    print(characters)

    freq, main_characters = get_main_characters(book, characters, number_of_characters=10)

    sentiment_mtx, cooccur_mtx = get_mtx(sentences, main_characters)

    # TODO: plotting

