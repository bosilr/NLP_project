# Natural language processing project

## Description

The goal of this project was to find main characters in a book (here specifically Game of Thrones) and determine if they are allies or foes.

Scripts ![analiza2_flairNER](https://github.com/bosilr/NLP_project/tree/main/code/analiza2_flairNER.ipynb) and ![flairNERForChapters](https://github.com/bosilr/NLP_project/tree/main/code/flairNERForChapters.py) are used for Named Entity Relations. Their evaluation is located in ![this](https://github.com/bosilr/NLP_project/tree/main/code/modeli_NER/NER_results) folder. Script ![sentimentAnalysis](https://github.com/bosilr/NLP_project/tree/main/code/sentimentAnalysis.py) is used for determining the relations and script ![sentimentAnalysisGraphs](https://github.com/bosilr/NLP_project/tree/main/code/sentimentAnalysisGraphs.py) is used for plotting the graphs. Different models for NER can be found in code/modeli_NER.



All images and results for the book A Game of Thrones can be found in the results folder ![here](https://github.com/bosilr/NLP_project/tree/main/results/books/ASongOfIceAndFire/AGOT/). 

## How to run the code

To obtain the same final results, that are present in the report and in the ![results](https://github.com/bosilr/NLP_project/tree/main/results) folder one needs to follow the following steps:

* to obtain the NER results (without coreference resolution) you run ![flairNERForChapters](https://github.com/bosilr/NLP_project/tree/main/code/flairNERForChapters.py). This code saves the NER results ![here](https://github.com/bosilr/NLP_project/tree/main/results/books/ASongOfIceAndFire/AGOT/chapters).
    * to obtain NER results with coreference resolution you need to run ![FlairNERForChapters_allen_colab.ipynb](https://github.com/bosilr/NLP_project/blob/main/code/FlairNERForChapters_allen_colab.ipynb) in Google Colaboratory (this code takes quite some time to execute, even with the use of a GPU). Before you can run the code you need to zip the whole repository and upload the zip file to your drive (in a new directory named Kode). After this all cells can be run (the code produces text files after coreference resolution and NER results with coreference resolution). If you wish to perform further analysis you will need to copy the obtained results into the results folder of the repository (we copied the text results with the Allennlp coreference resolution ![results/books/ASongOfIceAndFire/AGOT/chapters_coref_allen_text](https://github.com/bosilr/NLP_project/tree/main/results/books/ASongOfIceAndFire/AGOT/chapters_coref_allen_text) and the NER results into ![results/books/ASongOfIceAndFire/AGOT/chapters_coref_allen](https://github.com/bosilr/NLP_project/tree/main/results/books/ASongOfIceAndFire/AGOT/chapters_coref_allen)).

* results of NER are provided in the following direcotories:
    * NER without coreference resolution: ![results/books/ASongOfIceAndFire/AGOT/chapters](https://github.com/bosilr/NLP_project/tree/main/results/books/ASongOfIceAndFire/AGOT/chapters)
    * NER with Allennlp coreference resolution: ![results/books/ASongOfIceAndFire/AGOT/chapters_coref_allen](https://github.com/bosilr/NLP_project/tree/main/results/books/ASongOfIceAndFire/AGOT/chapters_coref_allen)
    * NER with spaCy coreference resolution: ![results/books/ASongOfIceAndFire/AGOT/chapters_coref_spacy](https://github.com/bosilr/NLP_project/tree/main/results/books/ASongOfIceAndFire/AGOT/chapters_coref_spacy) 

* to obtain the results for detecting the main characters of chapters you run ![mainCharacters.py](https://github.com/bosilr/NLP_project/tree/main/code/mainCharacters.py).
    * depending on the path in code (normal_path, coref_spacy, coref_allen) different NER results will be used in the analysis
   
* to obtain the sentiment analysis graphs you run ![sentimentAnalysisGraphs.py](https://github.com/bosilr/NLP_project/tree/main/code/sentimentAnalysisGraphs.py). Currently the code is set to use NER results from the Allennlp coreference resolution, if you wish to use different NER results the correct paths need to be changed. (To use NER results without coreference resolution you will need to change some variables (all are commented in main next to their replacements)).

If you have any problems of questions you can contact us on github: MGG#3032 or Krompir#5509

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
