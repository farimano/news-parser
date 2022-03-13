from utils.logger import Logger
from utils.runners import RunnerInterface

class Initializer:
	def __init__(self, runner:RunnerInterface):
		self.__dict__.update(runner.__dict__)
		self.runner = runner
		
		name_class = type(self).__name__
		self.logger.info(f"{name_class} has been initialized.")
