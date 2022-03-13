from app.utils.runners import RunnerInterface
from .utils.runners import RunnerInterface

class WordCloudRunner(RunnerInterface):
    def run(self):
        links_list = self.load_links()
        raw_corpus = []
        for link in links_list:
            record = self.get_record(link)
            raw_corpus.append(record)
        corpus = self.preprocess(raw_corpus)
        labels = self.cluster(corpus)
        figure = self.get_figure(corpus, labels)
        return figure

        