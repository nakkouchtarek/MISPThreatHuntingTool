import requests
import json
from pymisp import PyMISP, MISPEvent, MISPOrganisation, MISPAttribute, MISPTag
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
from dotenv import load_dotenv
import os, time

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class MISPClient:
	def __init__(self, logger):
		load_dotenv()
		self.misp_url = 'https://172.27.126.81'
		self.misp_key = os.getenv('MISP')
		self.logger = logger
		self.misp = PyMISP(self.misp_url, self.misp_key, False)

	def api_add_tag(self, tag_name):
		headers = {
		    'Authorization': self.misp_key,
		    'Content-Type': 'application/json'
		}

		# Request body
		data = {
		    'name': tag_name,
		    'exportable': True
		}
		response = requests.post(self.misp_url+"/tags/add", headers=headers, json=data, verify=False)  # Set verify to True if using a valid SSL certificate

		# Check the response
		if response.status_code == 200:
			self.logger.success(f'Tag added successfully: {tag_name}')
		else:
		    self.logger.warn(f'Error adding tag: {response.text}')


	def check_tag(self,tag_name):
		tag = self.misp.get_tag(tag_name)
		if tag['errors'][0] == 405:
			self.api_add_tag(tag)
		return tag_name

	def add_event(self, json_object):
		try:
			event = MISPEvent()
			event.info = json_object['info']
			event.date = json_object['date']
			event.threat_level_id = json_object['threat_level_id']
			event.published = False

			if 'context' in json_object:
				event.add_attribute("text", json_object['context'], comment="Context of keyword")

			event.add_attribute("text", json_object['url'], comment="URL of detection")
			event.add_attribute("text", json_object['attribute'], comment="Flagged")
			event.add_attribute("comment", json_object['comment'], comment="Description")

			for tag_name in json_object['tags']:
				tag = MISPTag()
				tag.name = tag_name
				event.add_tag(tag)

			response = self.misp.add_event(event, pythonify=True)

			if response and 'errors' not in response:
				self.logger.success(f"Event added successfully: {json_object['info']}")
			else:
			    self.logger.warn(f'Error: {response["errors"]}')
		except:
			self.logger.warn(f"An error occured while sending event for {json_object['info']}...")
