My submission for a method to grab details of prospective leads for follow-up contact. 
The method I've employed utilised a modified LinkedIn Scraper (based on https://github.com/joeyism/linkedin_scraper/). 


This program is a bot that undergoes two operations: scanning, then scraping
Initially, using search parameters defined by the user (the trial case was the term "Chef" preceeded by a modifier term, such as "Head", "Sous" or "Experienced"); resulting profiles are indexed for use in operation 2.
The second operation involves using the modified scraper to find key details on the potential lead: name, location, education, experience and about (the user's bio). This information is stored in a CSV file that can be indexed further to query specific details, such as the LinkedIn profile of the educational institute.

Setup Requirements: This project needs an installation of Google Chrome, as well as the applicable version of the Chrome Web Driver (https://developer.chrome.com/docs/chromedriver/downloads).
All customisation options are availible in main.py, the only file that's required to be run to deploy the bot.
