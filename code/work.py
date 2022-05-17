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


def read_text(path):
    with open(path) as f:
        text = f.read().replace('\r', ' ').replace('\n', ' ').replace("\'", "'")

    return text


if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')

    book = read_text('../data/books/ASongOfIceAndFire/ASongOfIceAndFire.txt')

    print()

    sentences = nltk.sent_tokenize(book)