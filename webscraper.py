import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import time, random
from logger import Logger

class DarkWebScraper:
    def __init__(self, logger):
        self.user_agents = open("core/user_agents.txt").readlines()
        self.proxies = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
        self.logger = logger
        self.found = set()

    def get_random_user_agent(self):
        return random.choice(self.user_agents).strip()

    def scrape(self, url):
        try:
            headers = {'User-Agent': self.get_random_user_agent()}
            response = requests.get(url, headers=headers, proxies=proxies)

            if response.status_code == 200:
                title, source = self.title_source(url, response.text)
                return title, source[:300]
            else:
                self.logger.warn(f"Failed to fetch content from {url} Status Code: {response.status_code}")
                return "", ""
        except Exception as e:
            self.logger.warn(f"Encoutered exception: {e}")
            return "", ""

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    
    def crawl_site(self, base_url, soup):
        for tag in soup.findAll(href=True):
            url = tag['href']

            base_url = base_url.split("/")

            base_url = base_url[0] + "//" + base_url[2] + "/"

            if "http" in url and ".onion" in url:
                self.found.add(url)

            elif "http" not in url:
                if url[0] == ".":
                    url = url[1:]

                if base_url[-1] == "/" and url[0] == "/":
                    url = url[1:]

                if base_url[-1] != "/" and url[0] != "/":
                    base_url += "/"

                url = base_url + url
                self.found.add(url)
        
        self.logger.success(f"Found {len(self.found)} new directories and sites")

    def title_source(self, url, body):
        soup = BeautifulSoup(body, 'html.parser')

        self.logger.info(f"Scraped url {url}")

        # extract urls mid scrape
        self.crawl_site(url, soup)

        texts = soup.findAll(string=True)
        visible_texts = filter(self.tag_visible, texts)
        title = soup.title.text if soup.title else ""
        return title, u" ".join(t.strip() for t in visible_texts)

