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
    threshold = 0.0005
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

def matrix_to_edge_list(matrix, main_characters, mode):
    edge_list = []
    shape = matrix.shape[0]
    lower_tri_loc = list(zip(*np.where(np.triu(np.ones([shape, shape])) == 0)))
    normalized_matrix = matrix / np.max(np.abs(matrix))
    if mode == 'co-occurrence':
        weight = np.log(2000 * normalized_matrix + 1) * 0.7
        color = np.log(2000 * normalized_matrix + 1)
    if mode == 'sentiment':
        weight = np.log(np.abs(1000 * normalized_matrix) + 1) * 0.7
        color = 2000 * normalized_matrix
    for i in lower_tri_loc:
        edge_list.append((main_characters[i[0]], main_characters[i[1]], {'weight': weight[i], 'color': color[i]}))

    return edge_list


def plotGraph(edge_list, nor_freq, main_characters, name):
    plt.figure(figsize=(20, 20))
    G = nx.Graph()
    G.add_nodes_from(main_characters)
    G.add_edges_from(edge_list)

    weights = [G[u][v]['weight'] for u, v in G.edges]
    colors = [G[u][v]['color'] for u, v in G.edges]

    label = {i: i for i in main_characters}
    if name == 'Sentiment':
        nx.draw(G, nx.circular_layout(G), node_color='#A0CBE2', node_size=np.sqrt(nor_freq) * 4000,
                linewidths=10, font_size=35, labels=label, edge_color=colors, with_labels=True,
                width=weights, edge_vmin=-1000, edge_vmax=1000)
    else:
        nx.draw(G, nx.circular_layout(G), node_color='#A0CBE2', node_size=np.sqrt(nor_freq) * 4000, edge_cmap=plt.cm.Blues,
                linewidths=10, font_size=35, labels=label, edge_color=colors, with_labels=True, width=weights)

    plt.savefig(name+'.png')


if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')
    common_english_words = get_common_english_words('../data/common_english_words.txt')

    book = read_text('../data/books/ASongOfIceAndFire/AGameOfThrones.txt')
    sentences = nltk.sent_tokenize(book)
    
    characters = get_named_entities(sentences)
    print(characters)

    freq, main_characters = get_main_characters(book, characters, number_of_characters=25)

    sentiment_mtx, cooccur_mtx = get_mtx(sentences, main_characters)

    # TODO: plotting
    # plotting
    edge_list_sentiment = matrix_to_edge_list(sentiment_mtx, main_characters, mode='co-occurrence')
    edge_list_cooccur = matrix_to_edge_list(cooccur_mtx, main_characters, mode='sentiment')
    nor_freq = np.array(freq) / np.max(freq)

    plotGraph(edge_list_sentiment, nor_freq, main_characters, name='Sentiment')
    plotGraph(edge_list_cooccur, nor_freq, main_characters, name='Coocur')
