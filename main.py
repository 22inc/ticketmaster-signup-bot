# ARGS AND RUN COMMAND
# typer (filename).py run YOUR_PROFILE_NAME DECLARED_MODULE PERSON/EVENT/WEBSITE

import os
import time
import random
import requests
import json
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import platform
import keyboard
from universalclear import clear
import typer

app = typer.Typer()

# chromedriver_autoinstaller.install()

ticketmasterAccountList = []

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

def readProxies():
    with open('proxies.txt', 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def getRandomProxy(proxies):
    if proxies:
        return random.choice(proxies)
    else:
        print("No proxies found. Running without proxy.")
        return None

def configureDriver(proxy):
    global driver
    chromeOptions = Options()
    
    if proxy:
        chromeOptions.add_argument('--proxy-server=%s' % proxy)
    
 #   chromeOptions.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0")

    driver = webdriver.Chrome(options=chromeOptions)

    return driver

def isTextPresent(text):
    try:
        # Wait for up to 10 seconds for the text to be present
        elementPresent = EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
        WebDriverWait(driver, 10).until(elementPresent)
        return True
    except:
        return False
    
def holdKeyforDuration(key, duration):
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)

def ticketmasterAccountDefine(profile, module, selected):
    global ticketmasterAccountList
    
    # Clear the list first
    ticketmasterAccountList = []

    # Read the accounts from the file and store them as tuples in a list
    with open("ticketmaster_accounts.txt", "r") as file:
        for line in file:
            # Split the line into email and password
            email, password = line.strip().split(":")
            account = (email, password)
            
            # Append the account to the list
            ticketmasterAccountList.append(account)

    print("Accounts loaded:", ticketmasterAccountList)
    time.sleep(1)
    clear()
    print("Ticketmaster module loading...")
    ticketmasterModule(profile, module, selected)


def markAccountAsUsed(email, password):
    # Mark an account as used by adding a '#' in front of it in the file
    with open("ticketmaster_accounts.txt", "r") as file:
        lines = file.readlines()

    with open("ticketmaster_accounts.txt", "w") as file:
        for line in lines:
            if f"{email}:{password}" in line:
                line = "#" + line.lstrip('#')
            file.write(line)

def getUnusedAccount():
    for email, password in ticketmasterAccountList:
        return email, password
    return None, None

def ticketmasterLogin(profile, module, selected):
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
            time.sleep(5)
            while isTextPresent("Let's Get Your Identity Verified"):
                time.sleep(5)
                holdKeyforDuration('enter', 10)
                print("First anti-bot done succesfuly.")
                return
            
            #actions.send_keys(Keys.TAB).perform()
            #time.sleep(5)
            #holdKeyforDuration('enter', 10)
            #print("Second anti-bot done succesfuly.")

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

            print("Details entered successfully.")

            signInButton = driver.find_element(By.XPATH, "//span[text()='Sign in']")
            signInButton.click()
            print("Sign in button clicked.")

            actions.send_keys(Keys.TAB).perform()
            time.sleep(1)

            while isTextPresent("Let's Get Your Identity Verified"):
                time.sleep(5)
                holdKeyforDuration('enter', 10)
                print("Second anti-bot done succesfuly.")
                return


        except Exception as e:
            print("Failed to enter email: ", e)
        
        print("Anti-bot done successfully.")

    else:
        print("No unused accounts available.")

    input("")

    markAccountAsUsed(email, password)
    
def ticketmasterModule(profile, module, selected):
    global driver, actions
    proxies = readProxies()
    
    proxy = getRandomProxy(proxies)

    clear()

    print(f"Selected Proxy: {proxy}")

    driver = configureDriver(proxy)
    driver.get('https://registration.ticketmaster.com/' + selected)

    actions = ActionChains(driver)

    clear()
    print("Now loading " + driver.title + "...")

    ticketmasterLogin(profile, module, selected)

def shopifyProductFound():
    r = requests.get(productUrl)
    print(productUrl)
    exit()

def shopifyModule(profile, module, selected):
    global productUrl
    proxies = readProxies()
    
    selectedProxy = getRandomProxy(proxies)

    clear()
    shopifySelectedUrl = 'https://www.' + selected + '.com/' + 'products.json'

    desiredProduct = input("What product do you want? ") 
    clear()

    print(f"Selected Proxy: {selectedProxy}")

    while True:
        r = requests.get(shopifySelectedUrl)
        products = json.loads(r.text)['products']

        found = False

        for product in products:
            productName = product['title'].lower()

            if desiredProduct.lower() in productName:
                print("Checking for product.")
                found = True
                print(f"Found product: {product['title']}")
                productUrl = 'https://www.' + selected + '.com/products/' + product['handle']
                shopifyProductFound()

        if not found:
            print(f"No product matching '{desiredProduct}' found. Waiting...")
            time.sleep(3.333)
            

    clear() 
    # print("Now loading " + driver.title + "...")

    input("")

@app.command()
def profile(profile: str, module: str, selected: str):
    profileSelect(profile, module, selected)

def profileSelect(profile, module, selected):
    global pName, pEmail, pShippingAddress, pShippingSecondary, pShippingCity, pShippingZipCode, pShippingState, pShippingPhone, pBillingAddress, pBillingSecondary, pBillingCity, pBillingZipCode, pBillingState, pBillingPhone

    

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
            # ... (other shipping variables)

            # Define billing variables from the selected profile.
            if "Billing Address:" in line:
                pBillingAddress = line.split("Billing Address: ")[1].strip()
            # ... (other billing variables)

    clear()
    
    print("Your profile has been loaded.")

    loadSite(profile, module, selected)

def loadSite(profile, module, selected):
    clear()

    if module.lower() == 'ticketmaster':
        clear()
        print("Ticketmaster Module Loading!")
        ticketmasterAccountDefine(profile, module, selected)
    elif module.lower() == 'shopify':
        clear()
        print("Shopify Module Loading!")
        shopifyModule(profile, module, selected)
    else:
        print("Invalid module choice.")
        time.sleep(2.5)
        exit()

if __name__ == "__main__":
    app()