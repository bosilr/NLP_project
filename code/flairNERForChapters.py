from nltk.tokenize import sent_tokenize
from tqdm import tqdm
from flair.models import SequenceTagger
from flair.data import Sentence
import operator
import json
import os

from preprocessing_util.preprocessing import readWholeBook, readBookByChapters, getChaptersInOrder


def read_text(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
        text = text.replace('\r', ' ').replace('\n', ' ')\
            .replace("’", "'").replace("\"", "").replace("”", "").replace("“", "")
    return text


def flair_NER(book):
    """
    flair_NER vrne seznam, v katerem so shranjene prepoznane identitete glede na posamezni stavek
    :param book: str
    :return: entity_dict (seznam slovarjev kot npr. [name, tag, start_pos, stop_pos, line_num. token_num])
    """

    # 00 Pretvori knjigo v stavke:
    sent = sent_tokenize(book)

    # 01 NER model
    entity_dict = []
    for line_num, line in enumerate(tqdm(sent)):

        # 01a Predict:
        sentence = Sentence(line)
        tagger.predict(sentence)

        # 01b Vmesni izpis (brez lokacije):
        #print(sentence.to_tagged_string())
        #print(sentence.get_spans('ner'))

        # 01c Ekstrakcija podatka iz stavka:
        for entity in sentence.get_spans('ner'):        # veliko različnih flair - nerov
            name = entity.text

            # str location
            # start_pos = entity.start_position    # št. str
            # stop_pos = entity.end_position      # št. str

            # token location
            tmp_flag = True
            for token in entity:
                if tmp_flag:
                    start_pos = token.idx -1
                    stop_pos = token.idx
                else:
                    stop_pos = token.idx
                tmp_flag = False

            tag = entity.get_label("ner").value             # tag = entity.tag
            conf_score = entity.get_label("ner").score      # conf_score = entity.score

            info_dict = {}
            info_dict["name"] = name
            info_dict["tag"] = tag
            info_dict["start_pos"] = start_pos
            info_dict["stop_pos"] = stop_pos
            info_dict["line_num"] = line_num

            entity_dict.append(info_dict)

    return entity_dict


def get_names_from_NER(entity_dict):
    """
    get_names_from_NER sprejme entity_dict in vrne urejen seznam terk ("ime", št_zaznano)
    :param entity_dict: dict (seznam dictov)
    :return: unique_names: list
    """
    unique_names = {}

    for entity in entity_dict:
        if entity["tag"] == "PER":
            if entity["name"] not in unique_names:
                unique_names[entity["name"]] = 1
            else:
                unique_names[entity["name"]] += 1
    unique_names = sorted(unique_names.items(), key=operator.itemgetter(1), reverse=True)

    return unique_names


def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')


if __name__ == "__main__":
    tagger = SequenceTagger.load('ner')

    data_path = "../data/books/ASongOfIceAndFire/AGOT/chapters/"
    results_path = "../results/books/ASongOfIceAndFire/AGOT/chapters"
    chapters = getChaptersInOrder(data_path)

    for chapter in chapters:
        text = read_text(data_path + chapter)

        entitiy_dict = flair_NER(text)
        unique_names = get_names_from_NER(entitiy_dict)

        chapter = chapter.replace(".txt", "")

        with safe_open_w("../results/books/ASongOfIceAndFire/AGOT/chapters/" + chapter + "_entity_dict") as f:
            json.dump(entitiy_dict, f)

        with safe_open_w("../results/books/ASongOfIceAndFire/AGOT/chapters/" + chapter + "_unique_names") as f:
            json.dump(unique_names, f)

    # whole book NER
    book = readWholeBook(data_path)
    entitiy_dict = flair_NER(book)
    unique_names = get_names_from_NER(entitiy_dict)

    with safe_open_w("../results/books/ASongOfIceAndFire/AGOT/entity_dict") as f:
        json.dump(entitiy_dict, f)

    with safe_open_w("../results/books/ASongOfIceAndFire/AGOT/unique_names") as f:
        json.dump(unique_names, f)




