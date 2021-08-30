import re
import requests, bs4


# This function creates link of googlenews for searched topic.
def url_generator(key_word):
    key_word = '%20'.join(key_word.split())
    return 'https://news.google.com/search?q={}%20when%3A31d&hl=en-US&gl=US&ceid=US%3Aen'.format(key_word)


# This function generates list of links from google news, related to the topic 
def generate_list_of_links(url): 
    
    info = requests.get(url).text
    parser = bs4.BeautifulSoup(info, 'lxml')
    grid = parser.find('main', {'class':"HKt8rc CGNRMc"})
    links = grid.findAll('article')

    list_links = []
    for link in links:
        try:
            list_links.append(link.find('a', {"class":"VDXfz"})['href'])
        except:
            pass

    list_links = ['https://news.google.com' + i[1:] for i in list_links]
    
    return list_links


# Parser
def parser_3000(corpus):
    new_corpus = []
    
    # these symbols should be removed (replaced by ' ')
    replace_list = [
        u'\xa0',
    ]

    for i in corpus:
        try:
            h = i[1]
            title = h.find('h1').text
            if i[0] == 'apnews.com':
                content = ' '.join(' '.join([i.text for i in h.find('div', {'class':'Article'}).findAll('p')][:-2]).split('— ')[1:])
            
            elif i[0] == 'www.aljazeera.com':
                content = ' '.join([i.text for i in h.findAll('p') if not i.find('strong')][:-1])
            
            elif i[0] == 'www.bloomberg.com':
                content = ' '.join([i.text for i in h.findAll('p', {'class':None}) if i.text])
            
            elif i[0] == 'www.brookings.edu':
                content = ' '.join([i.text for i in h.find('div', {'itemprop':re.compile('article*')}).findAll('p', {'class':None}) if not i.find('em')])
            
            elif i[0] == 'carnegieeurope.eu':
                content =' '.join([i.text for i in h.find('div', {'class':re.compile('article.*')}).findAll('p', {'class':None}) if not i.find('em')])
            
            elif i[0] == 'www.cnbc.com':
                content = ' '.join(' '.join([i.text for i in h.findAll('p', {'class':None}) if i.text]).split('— ')[1:])
            
            elif i[0] == 'www.defenseone.com':
                content = ' '.join([i.text for i in h.findAll('p', {'class':None}) if i.text and not i.find('em') and not i.find('i')][:-1])
            
            elif i[0] == 'edition.cnn.com':
                content = h.find('div', {'class':'l-container'}).text
            
            elif i[0] == 'finance.yahoo.com':
                content = ' '.join([i.text for i in h.find('div', {'class':'caas-body'}).findAll('p', {'class':None}) if not i.find('a')][2:-1])
            
            elif i[0] in ['www.kfgo.com', 'kfgo.com']:
                content = ' '.join(' '.join([i.text for i in h.findAll('p', {'class':None}) if i.text][:-1]).split('–  ')[1:])
            
            elif i[0] == 'moderndiplomacy.eu':
                a = h.find('article')
                content = ' '.join(a.find('div', {'id':'mvp-content-main'}).text.split('\n')[2:-5])
            
            elif i[0] == 'www.ndtv.com':
                content = ' '.join([i.text for i in h.find('div', {'itemprop':'articleBody'}).findAll('p', {'class':None}) if i.text if not i.find('i')])
            
            elif i[0] == 'news.usni.org':
                a = h.find('article')
                content = ' '.join([i.text for i in h.findAll('p', {'class':None}) if i.text][:-1])
            
            elif i[0] == 'www.nytimes.com':
                content = ' '.join(' '.join([i.text for i in h.findAll('p') if i.text][4:-2]).split('— ')[1:])
            
            elif i[0] == 'www.ohio.edu':
                title = h.find('h1', {'class':'story-title'}).text.replace('\n', '')
                content = ' '.join([i.text for i in h.findAll('p') if i.text][:-1])
            
            elif i[0] == 'www.reuters.com':
                a = h.find('article')
                content = ' '.join(' '.join([i.text for i in a.findAll('p')][:-1]).split('- ')[1:])
            
            elif i[0] == 'swimswam.com':
                content = ' '.join([i.text for i in h.find('article').findAll('p') if not i.find('em')])
            
            elif i[0] == 'tass.com':
                content = ' '.join(' '.join([i.text for i in h.findAll('p', {'class':None}) if not i.find('em')]).split('/.')[1:])
            
            elif i[0] == 'www.theguardian.com':
                a = h.find('article')
                content = ' '.join([i.text for i in a.find('main').findAll('p')])
            
            elif i[0] == 'thehill.com':
                content = ' '.join([i.text for i in h.findAll('p')][1:-3])
            
            elif i[0] == 'www.themoscowtimes.com':
                content = ' '.join([i.text for i in h.find(attrs={'class':'article__content'}).findAll('p') if i.text])
            
            elif i[0] == 'www.wsj.com':
                content = ' '.join([i.text for i in h.findAll('p', {'class':None}) if i.text][:-3])
            
            else:
                ' '.join([i.text for i in h.findAll('p', {'class':None}) if i.text][:-3])
            
            text = title + ' ' + content
            
            for j in replace_list:
                text = text.replace(j, ' ')
            
            new_corpus.append(text)
        except:
            pass
    return new_corpus
    
# Second preprocessing of text
def clean_text(s):
    new_s = ''
    sign = 0
    for c in s:
        if sign:
            sign = 0
        else:
            if c == '’':
                sign = 1
            elif c in '.,\'?!|:(){}[]\"&%#$1234567890\\/-—><':
                pass
            else:
                new_s = new_s + c
    return new_s.upper()