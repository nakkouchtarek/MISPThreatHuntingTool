from datetime import datetime

class Logger:
	def __init__(self, log_file):
		self.log_file = log_file

	def success(self, message):
		with open(self.log_file, "a") as fp:
			message = f"[+] {datetime.now().ctime()} : {message}"
			
			fp.write(message + "\n")
			print(message)

	def info(self, message):
		with open(self.log_file, "a") as fp:
			message = f"[i] {datetime.now().ctime()} : {message}"

			fp.write(message + "\n")
			print(message)

	def warn(self, message):
		with open(self.log_file, "a") as fp:
			message = f"[!] {datetime.now().ctime()} : {message}"

			fp.write(message + "\n")
			print(message)
