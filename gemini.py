import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiClass:
	def __init__(self, logger):
		load_dotenv()
		self.logger = logger
		genai.configure(api_key=os.getenv('GEMI'))

		generation_config = {
		  "temperature": 0.9,
		  "top_p": 1,
		  "top_k": 1,
		  "max_output_tokens": 2048,
		}

		safety_settings = [
		  {
		    "category": "HARM_CATEGORY_HARASSMENT",
		    "threshold": "BLOCK_ONLY_HIGH"
		  },
		  {
		    "category": "HARM_CATEGORY_HATE_SPEECH",
		    "threshold": "BLOCK_ONLY_HIGH"
		  },
		  {
		    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
		    "threshold": "BLOCK_ONLY_HIGH"
		  },
		  {
		    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
		    "threshold": "BLOCK_ONLY_HIGH"
		  },
		]

		model = genai.GenerativeModel(model_name="gemini-1.0-pro",
		                              generation_config=generation_config,
		                              safety_settings=safety_settings)

		self.convo = model.start_chat(history=[
		  {
		    "role": "user",
		    "parts": ["I will be giving you the following input from here on out in this format : Title: {title_name}\\\\nSource: {page_source} and i want you to give me how dangerous the site is out of 10, so if the site for example tries to sell illegal stuff you give me a 10, if a site is an article about selling illegal stuff the rating should be moderately low, not high since it is not commit criminal activity."]
		  },
		  {
		    "role": "model",
		    "parts": ["​"]
		  },
		  {
		    "role": "user",
		    "parts": ["Title: Crack cocaine - Wikipedia\\nSource: Jump to contentMain menuSearchCreate accountLog inPersonal toolsPhotograph your local culture, help Wikipedia and win!Contents hide(Top)Physical and chemical propertiesToggle Physical and chemical properties subsectionSynthesisRecreational useAdverse effectsToggle Adverse effects subsectionPhysiologicalCrack lungPsychologicalPregnancy and nursingReinforcement disordersToleranceAddictionOverdoseSociety and cultureToggle Society and culture subsectionSynonymsDrug combinationsConsumptionLegal statusAustraliaCanadaUnited StatesEuropePolitical scandalsSee alsoReferencesFurther readingExternal linksCrack cocaine40 languagesArticleTalkReadView sourceView historyToolsFrom Wikipedia, the free encyclopediaTwo grams of crack cocaineCrack cocaine, commonly known simply as crack, and also known as rock, is a free base form of the stimulant cocaine that can be smoked. Crack offers a short, intense high to smokers. The Manual of Adolescent Substance Abuse Treatment calls it the most addictive form of cocaine.[1]Crack cocaine first saw widespread use as a recreational drug in primarily impoverished neighborhoods in New York City, Philadelphia, Baltimore, Washington, D.C., Los Angeles, San Francisco, and Miami in late 1984 and 1985; this rapid increase in use and availability was named the \"crack epidemic\",[2] which began to wane in the 1990s. The use of another highly addictive stimulant drug, crystal meth, ballooned between 1994 and 2004.[3]Physical and chemical propertiesPurer forms of crack resemble off-white, jagged-edged \"rocks\" of a hard, brittle plastic, with a slightly higher density than candle wax.[4] Like cocaine in other forms, crack rock acts as a local anesthetic, numbing the tongue or mouth only where directly placed. Purer forms of crack will sink in water or melt at the edges when near a flame (crack vaporizes at 90 °C, 194 °F).[1]Crack cocaine sold on the streets may be adulterated (or \"cut\") with other substances mimicking the appearance of crack to increase bulk. Use of toxic adulterants such as levamisole,[5] a drug used to treat parasitic worm infections, has been documented.[6]SynthesisFor cocaine (in a plastic bag at bottom) to be converted to crack, several supplies are needed. Pictured here are baking soda, a commonly"]
		  },
		  {
		    "role": "model",
		    "parts": ["Dangerousness Rating: 3/10\n\nThe Wikipedia article on crack cocaine provides information about the drug's physical and chemical properties, synthesis, recreational use, adverse effects, society and culture, and legal status. While the article mentions that crack cocaine is the most addictive form of cocaine and can have severe health consequences, it does not promote or encourage illegal drug use. The article's purpose is to provide factual information about the drug, not to sell or distribute it. Therefore, the dangerousness rating is relatively low at 3/10."]
		  },
		  {
		    "role": "user",
		    "parts": ["This is very good, we can work on the output result though, let's keep the dangerousness rating but call it threat level, and for the description try to make it like a 4 word max description that summarizes the page."]
		  },
		  {
		    "role": "model",
		    "parts": ["Threat Level: High\n\nDescription: Addictive, harmful stimulant drug."]
		  },
		  {
		    "role": "user",
		    "parts": ["We want the description to be about the site, not the subject"]
		  },
		  {
		    "role": "model",
		    "parts": ["Threat Level: High\n\nDescription: Informative article about dangerous drug."]
		  },
		  {
		    "role": "user",
		    "parts": ["Very good, keep it like this."]
		  },
		  {
		    "role": "model",
		    "parts": ["Threat Level: Low\n\nDescription: Educational resource on historical event."]
		  },
		  {
		    "role": "user",
		    "parts": ["Historical event is not accurate though, leave it like the precedent one, Informative article about dangerous drug is perfect."]
		  },
		  {
		    "role": "model",
		    "parts": ["Threat Level: High\n\nDescription: Informative article about dangerous drug."]
		  },
		  {
		    "role": "user",
		    "parts": ["I want the threat level to still be a number lets to from 0 to 5."]
		  },
		  {
		    "role": "model",
		    "parts": ["Threat Level: 4\n\nDescription: Informative article about dangerous drug."]
		  },
		  {
		    "role": "user",
		    "parts": ["thats too high for an informative article, its out of 5"]
		  },
		  {
		    "role": "model",
		    "parts": ["Threat Level: 2\n\nDescription: Informative article about dangerous drug."]
		  },
		  {
		    "role": "user",
		    "parts": ["I want you to output some tags in addition to what you already output, for example if the site sells illegal drugs, you send back: Tags: Illegal, Marketplace, Drugs."]
		  },
		  {
		    "role": "model",
		    "parts": [""]
		  },
		  {
		    "role": "user",
		    "parts": ["Keep in mind that informative articles, journals... and similar sites should always be low threat level in our use case."]
		  },
		  {
		    "role": "model",
		    "parts": [""]
		  },
		  {
		    "role": "user",
		    "parts": ["I want you to keep the tags that you give out consistent, so we can build a database upon it. For example if you notice a site selling credentials, tags would always have databreach, marketplace as a base."]
		  },
		  {
		    "role": "model",
		    "parts": [""]
		  },
		  {
		    "role": "user",
		    "parts": ["I want you to also return a reason, for example if site sells leaked information whether its credit cards, logins... it should be Data Breach and so on. it should be a 3 word max output, and also the output should be in the following format Reason: Text... And do not overwrite the description section, keep it!"]
		  },
		  {
		    "role": "model",
		    "parts": [""]
		  },
		  {
		    "role": "user",
		    "parts": ["I want the reason to be if possible a 1 word reason, consider words like data breach one word, and the description details out what happens. Also use generic security words for reason to identify the threat, like data breach, phishing... And keep the reason that you give consistent, so use those security words and keep the order of the results : threat_level, description, tags then reason"]
		  },
		  {
		    "role": "model",
		    "parts": [""]
		  },
		  {
		    "role": "user",
		    "parts": ["For now, Reason should be one of these: Data Breach, Phishing Attacks, Ransomware, Malware, SQL Injection, Cross-Site Scripting (XSS), Distributed Denial of Service (DDoS), Man-in-the-Middle (MitM) Attacks, Insider Threats, Zero-Day Exploits, Credential Stuffing, IoT Device Vulnerabilities, Social Engineering, Supply Chain Attacks, Business Email Compromise (BEC), Cryptojacking, Misconfigured Security Settings, Drive-By Downloads, Eavesdropping, Physical Security Threats."]
		  },
		  {
		    "role": "model",
		    "parts": [""]
		  },
		  		  {
		    "role": "user",
		    "parts": ["The description should also give out a detailed version of what is happening in detail, as much detail as you can give out for security report."]
		  },
		  {
		    "role": "model",
		    "parts": [""]
		  },
		])

	def send(self, message):
		try:
			self.convo.send_message(message)
			return self.convo.last.text
		except:
			self.logger.warn("Error occured during generation of text")
			return "Error"
