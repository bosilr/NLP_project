import re
import spacy
nlp = spacy.load('en_core_web_md')

def remove_non_alphanumeric(text):
    text =  re.sub('[^a-zA-Z]', ' ', text)
    return re.sub('Ser', text)
