import sys
import os
import time
import random
import requests
import json
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import keyboard
from universalclear import clear
from typing import List, Tuple, Optional
import typer

app = typer.Typer()

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QStackedWidget, QListWidget, QListWidgetItem,
    QTextEdit
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Ensure PyQtWebEngine is installed
# pip install PyQtWebEngine

TicketmasterAccountList: List[Tuple[str, str]] = []

def AfterLoginProcess():
    print("Login completed!")
    time.sleep(3600)

def ReadProxies() -> List[str]:
    """
    Read proxies from the 'files/proxies.txt' file.

    Returns:
        List[str]: List of proxies.
    """
    try:
        with open('files/proxies.txt', 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        return proxies
    except FileNotFoundError:
        print("Proxies file not found. Ensure 'files/proxies.txt' exists.")
        return []
    except Exception as e:
        print(f"An error occurred while reading proxies: {e}")
        return []

def GetRandomProxy(proxies: List[str]) -> Optional[str]:
    """
    Get a random proxy from the list of proxies.

    Args:
        proxies (List[str]): List of proxies.

    Returns:
        Optional[str]: A random proxy or None if no proxies are available.
    """
    try:
        if proxies:
            return random.choice(proxies)
        else:
            print("No proxies found. Running without proxy.")
            return None
    except Exception as e:
        print(f"An error occurred while selecting a proxy: {e}")
        return None

def ConfigureDriver(proxy: Optional[str] = None) -> webdriver.Chrome:
    """
    Configure the Chrome WebDriver with or without a proxy.

    Args:
        proxy (Optional[str], optional): Proxy server address. Defaults to None.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver.
    """
    try:
        chromeOptions = Options()
        if proxy:
            chromeOptions.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(options=chromeOptions)
        return driver
    except Exception as e:
        print(f"An error occurred while configuring the WebDriver: {e}")
        raise

def IsTextPresent(driver: webdriver.Chrome, text: str, email: str, password: str, retries: int = 3) -> bool:
    """
    Check if the specified text is present on the page.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        text (str): The text to search for.
        email (str): The email for login.
        password (str): The password for login.
        retries (int, optional): Number of retries. Defaults to 3.

    Returns:
        bool: True if text is found, False otherwise.
    """
    for attempt in range(retries):
        try:
            elementPresent = EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
            WebDriverWait(driver, 5).until(elementPresent)
            print("Found the text! Sending to the next process.")
            return True
        except Exception as e:
            print("Text not detected, moving on to the next process!")
            TicketmasterLogin(driver, email, password)
    print(f"Failed to find text '{text}' after {retries} retries.")
    return False

def LoadTicketmasterAccounts(profile: str, selected: str):
    """
    Load Ticketmaster accounts from the 'files/ticketmaster_accounts.txt' file.

    Args:
        profile (str): The profile name.
        selected (str): The selected event or action.
    """
    global TicketmasterAccountList
    try:
        TicketmasterAccountList = []
        with open("files/ticketmaster_accounts.txt", "r") as file:
            for line in file:
                email, password = line.strip().split(":")
                TicketmasterAccountList.append((email, password))
        print(f"Accounts loaded: {TicketmasterAccountList}")
        time.sleep(1)
        clear()
        print("Ticketmaster module loading...")
        TicketmasterModule(profile, selected)
    except FileNotFoundError:
        print("Ticketmaster accounts file not found. Ensure 'files/ticketmaster_accounts.txt' exists.")
    except Exception as e:
        print(f"An error occurred while loading Ticketmaster accounts: {e}")

def MarkAccountAsUsed(email: str, password: str):
    """
    Mark a Ticketmaster account as used in the 'files/ticketmaster_accounts.txt' file.

    Args:
        email (str): The email of the account.
        password (str): The password of the account.
    """
    try:
        with open("files/ticketmaster_accounts.txt", "r") as file:
            lines = file.readlines()
        with open("files/ticketmaster_accounts.txt", "w") as file:
            for line in lines:
                if f"{email}:{password}" in line:
                    line = "#" + line.lstrip('#')
                file.write(line)
    except FileNotFoundError:
        print("Ticketmaster accounts file not found. Ensure 'files/ticketmaster_accounts.txt' exists.")
    except Exception as e:
        print(f"An error occurred while marking account as used: {e}")

def GetUnusedAccount() -> Tuple[Optional[str], Optional[str]]:
    """
    Get an unused Ticketmaster account.

    Returns:
        Tuple[Optional[str], Optional[str]]: Email and password of the unused account, or (None, None) if no unused accounts are available.
    """
    try:
        for email, password in TicketmasterAccountList:
            return email, password
        return None, None
    except Exception as e:
        print(f"An error occurred while getting an unused account: {e}")
        return None, None

def TicketmasterLogin(driver: webdriver.Chrome, email: str, password: str):
    """
    Perform login on Ticketmaster.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        email (str): The email for login.
        password (str): The password for login.
    """
    try:
        time.sleep(1)
        emailInput = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'email')))
        emailInput.send_keys(email)
        print("Email entered successfully.")
    except Exception as e:
        print(f"Failed to enter email: {e}")
        return

    try:
        time.sleep(1)
        passwordInput = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'password')))
        passwordInput.send_keys(password)
        print("Password entered successfully.")
    except Exception as e:
        print(f"Failed to enter password: {e}")
        return

    try:
        time.sleep(1)
        signInButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']")))
        signInButton.click()
        print("Sign in button clicked.")
    except Exception as e:
        print(f"Failed to click sign in button: {e}")
        return

    try:
        time.sleep(5)
        action = ActionChains(driver)
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        time.sleep(1)
        action.key_down(Keys.ENTER).pause(15).key_up(Keys.ENTER).perform()
        print("Second anti-bot completed, login should have been completed!")
    except Exception as e:
        print(f"Error during second anti-bot process: {e}")
    print("Login process completed successfully.")
    AfterLoginProcess()

def TicketmasterAntiBot(driver: webdriver.Chrome):
    """
    Handle anti-bot verification on Ticketmaster.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
    """
    email, password = GetUnusedAccount()
    if email:
        try:
            time.sleep(2.5)
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'company-logo')))
            button.click()
            print("Sign in started.")
        except Exception as e:
            print(f"Failed to click the button: {e}")

        antibotAttempts = 0
        maxAttempts = 3

        while antibotAttempts < maxAttempts:
            if IsTextPresent(driver, "Please verify you are a human", email, password):
                clear()
                print(f"Anti-bot attempt {antibotAttempts + 1} of {maxAttempts}!")
                try:
                    time.sleep(5)
                    ActionChains(driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()
                    time.sleep(1)
                    action = ActionChains(driver)
                    action.key_down(Keys.ENTER).pause(15).key_up(Keys.ENTER).perform()
                    print(f"Completed anti-bot attempt {antibotAttempts + 1}!")
                    time.sleep(5)
                    clear()
                    if IsTextPresent(driver, "Please verify you are a human", email, password):
                        antibotAttempts += 1
                        if antibotAttempts >= maxAttempts:
                            print(f"Exceeded {maxAttempts} attempts. Quitting.")
                            return
                        print("Re-doing anti-bot!")
                    else:
                        print("Passed anti-bot!")
                        time.sleep(2.5)
                        TicketmasterLogin(driver, email, password)
                        return
                except Exception as e:
                    print(f"Failed to do anti-bot attempt {antibotAttempts + 1}: {e}")
        if antibotAttempts == 0:
            print("No antibot verification required or successful.")
            TicketmasterLogin(driver, email, password)
    else:
        print("No unused accounts available.")

def TicketmasterModule(profile: str, selected: str):
    """
    Run the Ticketmaster module.

    Args:
        profile (str): The profile name.
        selected (str): The selected event or action.
    """
    proxies = ReadProxies()
    proxy = GetRandomProxy(proxies)
    print(f"Selected Proxy: {proxy}")
    clear()
    try:
        driver = ConfigureDriver(proxy)
        driver.get(f'https://registration.ticketmaster.com/{selected}')
        print(f"Now loading {driver.title}...")
        TicketmasterAntiBot(driver)
    except Exception as e:
        print(f"Error in Ticketmaster module: {e}")
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting the driver: {e}")

def ShopifyCheckout(driver: webdriver.Chrome, profile: dict):
    """
    Perform checkout on Shopify.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        profile (dict): Profile data containing checkout details.
    """
    actions = ActionChains(driver)
    try:
        checkoutButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Checkout']")))
        checkoutButton.click()
        print("Checkout initiated.")
    except Exception as e:
        print(f"Failed to initiate checkout: {e}")
        return

    try:
        actions.send_keys(profile["Email"]).perform()
        actions.send_keys(Keys.TAB * 3).perform()
        actions.send_keys(profile["FirstName"]).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(profile["LastName"]).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(profile["ShippingAddress"]).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(profile["ShippingSecondary"]).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(profile["ShippingCity"]).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(profile["ShippingState"]).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(profile["ShippingZipCode"]).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(profile["ShippingPhone"]).perform()
        actions.send_keys(Keys.TAB * 4).perform()
        print("Shipping details filled.")
    except Exception as e:
        print(f"Failed to fill shipping details: {e}")
        return

    try:
        actions.send_keys(profile["CardNumber"]).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(profile["ExpirationDate"]).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(profile["SecurityCode"]).perform()
        actions.send_keys(Keys.TAB * 7).perform()
        print("Payment details filled.")
    except Exception as e:
        print(f"Failed to fill payment details: {e}")
        return

    try:
        checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Checkbox1")))
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", checkbox)
        print("Checkbox clicked successfully.")
    except Exception as e:
        print(f"Failed while agreeing to the TOS: {e}")

    time.sleep(5)
    print("Ready to checkout!")

def ShopifyAddToCart(driver: webdriver.Chrome, profile: dict):
    """
    Add a product to the cart on a Shopify website and proceed to checkout.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        profile (dict): Profile data containing checkout details.
    """
    actions = ActionChains(driver)
    try:
        addToCartButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Add to Cart']")))
        addToCartButton.click()
        print("Add to cart initiated.")
        ShopifyCheckout(driver, profile)
    except Exception as e:
        print(f"Failed to initiate add to cart: {e}")
        return

def ShopifyProductFound(driver: webdriver.Chrome, profile: dict, productUrl: str):
    """
    Load a Shopify product page and attempt to add it to the cart.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        profile (dict): Profile data containing checkout details.
        productUrl (str): URL of the product page.
    """
    try:
        driver.get(productUrl)
        clear()
        print(f"Now loading {driver.title}...")
        time.sleep(2.5)
        ShopifyAddToCart(driver, profile)
    except Exception as e:
        print(f"Failed to load product page or add to cart: {e}")

def ShopifyModule(profile: str, selected: str, desiredProduct: str):
    """
    Main function to run the Shopify module.

    Args:
        profile (str): The profile name.
        selected (str): The selected Shopify store.
        desiredProduct (str): The product to search for.
    """
    proxies = ReadProxies()
    proxy = GetRandomProxy(proxies)
    clear()
    try:
        driver = ConfigureDriver(proxy)
        shopifySelectedUrl = f'https://{selected}.com/products.json'
        clear()
        print(f"Selected Proxy: {proxy}")
        while True:
            try:
                r = requests.get(shopifySelectedUrl)
                products = r.json().get('products', [])
                found = False
                for product in products:
                    productName = product['title'].lower()
                    if desiredProduct in productName:
                        print(f"Found product: {product['title']}")
                        productUrl = f'https://{selected}.com/products/{product["handle"]}'
                        time.sleep(2.5)
                        ShopifyProductFound(driver, profile, productUrl)
                        found = True
                        break
                if not found:
                    print(f"No product matching '{desiredProduct}' found. Waiting...")
                    time.sleep(3.333)
            except requests.RequestException as e:
                print(f"Error during product search: {e}")
            except Exception as e:
                print(f"An error occurred during product search: {e}")
    except Exception as e:
        print(f"Error in Shopify module: {e}")
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting the driver: {e}")

def LoadProfile(profile: str) -> Optional[dict]:
    """
    Load user profile data from a file.

    Args:
        profile (str): The profile name.

    Returns:
        Optional[dict]: A dictionary containing profile data or None if loading fails.
    """
    profileData = {}
    try:
        with open(f"files/profile_{profile}.txt", "r") as profileFile:
            for line in profileFile:
                if "Name:" in line:
                    pName = line.split("Name: ")[1].strip()
                    nameParts = pName.split(' ')
                    profileData["FirstName"] = nameParts[0] if len(nameParts) >= 1 else ""
                    profileData["LastName"] = nameParts[1] if len(nameParts) >= 2 else ""
                if "Email:" in line:
                    profileData["Email"] = line.split("Email: ")[1].strip()
                if "Shipping Address:" in line:
                    profileData["ShippingAddress"] = line.split("Shipping Address: ")[1].strip()
                if "Shipping Secondary:" in line:
                    profileData["ShippingSecondary"] = line.split("Shipping Secondary: ")[1].strip()
                if "Shipping City:" in line:
                    profileData["ShippingCity"] = line.split("Shipping City: ")[1].strip()
                if "Shipping Zip Code:" in line:
                    profileData["ShippingZipCode"] = line.split("Shipping Zip Code: ")[1].strip()
                if "Shipping State:" in line:
                    profileData["ShippingState"] = line.split("Shipping State: ")[1].strip()
                if "Shipping Phone:" in line:
                    profileData["ShippingPhone"] = line.split("Shipping Phone: ")[1].strip()
                if "Billing Address:" in line:
                    profileData["BillingAddress"] = line.split("Billing Address: ")[1].strip()
                if "Billing Secondary:" in line:
                    profileData["BillingSecondary"] = line.split("Billing Secondary: ")[1].strip()
                if "Billing City:" in line:
                    profileData["BillingCity"] = line.split("Billing City: ")[1].strip()
                if "Billing Zip Code:" in line:
                    profileData["BillingZipCode"] = line.split("Billing Zip Code: ")[1].strip()
                if "Billing State:" in line:
                    profileData["BillingState"] = line.split("Billing State: ")[1].strip()
                if "Billing Phone:" in line:
                    profileData["BillingPhone"] = line.split("Billing Phone: ")[1].strip()
                if "Card Number:" in line:
                    profileData["CardNumber"] = line.split("Card Number: ")[1].strip()
                if "Expiration Date:" in line:
                    profileData["ExpirationDate"] = line.split("Expiration Date: ")[1].strip()
                if "Security Code:" in line:
                    profileData["SecurityCode"] = line.split("Security Code: ")[1].strip()
        clear()
        print("Your profile has been loaded.")
        return profileData
    except FileNotFoundError:
        print(f"Profile file not found for {profile}. Ensure 'files/profile_{profile}.txt' exists.")
        return None
    except Exception as e:
        print(f"Failed to load profile: {e}")
        return None

def LoadSite(profile: str, module: str, selected: str, desiredProduct: str):
    """
    Loads the appropriate module based on user input.

    Args:
        profile (dict): Profile data containing checkout details.
        module (str): The module name.
        selected (str): The selected event or action.
        desiredProduct (Optional[str]): The desired product.
    """
    clear()
    if module.lower() == 'ticketmaster':
        clear()
        print("Ticketmaster Module Loading!")
        LoadTicketmasterAccounts(profile, selected)
    elif module.lower() == 'shopify':
        clear()
        print("Shopify Module Loading!")
        ShopifyModule(profile, selected, desiredProduct)
    else:
        print("Invalid module choice.")
        time.sleep(2.5)
        exit()

@app.command()
def profile(profile: str, module: str, selected: str, desiredproduct: str):
    """
    Loads the user profile and starts the appropriate module.

    Args:
        profile (str): The profile name.
        module (str): The module name.
        selected (str): The selected event or action.
        desiredProduct (Optional[str]): The desired product.
    """
    
    desiredProduct = desiredproduct.lower()
    profileData = LoadProfile(profile)
    if profileData:
        LoadSite(profileData, module, selected, desiredProduct)
    else:
        print("Error! Something is missing...")
        return
    
if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(f"Error in main execution: {e}")