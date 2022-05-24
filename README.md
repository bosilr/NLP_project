# Natural language processing project

## Description

The goal of this project was to find main characters in a book (here specifically Game of Thrones) and determine if they are allies or foes.

Scripts ![analiza2_flairNER](https://github.com/bosilr/NLP_project/blob/main/code/analiza2_flairNER.ipynb) and ![flairNERForChapters](https://github.com/bosilr/NLP_project/blob/main/code/flairNERForChapters.py) are used for Named Entity Relations, script ![sentimentAnalysis](https://github.com/bosilr/NLP_project/blob/main/code/sentimentAnalysis.py) is used for determining the relations and script ![sentimentAnalysisGraphs](https://github.com/bosilr/NLP_project/blob/main/code/sentimentAnalysisGraphs.py) is used for plotting the graphs. Different models for NER can be found in code/modeli_NER.

All images can be found in the results folder ![here](https://github.com/bosilr/NLP_project/tree/main/results/books/ASongOfIceAndFire/AGOT/sentiment). 


## Generated GIFs for Knowledge graphs
These GIFs represent knowledge graphs obtained from our model with different parameters

### Co-occurrence 

Co-occurrence on original text
![](https://github.com/bosilr/NLP_project/blob/main/results/gif/normal_coor_gif.gif)

Co-occurrence on text preprocessed with coreference resolution
![](https://github.com/bosilr/NLP_project/blob/main/results/gif/coref_coor_gif.gif)

### Sentiment analysis using Afinn

Blue color represents that connected characters are allies and red color represents that they are foes.

Relations on original text
![](https://github.com/bosilr/NLP_project/blob/main/results/gif/normal_afinn_gif.gif)

Relations on text preprocessed with coreference resolution
![](https://github.com/bosilr/NLP_project/blob/main/results/gif/coref_afinn_gif.gif)

### Sentiment analysis using Vader
Relations on original text
![](https://github.com/bosilr/NLP_project/blob/main/results/gif/normal_vader_gif.gif)

Relations on text preprocessed with coreference resolution
![](https://github.com/bosilr/NLP_project/blob/main/results/gif/coref_vader_gif.gif)
