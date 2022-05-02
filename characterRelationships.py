import numpy as np
import pandas as pd
import os
import spacy
import nltk
from afinn import Afinn
import itertools



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
    named_entities = []
    for s in sentences:
        named_entities += NER(s)

    

    return named_entities


if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')
    common_english_words = get_common_english_words('data/common_english_words.txt')
    # print(common_english_words)

    book = read_text('data/HungerGames/hungergames_1.txt')
    # print(book)
    sentences = nltk.sent_tokenize(book)
    
    characters = get_named_entities(sentences)
    print(characters)