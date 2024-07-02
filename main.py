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

global pName, pEmail, pFirstName, pLastName, pShippingAddress, pShippingSecondary, pShippingCity, pShippingZipCode, pShippingState, pShippingPhone, pBillingAddress, pBillingSecondary, pBillingCity, pBillingZipCode, pBillingState, pBillingPhone, pCardNumber, pExpirationDate, pSecurityCode, driver

def readProxies():
    with open('files/proxies.txt', 'r') as file:
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
        elementPresent = EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
        WebDriverWait(driver, 10).until(elementPresent)
        return True
    except Exception as e:
        print("Error whilst checking if text is present: ", e)
        return False
    
def holdKeyforDuration(key, duration):
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)

def loadTicketmasterAccounts(profile, module, selected):
    global ticketmasterAccountList
    
    ticketmasterAccountList = []

    with open("files/ticketmaster_accounts.txt", "r") as file:
        for line in file:
            email, password = line.strip().split(":")
            account = (email, password)
            
            ticketmasterAccountList.append(account)

    print("Accounts loaded:", ticketmasterAccountList)
    time.sleep(1)
    clear()
    print("Ticketmaster module loading...")
    ticketmasterModule(profile, module, selected)


def markAccountAsUsed(email, password):
    with open("files/ticketmaster_accounts.txt", "r") as file:
        lines = file.readlines()

    with open("files/ticketmaster_accounts.txt", "w") as file:
        for line in lines:
            if f"{email}:{password}" in line:
                line = "#" + line.lstrip('#')
            file.write(line)

def getUnusedAccount():
    for email, password in ticketmasterAccountList:
        return email, password
    return None, None

def ticketmasterLogin(profile, module, selected):
    try:
        emailInput = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'email'))
        )
        emailInput.send_keys(email)
        print("Email entered successfully.")

        passwordInput = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'password'))
        )
        passwordInput.send_keys(password)
        print("Password entered successfully.")

        signInButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))
        )
        signInButton.click()
        print("Sign in button clicked.")

        time.sleep(5)

        while isTextPresent("Let's Get Your Identity Verified"):
            time.sleep(5)
            action = ActionChains(driver)
            action.key_down(Keys.ENTER).pause(15).key_up(Keys.ENTER).perform()
            time.sleep(5)
            print("Second anti-bot done successfully.")
            return

    except Exception as e:
        print("Failed during login: ", e)

    print("Login process completed successfully.")

    input("Press Enter to continue...")

    markAccountAsUsed(email, password)

def ticketmasterAntiBot(profile, module, selected):
    global driver, actions, email, password

    email, password = getUnusedAccount()

    if email is not None:
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'company-logo'))
            )
            button.click()
            print("Sign in started.")

        except Exception as e:
            print("Failed to click the button: ", e)

        antibot_attempts = 0
        max_attempts = 3

        while antibot_attempts < max_attempts:
            if isTextPresent("Please verify you are a human"):
                print(f"Anti-bot attempt {antibot_attempts + 1} of {max_attempts}!")

                try:
                    time.sleep(5)
                    ActionChains(driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()
                    time.sleep(1)

                    action = ActionChains(driver)
                    action.key_down(Keys.ENTER).pause(15).key_up(Keys.ENTER).perform()
                    print(f"Completed anti-bot attempt {antibot_attempts + 1}!")
                    time.sleep(5)
                    clear()

                    if isTextPresent("Please verify you are a human"):
                        antibot_attempts += 1                        
                        if antibot_attempts >= max_attempts:
                            print(f"Exceeded {max_attempts} attempts. Quitting.")
                            return  # Exit the function or script

                        print("Re-doing anti-bot!")
                    else:
                        print("Passed anti-bot!")
                        time.sleep(2.5)
                        ticketmasterLogin(profile, module, selected)

                except Exception as e:
                    print(f"Failed to do anti-bot attempt {antibot_attempts + 1}: {e}")

        if antibot_attempts == 0:
            print("No antibot verification required or successful.")
            ticketmasterLogin(profile, module, selected)

    else:
        print("No unused accounts available.")
    
def ticketmasterModule(profile, module, selected):
    proxies = readProxies()
    proxy = getRandomProxy(proxies)

    print(f"Selected Proxy: {proxy}")

    clear()
    driver = configureDriver(proxy)
    driver.get(f'https://registration.ticketmaster.com/{selected}')

    try:
        print(f"Now loading {driver.title}...")
        ticketmasterAntiBot(profile, module, selected)

    except Exception as e:
        print(f"Error in Ticketmaster module: {e}")

    finally:
        driver.quit()


def shopifyCheckout():
    global driver, actions, wait
    actions = ActionChains(driver)

    if productUrl is not None:
        try:
            checkoutButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Checkout']")))

            checkoutButton.click()
            print("Checkout initiated.")

            actions.send_keys(pEmail).perform()            
            actions.send_keys(Keys.TAB).perform()            
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(pFirstName).perform()            
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(pLastName).perform()            
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(pShippingAddress).perform()   
            actions.send_keys(Keys.TAB).perform()     
            actions.send_keys(pShippingSecondary).perform()   
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(pShippingCity).perform()    
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(pShippingState).perform() 
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(pShippingZipCode).perform()
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(pShippingPhone).perform()   
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(Keys.TAB).perform()

            print("Shipping details filled.")

            actions.send_keys(pCardNumber).perform() 
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(pExpirationDate).perform()   
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(pSecurityCode).perform()   
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys(Keys.TAB).perform()
            try:
                checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='Checkbox1']")))
                checkbox.click() 
            except Exception as e:
                print("Failed whilst agreeing to the TOS: ", e)
            #actions.send_keys(Keys.TAB).perform()
            #actions.send_keys(Keys.TAB).perform()
            #actions.send_keys(Keys.TAB).perform()
            time.sleep(5)
            print("Ready to checkout!")
            #checkout time

        except Exception as e:
            print("Failed to initiate the checkout: ", e)

def shopifyAddToCart():
    global driver, actions, wait

    if productUrl is not None:
        try:

            wait = WebDriverWait(driver, 10)
            addToCartButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Add to Cart']")))

            addToCartButton.click()
            print("Add to cart initiated.")

            shopifyCheckout()
            
        except Exception as e:
            print("Failed to add to cart: ", e)

def shopifyProductFound():
    proxies = readProxies()
    
    proxy = getRandomProxy(proxies)
    
    clear()

    driver = configureDriver(proxy)
    driver.get(productUrl)

    clear()

    print(f"Selected Proxy: {proxy}")
    print("Now loading " + driver.title + "...")
    print(productUrl)

    time.sleep(2.5)
    shopifyAddToCart()


def shopifyModule(profile, module, selected):
    global productUrl
    proxies = readProxies()
    
    selectedProxy = getRandomProxy(proxies)

    clear()
    shopifySelectedUrl = 'https://' + selected + '.com/' + 'products.json'

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
                time.sleep(2.5)
                shopifyProductFound()

        if not found:
            print(f"No product matching '{desiredProduct}' found. Waiting...")
            time.sleep(3.333)

@app.command()
def profile(profile: str, module: str, selected: str):
    profileSelect(profile, module, selected)

def profileSelect(profile, module, selected):
    global pName, pFirstName, pLastName, pEmail, pShippingAddress, pShippingSecondary, pShippingCity, pShippingZipCode, pShippingState, pShippingPhone, pBillingAddress, pBillingSecondary, pBillingCity, pBillingZipCode, pBillingState, pBillingPhone,  pCardNumber, pExpirationDate, pSecurityCode

    

    with open("files/profile_" + profile + ".txt", "r") as profile_file:
        for line in profile_file:
            print(line)

            if "Name:" in line:
                pName = line.split("Name: ")[1].strip()
                name_parts = pName.split(' ')
                if len(name_parts) >= 2:
                    pFirstName = name_parts[0]
                    pLastName = name_parts[1]
                else:
                    print("Profile First Name / Last Name not filled out correctly!")
            if "Email:" in line:
                pEmail = line.split("Email: ")[1].strip()
                


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
            
            if "Card Number:" in line:
                pCardNumber = line.split("Card Number: ")[1].strip()
            if "Expiration Date:" in line:
                pExpirationDate = line.split("Expiration Date: ")[1].strip()
            if "Security Code:" in line:
                pSecurityCode = line.split("Security Code: ")[1].strip()


    clear()
    
    print("Your profile has been loaded.")

    loadSite(profile, module, selected)

def loadSite(profile, module, selected):
    clear()

    if module.lower() == 'ticketmaster':
        clear()
        print("Ticketmaster Module Loading!")
        loadTicketmasterAccounts(profile, module, selected)
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
    ticketmasterModule("profile", "ticketmaster", "selected")