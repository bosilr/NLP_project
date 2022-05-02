from os import listdir
from os.path import isfile, join
from nltk import word_tokenize, pos_tag, ne_chunk, sent_tokenize
from nltk.tag import untag, str2tuple, tuple2str
from nltk.chunk import tree2conllstr, conllstr2tree, conlltags2tree, tree2conlltags
from sklearn.feature_extraction.text import TfidfVectorizer

if __name__ == "__main__":
    files = [f for f in listdir("../data/english") if isfile(join("../data/english", f))]
    vect = TfidfVectorizer()
    sent = []
    not_words = ['.', ',', ':', '"', '?', "!", '‘']
    num_tokens = 0
    token_len = 0
    for f in files:
        file = open("data/english/" + f, 'rt', encoding="utf8")
        text = file.read()
        text = text.lower()
        tokens = word_tokenize(text)
        for t in tokens:
            if t not in not_words:
                num_tokens += 1
                token_len += len(t)
        sent.append(text)
    tfidf = vect.fit_transform(sent)
    avg_tokens = num_tokens / len(files)
    avg_token_len = token_len / num_tokens
    print(avg_tokens)
    print(avg_token_len)



    cosine = (tfidf * tfidf.T).A
    avg = 0
    num = 0
    for i in range(len(cosine)):
        for j in range(len(cosine[0])):
            if i != j:
                avg += cosine[i][j]
                num += 1
    print("Cosine similarity between the documents: \n{}".format(cosine))
    print(avg/num)
    print(cosine.shape)