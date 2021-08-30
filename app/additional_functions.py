import re
import requests, bs4


# This function creates link of googlenews for searched topic.
def url_generator(key_word):
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


# First preprocessing of parsed text
def doc_edit(doc):
    
    # Exclude typical phrases
    excl_st = [
        'by signing up you agree to our terms of use and privacy\xa0policy',
        'the most important news stories of the day, curated by post editors and delivered every morning.',
        'advertisement',
        'supported by',
        'view the discussion thread.',
        'rfe/rl journalists report the news in 27\xa0languages in 23\xa0countries where a free press is banned by the government or not fully established. we provide what many people cannot get locally: uncensored news, responsible discussion, and open debate.',
        ' ',
        'the selected text has limit of 300 characters',
        '\n\n\nprint\n\n',
    ]
    
    # Exclude typical patterns
    excl_phr = [
        '(.*?)all rights reserved(.*?)',
        '(.*?)[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9](.*?)',
        '(.*?)please consider making a donation to(.*?)',
        '(.*?)our exclusives and on-the-ground reporting are being read and shared(.*?)',
        '(.*?)subscribe for our daily(.*?)',
        '(.*?)by subscribing i accept(.*?)'
    ]
    
    # These sentences indicate, that an article has ended, so the program should stop for-cycle
    stop_list = [
        'our standards: the thomson reuters trust principles.',
        'carnegie does not take institutional positions on public policy issues; the views represented herein are those of the author(s) and do not necessarily reflect the views of carnegie, its staff, or its trustees.',
        "reuters, the news and media division of thomson reuters, is the world’s largest multimedia news provider, reaching billions of people worldwide every day. reuters provides business, financial, national and international news to professionals via desktop terminals, the world's media organizations, industry events and directly to consumers.",
        'page not found',
        'the views expressed in this publication are the authors’ and do not imply endorsement by the office of the director of national intelligence, the intelligence community, or any other u.s. government agency.',
        'doi:10.1126/science.abm1182',
        '403 forbidden',
        'for more expert analysis of the biggest stories in economics, business and markets, sign up to money talks, our weekly newsletter.',
        'the views expressed in this article are the author’s own and do not necessarily reflect al jazeera’s editorial stance.',
        'got a confidential news tip? we want to hear from you.',
        '\r\n          to continue reading you must login or register with us.\r\n        ',
        "get insights on the latest news in us politics from jon lieber, head of eurasia group's coverage of political and policy developments in washington:",
        'bank of america is building a network of support for minority small business owners through cdfis, mdis, and minority focused funds.'
    ]
    
    # these phrases do not make sense, so they can be removed (replaced by None)
    replace_list = [
        u' - report - the jerusalem post ',
        u'- the new york times',
        u'\xa0',
        u'| thehill',
        u'- the moscow times',
        u'| reuters',
        u'| the economist',
        u'- gzero media'
    ]
    
    new_doc = []
    for i in doc:
        sign = 1
        if i.lower() in stop_list:
            break
        if i.lower() in excl_st:
            pass
        else:
            for j in excl_phr:
                if bool(re.match(j, i.lower(), re.DOTALL)):
                    sign = 0
                    break
            if sign:
                new_line = i.lower()
                for j in replace_list:
                    new_line = new_line.replace(j, ' ')
                new_doc.append(new_line)
    return new_doc


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
                content = ''
            
            text = title + ' ' + content
            
            for j in replace_list:
                text = text.replace(j, ' ')
            
            new_corpus.append(text)
        except:
            pass
    return new_corpus