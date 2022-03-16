import hydra

from argparse import ArgumentParser, RawTextHelpFormatter
from app.utils.runners import RunnerInterface
from app.utils.types import LinksList

class WordCloudRunner(RunnerInterface):
    def __init__(self):
        self.parse_args()
        self.load_settings()
    
    def parse_args(self):
        parser = ArgumentParser(description="This microservice creates"\
            "several wordclouds for a chosen topic. The example:\npython"\
            " service.py Europe", formatter_class=RawTextHelpFormatter)
        parser.add_argument('topic', type=str)
        parser.add_argument('settings', type=str)
        args = parser.parse_args()
        self.__dict__.update(args.__dict__)
    
    def load_settings(self) -> None:
        with hydra.initialize(config_path="../settings"):
            set_dict = dict(hydra.compose(config_name="settings", 
                overrides=[]))
        classes_dict = set_dict.pop("classes")
        self.import_classes(classes_dict)
        self.__dict__.update(set_dict)
		
        param_list = []
		
        for key in set_dict:
            param_string = f"{key}: {set_dict[key]}"
            param_list.append(param_string)
        param_info = ", ".join(param_list)
        self.logger.info("The following parameters have been" \
            f" selected - {param_info}.")		
    
    def import_classes(self, classes_dict:dict) -> None:
        for class_type in classes_dict:
            module_name = class_type.split('_')[-1]
            class_name = classes_dict[class_type]
            module = __import__(module_name)
            self.__dict__[class_type] = module.__dict__.get(class_name)

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
    
    def load_links(self) -> LinksList:
        links_loader = self.links_loader(self)
        links_list = links_loader.load()
        return links_list

if __name__ == "__main__":
    runner = WordCloudRunner()
    runner.run()