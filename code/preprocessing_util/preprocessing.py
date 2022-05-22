import os
import natsort



def renameFiles(path):
    for file in os.listdir("../../data/books/ASongOfIceAndFire/AGOT/chapters"):
        split_name = file.split("_")
        src = path + file
        dest = path + split_name[2].replace(".txt", "") + "_" + split_name[0] + "_" + split_name[1] + ".txt"
        # dest = path + split_name[1] + "_" + split_name[2].replace(".txt", "") + "_" + split_name[0] + ".txt"


        os.rename(src, dest)


def read_text(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
        # text = text.replace('\r', ' ').replace('\n', ' ')\
        #     .replace("’", "'").replace("\"", "").replace("”", "").replace("“", "")
    return text


def getChaptersInOrder(path):
    chapters = os.listdir(path)
    return natsort.natsorted(chapters)


def readWholeBook(path):
    chapter_lists = getChaptersInOrder(path)

    book = ""
    for chapter in chapter_lists:
        if "Appendix" not in chapter:
            book += read_text(path + chapter)

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
        book += read_text(path + chapter_lists[i])

    book = book.replace('\r', ' ').replace('\n', ' ') \
        .replace("’", "'").replace("\"", "").replace("”", "").replace("“", "")

    return book


if __name__ == "__main__":
    # renameFiles("../data/books/ASongOfIceAndFire/AGOT/chapters/")
    book = readWholeBook("../../data/books/ASongOfIceAndFire/AGOT/chapters/")

    # whole book without appendix: 0-73
    book = readBookByChapters("../../data/books/ASongOfIceAndFire/AGOT/chapters/", 0, 73)
    print(book)

