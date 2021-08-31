# 0. Import all required modules and packages
import bs4, requests

from .additional_functions import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from collections import Counter
from wordcloud import WordCloud, STOPWORDS


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'referrer': 'https://google.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Pragma': 'no-cache'
}



def model(n, key_word):
    try:
        assert type(key_word) == str
        # 1. Parsing of urls from google.news
        url = url_generator(key_word)
        list_links = generate_list_of_links(url)

        # 2. Parsing of articles, which have been collected on google.news
        corpus = []
        global headers
        for link in list_links[:30]: # to reduce time-consuming
            try:
                link = requests.head(link, stream=True).headers['Location']
                req = requests.get(link, timeout=1.5, headers=headers)
                if req.status_code < 400:
                    site = req.url.split('/')[2]
                    text = bs4.BeautifulSoup(req.text, 'lxml')

                    corpus.append((site, text))
            except:
                pass

        # 3. Cleaning and preprocessing
        corpus = parser_3000(corpus)
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
    except ValueError:
        fig = Figure(figsize=(6.8*0.6*1.1, 6.8*0.2*0.6*1.2))
        axis = fig.add_subplot(1, 1, 1)
        axis.text(0, 0, 'Sorry, not enough news for this topic.\nTry another one!', fontsize=20, ha='center', va='center', c='crimson', backgroundcolor='skyblue', family='monospace')
        axis.axis('off')
        fig.tight_layout()
    except:
        fig = Figure(figsize=(6.8*0.6*1.1, 6.8*0.2*0.6*1.2))
        axis = fig.add_subplot(1, 1, 1)
        axis.text(0, 0, 'Oops, something goes wrong.\nPlease, try again!', fontsize=20, ha='center', va='center', c='crimson', backgroundcolor='skyblue', family='monospace')
        axis.axis('off')
        fig.tight_layout()
    return fig