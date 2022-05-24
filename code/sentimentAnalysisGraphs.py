import os
import json
import numpy as np
from nltk.tokenize import sent_tokenize
import matplotlib.pyplot as plt
import networkx as nx
import operator


from preprocessing_util.utils import get_main_characters, replace_synonyms, readBookByChapters, readWholeBook, get_main_character_occurances_for_chapters, read_text
from sentimentAnalysis import vaderSentiment, afinnSentiment, textblobSentiment


def find_zero_indexes(matrix):
    result = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 0:
                result.append((i, j))
    return result


def get_edge_list_coocur(matrix, main_characters):
    edge_list = []
    triangle_lower = np.triu(np.ones([matrix.shape[0], matrix.shape[0]]))
    triangle_lower_zeros = find_zero_indexes(triangle_lower)

    normalized_mtx = matrix / np.max(np.abs(matrix))

    weight = np.log(2000 * normalized_mtx + 1) * 0.7
    color = np.log(2000 * normalized_mtx + 1)

    for (i, j) in triangle_lower_zeros:
        edge_list.append((main_characters[i], main_characters[j], {'weight': weight[(i, j)], 'color': color[(i, j)]}))

    return edge_list


def get_edge_list_sentiment(matrix, main_characters):
    edge_list = []
    triangle_lower = np.triu(np.ones([matrix.shape[0], matrix.shape[0]]))
    triangle_lower_zeros = find_zero_indexes(triangle_lower)

    normalized_mtx = matrix / np.max(np.abs(matrix))

    weight = np.log(np.abs(1000 * normalized_mtx) + 1) * 0.7
    color = 2000 * normalized_mtx

    for (i, j) in triangle_lower_zeros:
        edge_list.append((main_characters[i], main_characters[j], {'weight': weight[(i, j)], 'color': color[(i, j)]}))

    return edge_list


def plot_relationship_graph(main_characters_dict, matrix, type, save_file, title):
    main_characters = list(main_characters_dict.keys())
    label = {i: i for i in main_characters}

    main_characters_freq = list(main_characters_dict.values())
    normalized_main_characters_freq = np.array(main_characters_freq) / np.max(main_characters_freq)

    if type == 'sentiment':
        edge_list = get_edge_list_sentiment(matrix, main_characters)
    else:
        edge_list = get_edge_list_coocur(matrix, main_characters)

    fig = plt.figure(figsize=(20, 20))
    plt.title(title, fontsize=25)
    G = nx.Graph()
    G.add_nodes_from(main_characters)
    G.add_edges_from(edge_list)

    weights = [G[u][v]['weight'] for u, v in G.edges]
    colors = [G[u][v]['color'] for u, v in G.edges]

    if type == "sentiment":
        nx.draw(G, nx.circular_layout(G), node_color='#cad8fa', node_size=np.sqrt(normalized_main_characters_freq) * 4000,
                linewidths=10, font_size=35, labels=label, edge_color=colors, with_labels=True,
                width=weights, edge_vmin=-1000, edge_vmax=1000, edge_cmap=plt.cm.bwr_r)
    else:
        nx.draw(G, nx.circular_layout(G), node_color='#cad8fa', node_size=np.sqrt(normalized_main_characters_freq) * 4000, edge_cmap=plt.cm.Blues,
                linewidths=10, font_size=35, labels=label, edge_color=colors, with_labels=True, width=weights)

    # fig.set_facecolor('#e3e3e3')
    plt.savefig(save_file)
    plt.close(fig)


if __name__ == '__main__':
    all_chapters = 73
    start_chapter = 1

    """ 
    Here you can set parameters for the sentiment analysis
    :param number_of_chapters: how many chapters per analysis
    :param exclude: which entities to exclude from NER results
    :param number_of_characters: number of most common characters to plot
    """
    number_of_chapters = 8
    # 21 include Cersei, 27 incluide Viserys
    number_of_characters = 21
    exclude = ["Lannister", "Jory", "Hand", "Stark", "Mormont", "Grace"]

    # affin, vader, text
    ana_type = "vader"

    while start_chapter < all_chapters:
        end_chapter = min(73, start_chapter + number_of_chapters)

        # text = readBookByChapters("../results/books/ASongOfIceAndFire/AGOT/chapters_coref_text/", start_chapter, end_chapter)
        text = readBookByChapters("../data/books/ASongOfIceAndFire/AGOT/chapters/", start_chapter, end_chapter)

        text = replace_synonyms(text)
        sentences = sent_tokenize(text)

        # mc = get_main_characters("../results/books/ASongOfIceAndFire/AGOT/chapters_coref/", number_of_characters, exclude, chapters=True)
        mc = get_main_characters("../results/books/ASongOfIceAndFire/AGOT/unique_names", number_of_characters, exclude, chapters=False)

        print(mc)

        # main_characters_dict = get_main_character_occurances_for_chapters("../results/books/ASongOfIceAndFire/AGOT/chapters_coref/", mc, start_chapter, end_chapter)
        main_characters_dict = get_main_character_occurances_for_chapters("../results/books/ASongOfIceAndFire/AGOT/chapters/", mc, start_chapter, end_chapter)

        main_characters = list(main_characters_dict.keys())
        main_characters = list(map(str.lower, main_characters))

        # chose different sentiment analysis
        if ana_type == 'affin':
            sentiment_mtx, cooccurance_mtx = afinnSentiment(sentences, main_characters)
        elif ana_type == 'vader':
            sentiment_mtx, cooccurance_mtx = vaderSentiment(sentences, main_characters)
            sentiment_mtx = (sentiment_mtx / 4) * 5
        else:
            sentiment_mtx, cooccurance_mtx = textblobSentiment(sentences, main_characters)
            sentiment_mtx = sentiment_mtx * 5


        # save_file_sent = "../results/books/ASongOfIceAndFire/AGOT/sentiment/coref_first/"+ ana_type + "/sentiment_chapters_" + str(start_chapter) + "_" + str(end_chapter) + ".png"
        # save_file_coo = "../results/books/ASongOfIceAndFire/AGOT/sentiment/coref_first/" + ana_type + "/coocurance_chapters_" + str(start_chapter) + "_" + str(end_chapter) + ".png"
        save_file_sent = "../results/books/ASongOfIceAndFire/AGOT/sentiment/normal/" + ana_type + "/sentiment_chapters_" + str(start_chapter) + "_" + str(end_chapter) + ".png"
        save_file_coo = "../results/books/ASongOfIceAndFire/AGOT/sentiment/normal/" + ana_type + "/coocurance_chapters_" + str(start_chapter) + "_" + str(end_chapter) + ".png"

        title1 = "Relationship graph: chapters_" + str(start_chapter) + "_" + str(end_chapter - 1)
        title2 = "Cooccurrence graph: chapters_" + str(start_chapter) + "_" + str(end_chapter - 1)

        plot_relationship_graph(main_characters_dict, sentiment_mtx, "sentiment", save_file_sent, title1)
        plot_relationship_graph(main_characters_dict, cooccurance_mtx, "coocurance", save_file_coo, title2)

        start_chapter += number_of_chapters


###############################################################################################################

    # whole book sentiment analysis + plotting
    # book = readWholeBook("../results/books/ASongOfIceAndFire/AGOT/chapters_coref_text/")
    book = readWholeBook("../data/books/ASongOfIceAndFire/AGOT/chapters/")
    # book = read_text("../data/books/ASongOfIceAndFire/ASOS/AStormOfSwords")
    # print(book)
    book = replace_synonyms(book)
    sentences = sent_tokenize(book)

    # main_characters_dict = get_main_characters("../results/books/ASongOfIceAndFire/AGOT/chapters_coref/", number_of_characters, exclude, chapters=True)
    main_characters_dict = get_main_characters("../results/books/ASongOfIceAndFire/AGOT/unique_names", number_of_characters, exclude, chapters=False)
    print(main_characters_dict)

    main_characters = list(main_characters_dict.keys())
    main_characters = list(map(str.lower, main_characters))

    # chose different sentiment analysis
    if ana_type == 'affin':
        sentiment_mtx, cooccurance_mtx = afinnSentiment(sentences, main_characters)
    elif ana_type == 'vader':
        sentiment_mtx, cooccurance_mtx = vaderSentiment(sentences, main_characters)
        sentiment_mtx = (sentiment_mtx / 4) * 5
    else:
        sentiment_mtx, cooccurance_mtx = textblobSentiment(sentences, main_characters)
        sentiment_mtx = sentiment_mtx / 4

    # save_file_sent = "../results/books/ASongOfIceAndFire/AGOT/sentiment/coref_first/" + ana_type + "/sentiment_chapters_whole.png"
    # save_file_coo = "../results/books/ASongOfIceAndFire/AGOT/sentiment/coref_first/" + ana_type + "/coocurance_chapters_whole.png"
    save_file_sent = "../results/books/ASongOfIceAndFire/AGOT/sentiment/normal/" + ana_type + "/sentiment_chapters_whole.png"
    save_file_coo = "../results/books/ASongOfIceAndFire/AGOT/sentiment/normal/" + ana_type + "/coocurance_chapters_whole.png"

    title1 = "Relationship graph: AGOT whole book"
    title2 = "Cooccurrence graph: AGOT whole book"

    plot_relationship_graph(main_characters_dict, sentiment_mtx, "sentiment", save_file_sent, title1)
    plot_relationship_graph(main_characters_dict, cooccurance_mtx, "coocurance", save_file_coo, title2)

