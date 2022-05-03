import re
import spacy
nlp = spacy.load('en_core_web_md')

def remove_non_alphanumeric(text):
    return re.sub('[^a-zA-Z]', ' ', text)
