def conll_read():
    with open("conll2003/valid.txt") as f:
        lines = f.readlines()
    sentences = []
    sentences_tag = []
    tmp = ""
    tmp_tag = ""
    tags = []
    for i in range(1000):

        line = lines[i]
        line = line.split(" ")
        text_word = line[0]

        if text_word[0] != "-":
            if text_word == "\n":
                # print(tmp)
                # print(tmp_tag)
                # print("-------")
                sentences.append(tmp)
                tmp = ""
                #sentences_tag.append(tmp_tag)
                #tmp_tag = ""
                sentences_tag.append(tags)
                tags = []

            elif text_word == "(" or text_word == ")" or text_word == '"':
                pass
            else:
                if text_word[0] != "." and text_word[0] != "," and text_word[0] != ":" and text_word[0] != ";"\
                        and text_word[0] != "!" and text_word[0] != "?" and text_word[0] != ")" and text_word[0] != "'":   #or text_word[0] != "," or text_word[0] != "(" or text_word[0] != ")":
                    tmp = tmp + " " + text_word
                    line[3] = line[3].replace("\n", "")

                    if line[3] == "B-PER" or line[3] == "I-PER":
                        line[3] = "PER"
                        #tmp_tag = tmp_tag + " " + line[3]
                        tags.append(line[3])
                    else:
                        line[3] = "O"
                        #tmp_tag = tmp_tag + " " + line[3]
                        tags.append(line[3])
                else:
                    tmp = tmp +  text_word
                    line[3] = "O"
                    tags.append(line[3])


    return sentences, sentences_tag
