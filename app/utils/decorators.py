import time
import datetime

def timer(func):
	def func_with_timer(self, *args, **kwargs):
		start = time.time()
		
		output = func(self, *args, **kwargs)
		
		seconds = time.time() - start
		dur = str(datetime.timedelta(seconds=seconds))
		self.logger.info(f"The {self.operation_name} has"\
			f" been successfully completed in {dur}.")
		return output
	return func_with_timer
