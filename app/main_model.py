# 0. Import all required modules and packages
import bs4, requests

from .additional_functions import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from collections import Counter
from wordcloud import WordCloud, STOPWORDS


def model(n, key_word):
    # 1. Parsing of urls from google.news
    url = url_generator(key_word)
    list_links = generate_list_of_links(url)

    # 2. Parsing of articles, which have been collected on google.news
    corpus = []
    for link in list_links[:30]: # to reduce time-consuming
        try:
            page = requests.get(link, timeout=10).text
            parser = bs4.BeautifulSoup(page, 'lxml')

            text = [parser.find('title').text]
            body = [i.text for i in parser.findAll('p')]
            text.extend(body)

            corpus.append(text)
        except:
            pass

    # 3. Cleaning and preprocessing
    corpus = list(map(doc_edit, corpus))
    corpus = [' '.join(i) for i in corpus]
    clean_corpus = [clean_text(doc) for doc in corpus]
    clean_corpus = [i for i in clean_corpus if len(i)>=100]

    # 4. Clustering
    vect = TfidfVectorizer(stop_words='english', ngram_range=(1, 4))
    vect_corpus = vect.fit_transform(clean_corpus)
    km = KMeans(n_clusters=n, init='k-means++')
    labels = km.fit_predict(vect_corpus)

    # 5. WordCloud
    global STOPWORDS
    STOPWORDS = {i.upper() for i in STOPWORDS}
    
    dict_of_cntr = {}

    for z in range(n):
        temp_corp = [j for c, l in zip(clean_corpus, labels) for j in c.split() if l==z]
        dict_of_cntr[z] = dict(Counter(temp_corp))

        for w in dict_of_cntr[z]:
            if w in STOPWORDS:
                dict_of_cntr[z][w] = 0

    fig = Figure(figsize=(6.8, 6.8*n*0.6))

    for i in range(n):
        cntr = dict_of_cntr[i]
        wc = WordCloud(width=1000, height=500, max_words=30, background_color='#085B88', colormap='Reds')
        axis = fig.add_subplot(n, 1, i+1)
        wc.generate_from_frequencies(dict(cntr))
        axis.axis('off')
        axis.set_title(f'{key_word} cluster № {i+1}')
        axis.imshow(wc)
    fig.tight_layout()

    return fig