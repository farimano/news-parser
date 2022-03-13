import logging

class Logger():
	default_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - " \
		"(%(filename)s.%(funcName)s(%(lineno)d)) - %(message)s"
	empty_log_format = f""
	
	def __new__(cls, name:str):
		cls.logger = logging.getLogger(name)
		cls.logger.setLevel(logging.INFO)
		cls.name = name
		
		if not len(cls.logger.handlers):
			cls.add_handler(cls, cls.empty_log_format)
			cls.logger.info("")
			cls.logger.handlers.clear()
			
			cls.add_handler(cls, cls.default_log_format)
		return cls.logger
		
	def add_handler(cls, log_format:str):
		handler = logging.FileHandler(f"logs/{cls.name}.log")
		handler.setLevel(logging.INFO)
		handler.setFormatter(logging.Formatter(log_format))
		cls.logger.addHandler(handler)
