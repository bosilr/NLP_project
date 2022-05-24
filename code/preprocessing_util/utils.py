import os
import json
import natsort
import operator
import itertools


def get_character_synonyms_dict():
    return {"Jon": ["Jon Snow", "Snow"],
            "Ned": ["Eddard Stark", "Lord Eddard", "Ned Stark", "Lord of Winterfell", "Eddard"],
            "Lyanna": ["Lyanna Stark"],
            "Benjen": ["Benjen Stark"],
            "Rickon": ["Rickon Stark"],
            "Tyrion": ["Tyrion Lannister", "Tyrion the Imp"],
            "Arya": ["Arya Stark"],
            "Bran": ["Bran Stark"],
            "Catelyn": ["Catelyn Tully Stark", "Catelyn Stark", "Cat", "Catelyn Tully", "Lady Catelyn"],
            "Daenerys": ["Dany", "Daenerys Targaryen", "Khaleesi", "Daenerys Stormborn"],
            "Viserys": ["Viserys Targaryen"],
            "Sansa": ["Sansa Stark", "Lady Sansa"],
            "Robb": ["Robb Stark", "Robb the Lord", "Robb ...", "Lord Robb"],
            "Robert": ["Robert Baratheon", "Robert of the House Baratheon"],
            "Stannis": ["Stannis Baratheon", "Lord Stannis"],
            "Renly": ["Renly Baratheon", "Lord Renly"],
            "Joffrey": ["Joffrey Baratheon"],
            "Myrcella": ["Myrcella Baratheon"],
            "Littlefinger": ["Lord Petyr Baelish", "Petyr Baelish", "Lord Baelish", "Petyr"],
            "Jorah": ["Ser Jorah Mormont", "Ser Jorah", "Jorah Mormont"],
            "Bronn": [],
            "Luwin": ["Maester Luwin"],
            "Rodrik": ["Ser Rodrik"],
            "Drogo": ["Khal Drogo"],
            "Jaime": ["Jaime Lannister", "Kingslayer"],
            "Varys": ["the Spider"],
            "Aemon": ["Maester Aemon"],
            "Cersei": ["Cersei Lannister"],
            "Tywin": ["Lord Tywin", "Tywin Lannister"],
            "Lysa": ["Lysa Arryn", "Lady Lysa"],
            "Sam": ["Samwell Tarly", "Sam Tarly", "Samwell"],
            "Illyrio": ["Illyrio Mopatis", "Magister Illyrio"],
            "Barristan": ["Ser Barristan the Bold", "Ser Barristan Selmy", "Ser Barristan", "Barristan Selmy"],
            "Theon": ["Theon Greyjoy"],
            "Pycelle": ["Grand Maester Pycelle", "Maester Pycelle"],
            "Hound": ["Sandor Clegane", "Sandor", "Ser Sandor"],
            "Syrio": ["Syrio Forel"],
            "Mountain": ["Ser Gregor", "Gregor Clegane", "Ser Gregor the Mountain", "Gregor"],
            "Loras": ["Ser Loras Tyrell", "Ser Loras", "Loras Tyrell", "Knight of Flowers",],
            "Walder": ["Lord Walder"],
            "Brynden": ["Ser Brynden Tully", "Blackfish", "Ser Brynden", "Brynden Tully", "Brynden Blackfish", "Uncle Brynden"],
            "Elia": ["Elia Martell"],
            "Mance": ["Mance Rayder"],
            "Oberyn": ["Prince Oberyn", "Oberyn Martell", "The Viper", "Viper"],
            "Qhorin": ["Qhorin Halfhand", "Halfhand"],
            "Fill1": ["Robert Arryn"],
            "Fill2": ["Jon Arryn"]}


def renameFiles(path):
    for file in os.listdir("../../data/books/ASongOfIceAndFire/AGOT/chapters"):
        split_name = file.split("_")
        src = path + file
        dest = path + split_name[2].replace(".txt", "") + "_" + split_name[0] + "_" + split_name[1] + ".txt"
        # dest = path + split_name[1] + "_" + split_name[2].replace(".txt", "") + "_" + split_name[0] + ".txt"

        os.rename(src, dest)


def read_text_og(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
        # text = text.replace('\r', ' ').replace('\n', ' ')\
        #     .replace("’", "'").replace("\"", "").replace("”", "").replace("“", "")
    return text


def read_text(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
        text = text.replace('\r', ' ').replace('\n', ' ')\
            .replace("’", "'").replace("\"", "").replace("”", "").replace("“", "")
    return text


def getChaptersInOrder(path):
    chapters = os.listdir(path)
    return natsort.natsorted(chapters)


def readWholeBook(path):
    chapter_lists = getChaptersInOrder(path)

    book = ""
    for chapter in chapter_lists:
        if "Appendix" not in chapter:
            book += read_text_og(path + chapter)

    book = book.replace('\r', ' ').replace('\n', ' ') \
        .replace("’", "'").replace("\"", "").replace("”", "").replace("“", "")

    return book


def readBookByChapters(path, from_chapter, to_chapter):
    """
    :param path: path of chapter location
    :param from_chapter: index of starting chapter (AGOT: min: 0, max: 74)   - 0 is prolog chapter
    :param to_chapter: index of ending chapter +1 (AGOT: min: 0, max: 74)    - 73 (73+1 = 74) is appendix
    :return: book text of selected chapters
    """
    chapter_lists = getChaptersInOrder(path)

    book = ""
    for i in range(from_chapter, to_chapter):
        book += read_text_og(path + chapter_lists[i])

    book = book.replace('\r', ' ').replace('\n', ' ') \
        .replace("’", "'").replace("\"", "").replace("”", "").replace("“", "")

    return book


def safe_open_w(path):
    """
    Open "path" for writing, creating any parent directories as needed.

    :example:     # with safe_open_w("../../results/books/ASongOfIceAndFire/AGOT/chapters/bran/test") as f:
                  #     json.dump(entitiy_dict, f)
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')


def get_character_occurances(path):
    """
    :param path: path to NER results
    :return: dictionary of characters order in the number of mentions in text
    """
    characters_dict = {}

    f = open(path)
    unique_names = json.load(f)
    f.close()

    synonyms = get_character_synonyms_dict()

    for name in unique_names:
        add_to_name = name[0]
        for true_name in synonyms:
            if name[0] in synonyms[true_name]:
                add_to_name = true_name

        if add_to_name not in characters_dict:
            characters_dict[add_to_name] = name[1]
        else:
            characters_dict[add_to_name] += name[1]

    return sorted(characters_dict.items(), key=operator.itemgetter(1), reverse=True)


def get_character_occurances2(path, form_chapter, to_chapter, to_print=False):
    characters_dict = {}

    NER_chapter_results = getChaptersInOrder(path)
    NER_chapter_results = [r for r in NER_chapter_results if "entity_dict" not in r]

    for i in range(form_chapter, to_chapter):
        if to_print:
            print(NER_chapter_results[i])
        f = open(path + NER_chapter_results[i])
        unique_names = json.load(f)
        f.close()

        synonyms = get_character_synonyms_dict()

        for name in unique_names:
            add_to_name = name[0]
            for true_name in synonyms:
                if name[0] in synonyms[true_name]:
                    add_to_name = true_name

            if add_to_name not in characters_dict:
                characters_dict[add_to_name] = name[1]
            else:
                characters_dict[add_to_name] += name[1]

    return sorted(characters_dict.items(), key=operator.itemgetter(1), reverse=True)


def get_main_character_occurances_for_chapters(path, main_characters, from_chapter, to_chapter):
    """
    :param path: path of all NER results
    :param from_chapter: starting chapter
    :param to_chapter: ending_chapter
    :return: dictionary of characters order in the number of mentions in text between from_chapter and to_chapter
    """
    characters_dict = {}
    for c in main_characters.keys():
        characters_dict[c] = 0

    NER_chapter_results = getChaptersInOrder(path)
    NER_chapter_results = [r for r in NER_chapter_results if "entity_dict" not in r]

    for i in range(from_chapter, to_chapter):
        f = open(path + NER_chapter_results[i])
        unique_names = json.load(f)
        f.close()

        synonyms = get_character_synonyms_dict()

        for name in unique_names:
            add_to_name = name[0]
            for true_name in synonyms:
                if name[0] in synonyms[true_name]:
                    add_to_name = true_name

            if add_to_name in characters_dict.keys():
                characters_dict[add_to_name] += name[1]

    return characters_dict


def get_main_characters(path, max_number_of_characters, excluded_characters, chapters):
    main_characters = {}
    if chapters:
        characters = get_character_occurances2(path, 1, 73)
    else:
        characters = get_character_occurances(path)

    for char in characters:
        if char[0] not in excluded_characters:
            main_characters[char[0]] = char[1]

        if len(main_characters) == max_number_of_characters:
            return main_characters

    return main_characters


def replace_synonyms(text):
    synonyms = get_character_synonyms_dict()

    for name in synonyms:
        for syn in synonyms[name]:
            text = text.replace(syn, name)
            # print(text)

    return text


if __name__ == "__main__":
    # renameFiles("../data/books/ASongOfIceAndFire/AGOT/chapters/")
    # book = readWholeBook("../../data/books/ASongOfIceAndFire/AGOT/chapters/")

    # whole book without appendix: 0-73
    # book = readBookByChapters("../../data/books/ASongOfIceAndFire/AGOT/chapters/", 0, 73)
    # print(book)

    # f = open("../../results/books/ASongOfIceAndFire/AGOT/unique_names")
    # unique_names = json.load(f)
    # f.close()
    # print(unique_names[0][0])

    main_characters = get_main_characters("../../results/books/ASongOfIceAndFire/ASOS/unique_names", 21000, ["Lannister", "Jory", "Hand", "Stark", "Mormont"], chapters=False)

    print(main_characters)
    # print(replace_synonyms("Eddard Stark went to the moon"))

    # freq = get_main_character_occurances_for_chapters("../../results/books/ASongOfIceAndFire/AGOT/chapters/", main_characters, 1, 2)
    # print(freq)









