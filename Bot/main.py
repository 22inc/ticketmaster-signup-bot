import os
import time
import chromedriver_autoinstaller
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

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

            # Define basic variables from the selected profile.
            if "Name:" in line:
                pName = line.split("Name: ")[1].strip()
            if "Email:" in line:
                pEmail = line.split("Email: ")[1].strip()

            # Define shipping variables from the selected profile.
            if "Shipping Address:" in line:
                pShippingAddress = line.split("Shipping Address: ")[1].strip()
            if "Shipping Secondary:" in line:
                pShippingSecondary = line.split("Shipping Secondary: ")[1].strip()
            if "Shipping City:" in line:
                pShippingCity = line.split("Shipping City: ")[1].strip()
            if "Shipping Zip Code:" in line:
                pShippingZipCode = line.split("Shipping Zip Code: ")[1].strip()
            if "Shipping State:" in line:
                pShippingState = line.split("Shipping State: ")[1].strip()
            if "Shipping Phone:" in line:
                pShippingPhone = line.split("Shipping Phone: ")[1].strip()

            # Define billing variables from the selected profile.
            if "Billing Address:" in line:
                pBillingAddress = line.split("Billing Address: ")[1].strip()
            if "Billing Secondary:" in line:
                pBillingSecondary = line.split("Billing Secondary: ")[1].strip()
            if "Billing City:" in line:
                pBillingCity = line.split("Billing City: ")[1].strip()
            if "Billing Zip Code:" in line:
                pBillingZipCode = line.split("Billing Zip Code: ")[1].strip()
            if "Billing State:" in line:
                pBillingState = line.split("Billing State: ")[1].strip()
            if "Billing Phone:" in line:
                pBillingPhone = line.split("Billing Phone: ")[1].strip()

    os.system("cls")
    print("Your profile has been loaded.")
    
    loadSite()

def ticketmasterAccountDefine():
    global account
    with open("ticketmaster_accounts.txt", "r") as file:
        for line in file:
            email, password = line.strip().split(":")
            
            account = f"{email}:{password}"
            ticketmasterAccountList.append(account)
        for account in ticketmasterAccountList:
            print(account)

    os.system("cls")    

    print("Accounts loaded. ")
    time.sleep(1)
    os.system("cls")    

    print("Ticketmaster module loading... ")
    time.sleep(5)
    ticketmasterModule()

def ticketmasterLogin():
    try:
        time.sleep(5)
        button = driver.find_element(By.ID, 'company-logo')
        button.click()
        print("Button clicked successfully. ")

    except Exception as e:
        print("Failed to click the button: ", e)

    try:
        time.sleep(5)
        email_input = driver.find_element(By.XPATH, "//input[@placeholder='email']")
        
        email_input.clear()
        
        email_input.send_keys("your_email@example.com")
        
        print("Email entered successfully.")

    except Exception as e:
        print("Failed to enter email: ", e)

    input("")


def ticketmasterModule():
    global driver

    os.system("cls")
    ticketmasterSelected = input("What/who are we going for? ")
    os.system("cls")

    driver = webdriver.Chrome()
    driver.get('https://registration.ticketmaster.com/' + ticketmasterSelected)

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