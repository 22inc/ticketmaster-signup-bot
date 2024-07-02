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
import keyboard
from universalclear import clear
import typer
from typing import List, Tuple, Optional

app = typer.Typer()

ticketmasterAccountList: List[Tuple[str, str]] = []

def readProxies() -> List[str]:
    """
    Reads proxy addresses from a file and returns them as a list.

    Returns:
        List[str]: A list of proxy addresses.
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

def getRandomProxy(proxies: List[str]) -> Optional[str]:
    """
    Selects a random proxy from the list of proxies.

    Args:
        proxies (List[str]): A list of proxy addresses.

    Returns:
        Optional[str]: A random proxy address or None if the list is empty.
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

def configureDriver(proxy: Optional[str] = None) -> webdriver.Chrome:
    """
    Configures and returns a Chrome WebDriver instance.

    Args:
        proxy (Optional[str], optional): Proxy address to be used. Defaults to None.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
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

def isTextPresent(driver: webdriver.Chrome, text: str) -> bool:
    """
    Checks if the specified text is present on the web page.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        text (str): The text to search for.

    Returns:
        bool: True if the text is present, False otherwise.
    """
    try:
        elementPresent = EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
        WebDriverWait(driver, 10).until(elementPresent)
        return True
    except Exception as e:
        print(f"Error while checking if text is present: {e}")
        return False

def holdKeyforDuration(key: str, duration: float):
    """
    Holds down a keyboard key for a specified duration.

    Args:
        key (str): The key to be held down.
        duration (float): The duration in seconds to hold the key down.
    """
    try:
        keyboard.press(key)
        time.sleep(duration)
        keyboard.release(key)
    except Exception as e:
        print(f"Error while holding key for duration: {e}")

def loadTicketmasterAccounts(profile: str, module: str, selected: str):
    """
    Loads Ticketmaster accounts from a file and starts the Ticketmaster module.

    Args:
        profile (str): The profile name.
        module (str): The module name.
        selected (str): The selected event or action.
    """
    global ticketmasterAccountList
    try:
        ticketmasterAccountList = []
        with open("files/ticketmaster_accounts.txt", "r") as file:
            for line in file:
                email, password = line.strip().split(":")
                ticketmasterAccountList.append((email, password))
        print("Accounts loaded:", ticketmasterAccountList)
        time.sleep(1)
        clear()
        print("Ticketmaster module loading...")
        ticketmasterModule(profile, module, selected)
    except FileNotFoundError:
        print("Ticketmaster accounts file not found. Ensure 'files/ticketmaster_accounts.txt' exists.")
    except Exception as e:
        print(f"An error occurred while loading Ticketmaster accounts: {e}")

def markAccountAsUsed(email: str, password: str):
    """
    Marks a Ticketmaster account as used by commenting it out in the file.

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

def getUnusedAccount() -> Tuple[Optional[str], Optional[str]]:
    """
    Retrieves an unused Ticketmaster account.

    Returns:
        Tuple[Optional[str], Optional[str]]: The email and password of an unused account or (None, None) if no unused accounts are available.
    """
    try:
        for email, password in ticketmasterAccountList:
            return email, password
        return None, None
    except Exception as e:
        print(f"An error occurred while getting an unused account: {e}")
        return None, None

def ticketmasterLogin(driver: webdriver.Chrome, email: str, password: str):
    """
    Logs into Ticketmaster using the provided email and password.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        email (str): The email of the Ticketmaster account.
        password (str): The password of the Ticketmaster account.
    """
    try:
        emailInput = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'email')))
        emailInput.send_keys(email)
        print("Email entered successfully.")
    except Exception as e:
        print(f"Failed to enter email: {e}")
        return

    try:
        passwordInput = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'password')))
        passwordInput.send_keys(password)
        print("Password entered successfully.")
    except Exception as e:
        print(f"Failed to enter password: {e}")
        return

    try:
        signInButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']")))
        signInButton.click()
        print("Sign in button clicked.")
        time.sleep(5)
    except Exception as e:
        print(f"Failed to click sign in button: {e}")

    try:
        while isTextPresent(driver, "Let's Get Your Identity Verified"):
            time.sleep(5)
            action = ActionChains(driver)
            action.key_down(Keys.ENTER).pause(15).key_up(Keys.ENTER).perform()
            time.sleep(5)
            print("Second anti-bot done successfully.")
            return
    except Exception as e:
        print(f"Error during second anti-bot process: {e}")
    print("Login process completed successfully.")
    input("Press Enter to continue...")

def ticketmasterAntiBot(driver: webdriver.Chrome):
    """
    Handles Ticketmaster anti-bot verification and performs login if successful.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
    """
    email, password = getUnusedAccount()
    if email:
        try:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'company-logo')))
            button.click()
            print("Sign in started.")
        except Exception as e:
            print(f"Failed to click the button: {e}")

        antibot_attempts = 0
        max_attempts = 3

        while antibot_attempts < max_attempts:
            if isTextPresent(driver, "Please verify you are a human"):
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
                    if isTextPresent(driver, "Please verify you are a human"):
                        antibot_attempts += 1
                        if antibot_attempts >= max_attempts:
                            print(f"Exceeded {max_attempts} attempts. Quitting.")
                            return
                        print("Re-doing anti-bot!")
                    else:
                        print("Passed anti-bot!")
                        time.sleep(2.5)
                        ticketmasterLogin(driver, email, password)
                        return
                except Exception as e:
                    print(f"Failed to do anti-bot attempt {antibot_attempts + 1}: {e}")
        if antibot_attempts == 0:
            print("No antibot verification required or successful.")
            ticketmasterLogin(driver, email, password)
    else:
        print("No unused accounts available.")

def ticketmasterModule(profile: str, module: str, selected: str):
    """
    Main function to run the Ticketmaster module.

    Args:
        profile (str): The profile name.
        module (str): The module name.
        selected (str): The selected event or action.
    """
    proxies = readProxies()
    proxy = getRandomProxy(proxies)
    print(f"Selected Proxy: {proxy}")
    clear()
    try:
        driver = configureDriver(proxy)
        driver.get(f'https://registration.ticketmaster.com/{selected}')
        print(f"Now loading {driver.title}...")
        ticketmasterAntiBot(driver)
    except Exception as e:
        print(f"Error in Ticketmaster module: {e}")
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting the driver: {e}")

def shopifyCheckout(driver: webdriver.Chrome, profile: dict):
    """
    Performs the checkout process on a Shopify website.

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
    except Exception as e:
        print(f"Failed to fill payment details: {e}")
        return

    try:
        checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='Checkbox1']")))
        checkbox.click()
    except Exception as e:
        print(f"Failed while agreeing to the TOS: {e}")
    time.sleep(5)
    print("Ready to checkout!")

def shopifyAddToCart(driver: webdriver.Chrome, profile: dict):
    """
    Adds a product to the cart on a Shopify website and proceeds to checkout.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        profile (dict): Profile data containing checkout details.
    """
    try:
        addToCartButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Add to Cart']")))
        addToCartButton.click()
        print("Add to cart initiated.")
        shopifyCheckout(driver, profile)
    except Exception as e:
        print(f"Failed to add to cart: {e}")

def shopifyProductFound(driver: webdriver.Chrome, profile: dict, productUrl: str):
    """
    Loads a Shopify product page and attempts to add it to the cart.

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
        shopifyAddToCart(driver, profile)
    except Exception as e:
        print(f"Failed to load product page or add to cart: {e}")

def shopifyModule(profile: str, module: str, selected: str):
    """
    Main function to run the Shopify module.

    Args:
        profile (str): The profile name.
        module (str): The module name.
        selected (str): The selected Shopify store.
    """
    proxies = readProxies()
    proxy = getRandomProxy(proxies)
    clear()
    try:
        driver = configureDriver(proxy)
        shopifySelectedUrl = f'https://{selected}.com/products.json'
        desiredProduct = input("What product do you want? ").lower()
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
                        productUrl = f'https://www.{selected}.com/products/{product["handle"]}'
                        time.sleep(2.5)
                        shopifyProductFound(driver, profile, productUrl)
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

@app.command()
def profile(profile: str, module: str, selected: str):
    """
    Loads the user profile and starts the appropriate module.

    Args:
        profile (str): The profile name.
        module (str): The module name.
        selected (str): The selected event or action.
    """
    profileData = loadProfile(profile)
    if profileData:
        loadSite(profileData, module, selected)

def loadProfile(profile: str) -> Optional[dict]:
    """
    Loads user profile data from a file.

    Args:
        profile (str): The profile name.

    Returns:
        Optional[dict]: A dictionary containing profile data or None if loading fails.
    """
    profileData = {}
    try:
        with open(f"files/profile_{profile}.txt", "r") as profile_file:
            for line in profile_file:
                if "Name:" in line:
                    pName = line.split("Name: ")[1].strip()
                    name_parts = pName.split(' ')
                    profileData["FirstName"] = name_parts[0] if len(name_parts) >= 1 else ""
                    profileData["LastName"] = name_parts[1] if len(name_parts) >= 2 else ""
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

def loadSite(profile: dict, module: str, selected: str):
    """
    Loads the appropriate module based on user input.

    Args:
        profile (dict): Profile data containing checkout details.
        module (str): The module name.
        selected (str): The selected event or action.
    """
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
    try:
        app()
        ticketmasterModule("profile", "ticketmaster", "selected")
    except Exception as e:
        print(f"Error in main execution: {e}")