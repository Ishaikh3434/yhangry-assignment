import getpass
import constants as c
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
def __prompt_email_password():
  u = input("Email: ")
  p = getpass.getpass(prompt="Password: ")
  return (u, p)

def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

def login(driver, email=None, password=None, cookie = None, timeout=10):
    if cookie is not None:
        return _login_with_cookie(driver, cookie)
  
    if not email or not password:
        email, password = __prompt_email_password()
  
    driver.get("https://www.linkedin.com/login")
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
  
    email_elem = driver.find_element(By.ID,"username")
    email_elem.send_keys(email)
  
    password_elem = driver.find_element(By.ID,"password")
    password_elem.send_keys(password)
    password_elem.submit()
  
    if driver.current_url == 'https://www.linkedin.com/checkpoint/lg/login-submit':
        remember = driver.find_element(By.ID,c.REMEMBER_PROMPT)
        if remember:
            remember.submit()
  
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, c.VERIFY_LOGIN_ID)))
  
def _login_with_cookie(driver, cookie):
    driver.get("https://www.linkedin.com/login")
    driver.add_cookie({
      "name": "li_at",
      "value": cookie
    })

def peopleSearchQuery(queryterm:str, driver=None):
    queryterm.replace(" ","%20")
    delay=10
    driver.get("https://www.linkedin.com/search/results/people/?keywords="+queryterm)

    scrapedAccounts = []
    divClass="dmnbVMzYktilnSsxiskVuRaAxFRuizCyniJQA"
    try:
        people = driver.find_elements(By.XPATH, f"//div[@class='{divClass}']")
        print(f"found {len(people)} results!")
    except Exception as e:
        print("Can't find element!", e)
        return scrapedAccounts

    for index in range(len(people)):
        try:
            people = driver.find_elements(By.XPATH, f"//div[@class='{divClass}']")
            thiselement = people[index]
            thiselement.click()
            sleep(1)
            noAccess=driver.find_elements(By.XPATH, "//button[@class='fr artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
            print(noAccess)
            if noAccess:
                print("No Access to Account!")
                overlay=driver.find_element(By.XPATH, "//button[@class='fr artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
                overlay.click()
                raise TimeoutError
            scrapedAccounts.append(driver.current_url)

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@data-field='browsemap_card_click']"))
                )
            moreAccounts=driver.find_elements(By.XPATH, "//a[@data-field='browsemap_card_click']")
            print(len(moreAccounts))
            moreLinks=[elem.get_attribute('href') for elem in moreAccounts]
            scrapedAccounts+=moreLinks

            driver.execute_script("window.history.go(-1)")
            
        except Exception as e:
            print("Error processing element:", e)
            continue

    return scrapedAccounts

