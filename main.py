import requests
from gemini import GeminiClass
import time
from MISP import MISPClient
from datetime import datetime
from queue import Queue
from threading import Thread
import hashlib
from webscraper import DarkWebScraper
from logger import Logger
import pyfiglet
import dnstwist
import sys, time
from bs4 import BeautifulSoup
import whoisfetcher

class DetectorFramework:
    def __init__(self, logger, _list):

        self.blacklist_words = [elem.strip() for elem in open("core/blacklist").readlines()]

        self.logger = logger

        self.scraper = DarkWebScraper(self.logger)
        self.gemini = GeminiClass(self.logger)
        self.misp_client = MISPClient(self.logger)

        self.queue = Queue()

        self.blacklist_urls = [elem.strip() for elem in open("core/blacklist_urls").readlines()[0].split(" ")][:-1]
        self.bins = [elem.split(",")[2] for elem in open("core/bins").readlines()]
        self.urls = []

        self.threads = []
        self.url_counter = 0

        self.n_threads = 5
        self.urls_per_thread = 1
        self.jump = self.n_threads * self.urls_per_thread

        self.url_list = _list

    def load_save(self):
        f = open("core/progress").readlines()
        if len(f) == 0: self.url_counter = 0

        self.url_counter = int(f[0].split("=")[1])

    def save_progress(self):
        with open("core/progress","w") as f:
            f.write(f"COUNT={self.url_counter}")

    def handle_urls(self, urls):
        for url in urls:
            self.handle_url(url)

    def get_threat_misp(self, threat_level):
        if threat_level >= 4:
            return 1
        elif threat_level >= 2:
            return 2
        else:
            return 3

    def clean_word(self, element):
        return "".join([elem.strip().lower() for elem in element if elem.isalpha()])

    def check_if_blacklisted(self, url):
        if hashlib.md5(url.strip().encode('utf-8')).hexdigest() in self.blacklist_urls:
            self.logger.warn(f"Domain blacklisted : {url}, please report it ! ")
            return True

        return False

    def get_context(self, word, text):
        for line in text.split("\n"):
            if word in line: return line
        return None

    def handle_url(self, url):
        # Scrape url
        title, source = self.scraper.scrape(url)

        for blacklisted_word in self.blacklist_words:
            context = self.get_context(blacklisted_word, source)
            if context:
                self.logger.success(f"Program has encountered a blacklisted word {blacklisted_word} at {url}")
                
                # Send request to Gemini
                gemini_res = self.gemini.send(f"Title: {title}\nSource: {source}")
                
                if gemini_res == "Error":
                	self.logger.warn(f"Error occured while proccessing detect word : {blacklisted_word} at {url}")
                	return

                #print(gemini_res)

                # Do some string modifications to results
                threat_level, description, tags, reason = [elem.split(":")[1].strip() for elem in gemini_res.split("\n") if elem != '']
                tags = [self.clean_word(elem) for elem in tags.split(",")][:2]
                
                misp_json = {
                    'url': url,
                    'context': context,
                    'info':f'{reason.replace(".","")} : {blacklisted_word} found at {url}',
                    'date':datetime.now().ctime(),
                    'threat_level_id':self.get_threat_misp(int(threat_level)),
                    'attribute':blacklisted_word,
                    'comment':f"Description: {description}",
                    'tags':tags,
                    'galaxy':'placeholder_galaxy'
                }

                self.misp_client.add_event(misp_json)

        for _bin in self.bins:
            if _bin in source or _bin in title:
                self.logger.success(f"Program has encountered a concerning BIN {_bin} at {url}")
                
                misp_json = {
                    'url': url,
                    'info':f'Credit Card Fraud : {_bin} found at {url}',
                    'date':datetime.now().ctime(),
                    'threat_level_id': 1,
                    'attribute': _bin,
                    'comment':f"Description : Encountered a bin while browsing {url} : _bin, risk of credit card fraud.",
                    'tags':["creditcardfraud"],
                    'galaxy':'placeholder_galaxy'
                }

                # Send event
                self.misp_client.add_event(misp_json)

    def add_to_urls(self, line_number, new_lines):
        with open(self.url_list, 'r') as file:
            new_lines = list(new_lines)

            lines = file.readlines()

            line_number = max(0, min(line_number, len(lines)))

            lines = lines[:line_number + 1] + new_lines + lines[line_number + 1:]

            with open(self.url_list, 'w') as file:
                for line in lines:
                    line = line.strip()

                    file.write(line+"\n")

    def keyword_search_darkweb(self): 
        self.logger.info(f"Started framework!")
        self.load_save()

        if self.url_counter != 0:
            self.logger.info(f"Loaded progress! Continuing at url number {self.url_counter}")
            self.urls = list(set([url.strip() for url in open(self.url_list).readlines()[self.url_counter:self.url_counter+self.jump] if not self.check_if_blacklisted(url)]))
        else:
            self.urls = list(set([url.strip() for url in open(self.url_list).readlines()[:self.jump] if not self.check_if_blacklisted(url)]))
        
        while True:
            for i in range(self.n_threads):
                for j in range(self.urls_per_thread):
                    if self.urls:
                        self.queue.put(self.urls[-1])
                        self.urls = self.urls[:-1]
                        self.url_counter += 1
            
            for _ in range(self.n_threads):
                thread_urls = []
                for j in range(self.urls_per_thread):
                    if not self.queue.empty():
                        thread_urls.append(self.queue.get())

                if thread_urls is not None:
                    self.threads.append(Thread(target=self.handle_urls, args=(thread_urls,)))
                    
            for i, thread in enumerate(self.threads):
                thread.start()

            for thread in self.threads:
                thread.join()

            self.threads.clear()
            
            self.logger.info(f"Program has processed {self.url_counter} urls! Saving progress...")
            self.save_progress()
            self.logger.info(f"Progress saved!")


            # add to urls.txt found directories
            self.add_to_urls(self.url_counter, self.scraper.found)
            # clear set
            self.scraper.found.clear()
            # take another bunch of urls and put to urls
            self.urls = list(set([url.strip() for url in open(self.url_list).readlines()[self.url_counter:self.url_counter+self.jump] if not self.check_if_blacklisted(url)]))

            if not self.urls:
                break
        
        self.logger.success("All websites have been processed! Exiting now...")

    def file_check(self):
        lines = []
        tags = set()

        with open(self.url_list) as f:
            for i,line in enumerate(f.readlines()):
                for blacklisted_word in self.blacklist_words:
                    if blacklisted_word in line:
                        lines.append(f"{i} -> {line}")
                        self.logger.success(f"Program has encountered a blacklisted word {blacklisted_word} at line {i} : {line.strip()}")
                        tags.add("databreach")
        
        if tags:
            new = '\n'.join(lines)
            misp_json = {
                'url': self.url_list,
                'info':f'Data Breach : Found {len(lines)} blacklisted words in file',
                'date':datetime.now().ctime(),
                'threat_level_id': 1,
                'attribute': self.url_list,
                'comment':f"Description : Encountered concerning info at specific lines in file:\n{new}",
                'tags':tags,
                'galaxy':'placeholder_galaxy'
            }

            self.misp_client.add_event(misp_json)

        self.logger.success("Extracted all suspected keywords from file! Exiting now...")

    def check_bin(self):
        lines = []
        tags = set()

        with open(self.url_list) as f:
            for i,line in enumerate(f.readlines()):
                for _bin in self.bins:
                    if _bin in line:
                        lines.append(f"{i} -> {line}")
                        self.logger.success(f"Program has encountered a concerning BIN {_bin} at line {i} : {line.strip()}")
                        tags.add("creditcardfraud")
        
        new = '\n'.join(lines)

        if tags:
            misp_json = {
                'url': self.url_list,
                'info':f'Credit Card Fraud : Found {len(lines)} leaked cards',
                'date':datetime.now().ctime(),
                'threat_level_id': 1,
                'attribute': self.url_list,
                'comment':f"Description : Encountered concerning info at specific lines in file:\n{new}",
                'tags':tags,
                'galaxy':'placeholder_galaxy'
            }

            self.misp_client.add_event(misp_json)
        self.logger.success("Extracted all suspected CC's from file! Exiting now...")

    def dns_phishing_search(self):
        self.logger.info("Started fuzzing for phishing domains")
        c = whoisfetcher.WHOisFetcher()
        for _ in [elem.strip() for elem in open(self.url_list).readlines()]:
            self.logger.info(f"Looking for similar domains to {_}")
            data = dnstwist.run(domain=_, format='null', registered=True, tld="core/tlds.dict", mxcheck=True, lsh="ssdeep")

            if len(data) == 0:
                self.logger.info("Found 0 results...")
                return

            self.logger.success(f"Found {len(data)} results!")
            self.logger.info(f"Sleeping for 5 minutes for DNS restoration")
            time.sleep(60*5)

            for domain in data:
                _domain = domain['domain']

                if domain['fuzzer'] != '*original':

                    self.logger.success(f"{_domain} is a lookalike domain. Sending event to CTI!")

                    whois_res = c.get_whois_info(_domain)

                    if whois_res != "Not Found":

                        while True:
                            try:
                                misp_json = {
                                    'url': _domain,
                                    'info':f'Phishing : found lookalike registered domain of {_} at {_domain}',
                                    'date':datetime.now().ctime(),
                                    'threat_level_id': 2,
                                    'attribute': _,
                                    'comment':f"{str(domain)}\nWHOIS results:\n{whois_res}",
                                    'tags':["Phishing","Lookalike"],
                                    'galaxy':'placeholder_galaxy'
                                }

                                self.misp_client.add_event(misp_json)
                                break
                            except:
                                self.logger.info("Something happened in MISP event process, retrying in 10 seconds...")
                                time.sleep(10)
                                continue

            c.driver.quit()
            self.logger.success("Went through all domains! Exiting now...")

if __name__ == "__main__":    
    print(pyfiglet.figlet_format("Threat Intelligence Tool"))

    if len(sys.argv) < 3:
        print("Invalid usage: python main.py [darkweb|filechecker|binchecker|phishing] [url_list]")
        exit(-1)

    handler = DetectorFramework(Logger("handler.log"), sys.argv[2])

    if sys.argv[1] == "darkweb":
        handler.keyword_search_darkweb()
    elif sys.argv[1] == "filechecker":
        handler.file_check()
    elif sys.argv[1] == "phishing":
        handler.dns_phishing_search()
    elif sys.argv[1] == "binchecker":
        handler.check_bin()
    else:
        print("Invalid usage: python main.py [darkweb|filechecker|binchecker|phishing] [url_list]")
        exit(-1)