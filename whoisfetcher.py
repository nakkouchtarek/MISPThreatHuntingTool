from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

class WHOisFetcher:
	def __init__(self):
		options = Options()
		options.add_argument("--headless")
		options.set_preference("general.useragent.override",random.choice(open("core/user_agents.txt").readlines()).strip())
		self.driver = webdriver.Firefox(options=options)

	def get_whois_info(self, domain):
		self.driver.get(f"https://www.whois.com/whois/{domain}")

		try:
			element = self.driver.find_element(By.ID, "registryData")
		except:
			element = None

		try:
			element2 = self.driver.find_element(By.ID, "registrarData")
		except:
			element2 = None

		if element:
			return element.text
		elif element2:
			return element2.text
		else:
			return "Not Found"