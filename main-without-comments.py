import os
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

chromedriver_autoinstaller.install()

pName = ""
pEmail = ""
pShippingAddress = ""
pShippingSecondary = ""
pShippingCity = ""
pShippingZipCode = ""
pShippingState = ""
pShippingPhone = ""
pBillingAddress = ""
pBillingSecondary = ""
pBillingCity = ""
pBillingZipCode = ""
pBillingState = ""
pBillingPhone = ""

driver = ""
ticketmasterAccountList = []

def profileSelect():
    global pName, pEmail, pShippingAddress, pShippingSecondary, pShippingCity, pShippingZipCode, pShippingState, pShippingPhone, pBillingAddress, pBillingSecondary, pBillingCity, pBillingZipCode, pBillingState, pBillingPhone

    os.system("cls")
    profile = input("Which profile would you like to use? ")

    with open("profile_" + profile + ".txt", "r") as profile_file:
        for line in profile_file:
            print(line)

            if "Name:" in line:
                pName = line.split("Name: ")[1].strip()
            if "Email:" in line:
                pEmail = line.split("Email: ")[1].strip()

            if "Shipping Address:" in line:
                pShippingAddress = line.split("Shipping Address: ")[1].strip()

            if "Billing Address:" in line:
                pBillingAddress = line.split("Billing Address: ")[1].strip()

    os.system("cls")
    print("Your profile has been loaded.")
    
    loadSite()

def ticketmasterAccountDefine():
    global account, email, password

    with open("ticketmaster_accounts.txt", "r") as file:
        for line in file:
            email, password = line.strip().split(":")
            account = (email, password)
            
            ticketmasterAccountList.append(account)

        for account in ticketmasterAccountList:
            print(account)

    os.system("cls")    

    print("Accounts loaded.")
    os.system("cls")

    print("Ticketmaster module loading...")
    ticketmasterModule()

def markAccountAsUsed():
    with open("ticketmaster_accounts.txt", "r") as file:
        lines = file.readlines()
    with open("ticketmaster_accounts.txt", "w") as file:
        for line in lines:
            if f"{email}:{password}" in line:
                line = "#" + line
            file.write(line)

def getUnusedAccount():
    for email, password in ticketmasterAccountList:
        if not email.startswith("#"):
            return email, password
    return None, None

def ticketmasterLogin():
    global driver, actions

    email, password = getUnusedAccount()

    if email is not None:
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'company-logo'))
            )
            button.click()
            print("Button clicked successfully.")

        except Exception as e:
            print("Failed to click the button: ", e)

        try:
            time.sleep(10)

            actions.send_keys(Keys.TAB).perform()
            time.sleep(1)

            actions.send_keys(Keys.TAB).perform()
            time.sleep(1)
            
            actions.send_keys(Keys.TAB).perform()
            time.sleep(1)

            actions.send_keys(email).perform()
            time.sleep(1)
    
            actions.send_keys(Keys.TAB).perform()
            time.sleep(1)

            actions.send_keys(password).perform()
            time.sleep(1)
            
            actions.send_keys(Keys.TAB).perform()
            time.sleep(1)

            actions.send_keys(Keys.TAB).perform()
            time.sleep(1)
 
            actions.send_keys(Keys.TAB).perform()
            time.sleep(1)
 
            actions.send_keys(Keys.TAB).perform()
            time.sleep(1)
 
            actions.send_keys(Keys.TAB).perform()
            time.sleep(1)
 
            actions.send_keys(Keys.TAB).perform()
            time.sleep(1)

            print("Details entered successfully.")

            actions.send_keys(Keys.RETURN).perform()

            time.sleep(5)

            actions.send_keys(Keys.TAB).perform()

        except Exception as e:
            print("Failed to enter email: ", e)

#        actions.send_keys(Keys.TAB).perform()
#        actions.send_keys(Keys.RETURN).perform(time.sleep(10))
        
        print("Anti-bot done successfully.")

    else:
        print("No unused accounts available.")

    input("")
    
    markAccountAsUsed()

def ticketmasterModule():
    global driver, actions

    os.system("cls")
    ticketmasterSelected = input("What/who are we going for? ")
    os.system("cls")

    driver = webdriver.Chrome()
    driver.get('https://registration.ticketmaster.com/' + ticketmasterSelected)

    actions = ActionChains(driver)

    os.system("cls") 
    print("Now loading " + driver.title + "...")

    ticketmasterLogin()

def loadSite():
    os.system("cls")
    selectedModule = input("What module would you like to load? ")

    if selectedModule.lower() == 'ticketmaster':
        os.system("cls")
        ticketmasterAccountDefine()
    elif selectedModule.lower() == 'shopify':
        print("Shopify module loading... ")
    else:
        print("Invalid module choice.")
        loadSite()

profileSelect()
