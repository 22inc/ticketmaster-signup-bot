## Spook Automation

import os
import sys
import time

def profileSelect():
    os.system("cls")
    profile = input("Which profile would you like to use? ")

    with open("profile_" + profile + ".txt", "r") as profile_file:
        for line in profile_file:
            print(line)

            ## Define basic variables from selected profile.

            if "Name:" in line:
                pName = line.split("Name:")[1].strip()
                break
            if "Email:" in line:
                pEmail = line.split("Email:")[1].strip()
                break

            ## Define shipping variables from selected profile.

            if "Shipping Address:" in line:
                pShippingAddress = line.split("Shipping Address:")[1].strip()
                break
            if "Shipping Secondary:" in line:
                pShippingSecondary = line.split("Shipping Secondary:")[1].strip()
                break
            if "Shipping City:" in line:
                pShippingCity = line.split("Shipping City:")[1].strip()
                break
            if "Shipping Zip Code:" in line:
                pShippingZipCode = line.split("Shipping Zip Code:")[1].strip()
                break
            if "Shipping State:" in line:
                pShippingState = line.split("Shipping State:")[1].strip()
                break
            if "Shipping Phone:" in line:
                pShippingPhone = line.split("Shipping Phone:")[1].strip()
                break

            ## Define billing variables from selected profile.

            if "Billing Address:" in line:
                pBillingAddress = line.split("Billing Address:")[1].strip()
                break
            if "Billing Secondary:" in line:
                pBillingSecondary = line.split("Billing Secondary:")[1].strip()
                break
            if "Billing City:" in line:
                pBillingCity = line.split("Billing City:")[1].strip()
                break
            if "Billing Zip Code:" in line:
                pBillingZipCode = line.split("Billing Zip Code:")[1].strip()
                break
            if "Billing State:" in line:
                pBillingState = line.split("Billing State:")[1].strip()
                break
            if "Billing Phone:" in line:
                pBillingPhone = line.split("Billing Phone:")[1].strip()    
    if profile == profile:
        os.system("cls")
        print("Your profile has been loaded.")
def loadSite(pName, pEmail, pShippingAddress, pShippingSecondary, pShippingCity, pShippingZipCode, pShippingState, pShippingPhone, pBillingAddress, pBillingSecondary, pBillingCity, pBillingZipCode, pBillingState, pBillingPhone):
    os.system("cls")
    selectedModule = input("What module would you like to load? ")
profileSelect()