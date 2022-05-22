import os
import json
import numpy as np
from nltk.tokenize import sent_tokenize


from preprocessing_util.utils import get_main_characters, replace_synonyms, readBookByChapters
from sentimentAnalysis import vaderSentiment, afinnSentiment, textblobSentiment


if __name__ == '__main__':
    all_chapters = 73
    start_chapter = 1

    while start_chapter < all_chapters:
        end_chapter = min(73, start_chapter + 10)

        text = readBookByChapters("../data/books/ASongOfIceAndFire/AGOT/chapters/", start_chapter, end_chapter)
        text = replace_synonyms(text)
        sentences = sent_tokenize(text)

        main_characters = get_main_characters("../results/books/ASongOfIceAndFire/AGOT/unique_names", 27, ["Lannister", "Jory", "Hand", "Stark", "Mormont"])
        print(main_characters)

        sentiment_mtx, cooccurance_mtx = afinnSentiment(sentences, main_characters)
        print(sentiment_mtx)
        print("-----------")
        print(cooccurance_mtx)

        break
