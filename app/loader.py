import requests

from app.utils.types import LinksList, Link
from app.utils.initializer import Initializer
from bs4 import BeautifulSoup

class LoaderInterface(object):
    def load(self):
        raise NotImplementedError

class LinksListLoaderInterface(LoaderInterface):
    def load(self) -> LinksList:
        raise NotImplementedError

class ParentLinksListLoader(LinksListLoaderInterface, Initializer):
    """The parent class for all LinksListLoaders"""

class GoogleLinksListLoader(ParentLinksListLoader):
    def load(self) -> LinksList:
        news_link = self.get_news_link()    
        
        text = requests.get(news_link).text
        parser = BeautifulSoup(text, 'lxml')
        main_section = parser.find('main', {'class':"HKt8rc CGNRMc"})
        articles_list = main_section.findAll('article')

        links_list = []
        for article in articles_list:
            try:
                link_body = article.find('a', {"class":"VDXfz"})['href'][1:]
                link = 'https://news.google.com' + link_body
                links_list.append(link)
            except:
                pass
        
        return links_list
    
    def get_news_link(self) -> Link:
        fmt_topic = '%20'.join(self.topic.split())
        news_link = f"https://news.google.com/search?q={fmt_topic}"\
            "%20when%3A31d&hl=en-US&gl=US&ceid=US%3Aen"
        return news_link

