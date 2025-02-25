import actions
from person import Person
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
import csv

def CSVExport(linkList:list, driver:None):
    fieldnames=["linkedin_url","name","education","experience"]
    with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        processedLinks=[]
        for link in linkList:
            print(f"Processing link: {link}")
            thisPerson=None
            try:
                if link not in processedLinks:
                    processedLinks.append(link)
                    
                    thisPerson=Person(link, driver=driver,close_on_complete=False)
                    writer.writerow({
                    "linkedin_url":thisPerson.linkedin_url,
                    "name":thisPerson.name,
                    "education":thisPerson.educations,
                    "experience":thisPerson.experiences
                                    })
                else:
                    print('skipped!')
            except:
                print("skipped!")
                pass

    print("Export Success!")

options=Options()
service=Service(executable_path=binary_path)

# Add various options to make the browser more stable
options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

driver = webdriver.Chrome(service=service, options=options)

email = "scraypehr@myyahoo.com"
password = "hiremeplease"

actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal

modifiers = [   #These Modifiers can be used to expand the range of searched terms
    "Sous", "Head", "de Partie", "Executive", "New York", "Restaurant", "Experienced", "Pan-Asian", "Fine Dining", "Tapas", "Fusion", "Line Cook", "Gourmet"
]

compiledList=[]
for state in modifiers:
    people=actions.peopleSearchQuery(f"{state} Chef", driver=driver)
    compiledList+=people

print(f"Compiled List: {compiledList}")


CSVExport(compiledList,driver=driver)


