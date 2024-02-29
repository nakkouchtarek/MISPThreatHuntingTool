# MISPThreatHuntingTool

Threat hunting tool for Darkweb crawling to find keywords, detect phishing domains and scan files for keywords and stolen credit cards.

![Capture](https://github.com/nakkouchtarek/MISPThreatHuntingTool/assets/98561646/0256d0d9-9ccc-485f-90df-448348db13d0)

# Install

You will be needing Firefox, MISP, Tor and python already installed. Now you gotta install the required python packages

'''
pip install -r requirements.txt
'''

You will also be needing a Gemini API key to integrate with this, as you will fill in your Gemini API key and MISP API key in the .env file.

# Usage

Before starting for all first 3 modes, you will need to fill the blacklist file with words to detect while crawling / scanning.

![image](https://github.com/nakkouchtarek/MISPThreatHuntingTool/assets/98561646/b466f769-1cc6-4306-ac31-96bd16e01974)

## DarkWeb Crawler

For this mode, you will need a file filled with urls to start crawling from, for example : 

![image](https://github.com/nakkouchtarek/MISPThreatHuntingTool/assets/98561646/6ca21853-3852-4081-8db5-902d117d15f4)

And now you can start the crawler through the following command : 

![image](https://github.com/nakkouchtarek/MISPThreatHuntingTool/assets/98561646/593bbd77-bfa1-4635-9781-ccdd45ec77a1)







