import numpy as np
import pandas as pd
import os
import spacy
nlp_basic = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_md')
nlp_basic.max_length = 2000000
nlp_basic.disable_pipes("ner", "tagger", "parser")
nlp_basic.add_pipe('sentencizer')

def get_touples(text):
    doc = nlp_basic(text)
    name_dict = {}
    for sentence in doc.sents:
        sentence = sentence.text
        sent = nlp(sentence)
        persons = set([per for per in sent.ents if per.ent_id_ == "PERSON"])
        if len(persons) == 2:
            if persons in name_dict.keys():
                name_dict[persons].append(sentence)
            else:
                name_dict[persons] = [sentence]

    return name_dict


if __name__ == "__main__":
    text = open("../data/books/ASongOfIceAndFire/GoT1.txt", encoding="utf8").read()
    dict = get_touples(text)
    print(len(dict))
