# MISPThreatHuntingTool

Threat hunting tool for Darkweb crawling to find keywords, detect phishing domains and scan files for keywords.

![image](https://github.com/nakkouchtarek/MISPThreatHuntingTool/assets/98561646/12773443-d619-4e5f-a40f-21e36a94b30d)

# Install

You will be needing Firefox, MISP, Tor and python already installed. Now you gotta install the required python packages

```
pip install -r requirements.txt
```

You will also be needing a Gemini API key to integrate with this, as you will fill in your Gemini API key and MISP API key in the .env file.

# Files to know

In core you will find certain files : 

- blacklist : list of blacklisted words you want to look for when searching with all operations except for binchecker
- progress : tracks the progress of your darkweb crawling, can reset it by setting the value of COUNT to 0
- blacklist_urls : list of urls that ahmia specified as containing abuse material which we will avoid, so we filter them out when crawling
- tlds_dict : list of top level domains to use when looking for possible phishing domains
- user_agents : list of user agents to rotate through while working with the tool

Files you can change would be blacklist, bin and progress when you want to reset progress.

# Usage

Before starting for all first 3 modes, you will need to fill the blacklist file with words to detect while crawling / scanning.

![image](https://github.com/nakkouchtarek/MISPThreatHuntingTool/assets/98561646/b466f769-1cc6-4306-ac31-96bd16e01974)

## DarkWeb Crawler

For this mode, you will need a file filled with urls to start crawling from, for example : 

![image](https://github.com/nakkouchtarek/MISPThreatHuntingTool/assets/98561646/6ca21853-3852-4081-8db5-902d117d15f4)

And now you can start the crawler through the following command : 

![image](https://github.com/nakkouchtarek/MISPThreatHuntingTool/assets/98561646/593bbd77-bfa1-4635-9781-ccdd45ec77a1)

Each encountered blacklisted word would be sent as an event towards MISP

## Phishing Domain Detector

You can use the following command to detect phishing domains for your domain, with a file containing your domains of course :

```
python main.py phishing domains.txt
```

## File Checker

This will check for blacklisted words inside your file and send events towards MISP when something is flagged :

```
python main.py filechecker file.txt
```






