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

import textacy
from nltk.stem import WordNetLemmatizer



def read_text(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
        text = text.replace('\r', ' ').replace('\n', ' ')\
            .replace("’", "'").replace("\"", "").replace("”", "").replace("“", "")
    return text


def NER(s):
    # s = lemmatizer.lemmatize(s)
    named_entities = []
    accepted_labels = ['PERSON', 'ORG']
    entities = nlp(s).ents
    for e in entities:
        if e.label_ in accepted_labels:
            named_entities.append(str(e).lower().replace("'s", "").split(' '))

            # named_entities.append(str(e).lower().replace("'s", ""))

    return list(itertools.chain(*named_entities))


def get_named_entities(sentences):
    named_entities = []
    named_entities_thresholded = []
    for s in sentences:
        named_entities += NER(s)

    named_entities = Counter(named_entities)

    return named_entities


if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')
    lemmatizer = WordNetLemmatizer()

    book = read_text('../data/books/ASongOfIceAndFire/AGOT/chapters/Bran_1_1')
    sentences = nltk.sent_tokenize(book)

    characters = get_named_entities(sentences)
    print(characters)

    # lemmatized_words = [lemmatizer.lemmatize(word) for word in words]


