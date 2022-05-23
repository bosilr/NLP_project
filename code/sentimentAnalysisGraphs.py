import os
import json
import numpy as np
from nltk.tokenize import sent_tokenize
import matplotlib.pyplot as plt
import networkx as nx


from preprocessing_util.utils import get_main_characters, replace_synonyms, readBookByChapters, readWholeBook, get_main_character_occurances_for_chapters
from sentimentAnalysis import vaderSentiment, afinnSentiment, textblobSentiment


def find_zero_indexes(matrix):
    result = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 0:
                result.append((i, j))
    return result


def get_edge_list(matrix, main_characters, type):
    edge_list = []
    triangle_lower = np.triu(np.ones([matrix.shape[0], matrix.shape[0]]))
    triangle_lower_zeros = find_zero_indexes(triangle_lower)

    normalized_mtx = matrix / np.max(np.abs(matrix))

    return_weights, return_colors, weights, colors = [], [], None, None
    # can fiddle with parameters
    if type == 'sentiment':
        weight = np.log(np.abs(1000 * normalized_mtx) + 1) * 0.7
        color = 2000 * normalized_mtx
    else:
        weight = np.log(2000 * normalized_mtx + 1) * 0.7
        color = np.log(2000 * normalized_mtx + 1)

    for (i, j) in triangle_lower_zeros:
        edge_list.append((main_characters[i], main_characters[j], {'weight': weight[(i, j)], 'color': color[(i, j)]}))

    return edge_list



def plot_relationship_graph(main_characters_dict, matrix, type, path):
    main_characters = list(main_characters_dict.keys())
    label = {i: i for i in main_characters}

    main_characters_freq = list(main_characters_dict.values())
    normalized_main_characters_freq = np.array(main_characters_freq) / np.max(main_characters_freq)

    edge_list = get_edge_list(matrix, main_characters, type)

    fig = plt.figure(figsize=(20, 20))
    G = nx.Graph()
    G.add_nodes_from(main_characters)
    G.add_edges_from(edge_list)

    weights = [G[u][v]['weight'] for u, v in G.edges]
    colors = [G[u][v]['color'] for u, v in G.edges]


    print(edge_list)

    if type == "sentiment":
        nx.draw(G, nx.circular_layout(G), node_color='#cad8fa', node_size=np.sqrt(normalized_main_characters_freq) * 4000,
                linewidths=10, font_size=35, labels=label, edge_color=colors, with_labels=True,
                width=weights, edge_vmin=-1000, edge_vmax=1000, edge_cmap=plt.cm.bwr_r)
        # nx.draw(G, nx.circular_layout(G), node_color='#b0f5f3', node_size=np.sqrt(normalized_main_characters_freq) * 4000,
        #         linewidths=10, font_size=35, labels=label, edge_color=colors, with_labels=True,
        #         width=weights)
    else:
        nx.draw(G, nx.circular_layout(G), node_color='#b0f5f3', node_size=np.sqrt(normalized_main_characters_freq) * 4000, edge_cmap=plt.cm.Blues,
                linewidths=10, font_size=35, labels=label, edge_color=colors, with_labels=True, width=weights)

    # fig.set_facecolor('#e3e3e3')
    # plt.show()
    plt.savefig('test.png')




if __name__ == '__main__':
    all_chapters = 73
    start_chapter = 1

    """ 
    Here you can set parameters for the sentiment analysis
    :param number_of_chapters: how many chapters per analysis
    :param exclude: which entities to exclude from NER results
    :param number_of_characters: number of most common characters to plot
    """
    number_of_chapters = 20
    number_of_characters = 21
    exclude = ["Lannister", "Jory", "Hand", "Stark", "Mormont"]

    while start_chapter < all_chapters:
        end_chapter = min(73, start_chapter + number_of_chapters)

        text = readBookByChapters("../data/books/ASongOfIceAndFire/AGOT/chapters/", start_chapter, end_chapter)
        text = replace_synonyms(text)
        sentences = sent_tokenize(text)

        # 27 incluide Viserys
        mc = get_main_characters("../results/books/ASongOfIceAndFire/AGOT/unique_names", number_of_characters, exclude)
        main_characters_dict = get_main_character_occurances_for_chapters("../results/books/ASongOfIceAndFire/AGOT/chapters/", mc, start_chapter, end_chapter)
        print(main_characters_dict)
        main_characters = list(main_characters_dict.keys())
        main_characters = list(map(str.lower, main_characters))

        # chose different sentiment analysis
        sentiment_mtx, cooccurance_mtx = afinnSentiment(sentences, main_characters)

        title =
        plot_relationship_graph(main_characters_dict, sentiment_mtx, "sentiment", "../results/books/ASongOfIceAndFire/AGOT/")
        # plot_relationship_graph(main_characters_dict, cooccurance_mtx, "coocurance")

        print(main_characters)
        print(main_characters_dict.values())
        # plot_graph(main_characters, list(main_characters_dict.values()), sentiment_mtx, "test", "sentiment")
        # plot_graph(main_characters, list(main_characters_dict.values()), cooccurance_mtx, "test", "co-occurrence")

        break

    # # whole book sentiment analysis + plotting
    # book = readWholeBook("../data/books/ASongOfIceAndFire/AGOT/chapters/")
    # sentences = sent_tokenize(book)
    #
    # main_characters_dict = get_main_characters("../results/books/ASongOfIceAndFire/AGOT/unique_names", 27, exclude)
    # main_characters = list(main_characters_dict.keys())
    # main_characters = list(map(str.lower, main_characters))
    #
    # sentiment_mtx, cooccurance_mtx = afinnSentiment(sentences, main_characters)
    #
    # plot_relationship_graph(main_characters_dict, sentiment_mtx, None, None, type="sentiment")
    # plot_relationship_graph(main_characters_dict, cooccurance_mtx, None, None, type="coocurance")
