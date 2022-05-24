from preprocessing_util.utils import get_character_occurances2, getChaptersInOrder, get_main_characters


if __name__ == '__main__':
    normal_path = "../results/books/ASongOfIceAndFire/AGOT/chapters/"
    coref_spacy = "../results/books/ASongOfIceAndFire/AGOT/chapters_coref_spacy/"
    coref_allen = "../results/books/ASongOfIceAndFire/AGOT/chapters_coref_allen/"

    chapters = getChaptersInOrder(coref_allen)
    chapters = [r for r in chapters if "entity_dict" not in r]

    print(get_main_characters(coref_allen, 21000, [], chapters=True))

    pov_dict = {}
    for chapter in chapters:
        pov_character = chapter.split("_")[1]
        if pov_character not in pov_dict:
            pov_dict[pov_character] = []

    for i in range(73):
        mc = get_character_occurances2(coref_allen, i, i+1, to_print=True)
        pov_character = chapters[i].split("_")[1]
        print("POV character:", pov_character)

        position = -1
        for j, el in enumerate(mc):
            if pov_character == "Eddard":
                if el[0] == "Ned":
                    position = j+1
            if el[0] == pov_character:
                position = j+1

        pov_dict[pov_character].append(position)

        print("Position of POV character: ", position)
        print()
        print(mc)
        print("---------------------------------------------------------------------------------")

    print("---------------------Eval----------------------")
    for pov in pov_dict:
        if pov != "Appendix":
            print(pov, pov_dict[pov], " | Average: ", (sum(pov_dict[pov])/len(pov_dict[pov])))



