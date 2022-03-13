from argparse import ArgumentParser, RawTextHelpFormatter
from app.utils.runners import RunnerInterface

class WordCloudRunner(RunnerInterface):
    def __init__(self):
        self.load_args()
        self.load_settings()
    
    def load_args(self):
        parser = ArgumentParser(description="This microservice creates"\ 
            "several wordclouds for a chosen topic. The example:\npython"\
            " service.py Europe", formatter_class=RawTextHelpFormatter)
        parser.add_argument('topic', type=str)
        parser.add_argument('settings', type=str)
        args = parser.parse_args()
        self.__dict__.update(args.__dict__)

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

if __name__ == "__main__":
    runner = WordCloudRunner()
    runner.run()