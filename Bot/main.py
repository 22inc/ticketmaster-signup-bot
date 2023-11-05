import os

def profileSelect():
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
    
    loadSite(pName, pEmail, pShippingAddress, pShippingSecondary, pShippingCity, pShippingZipCode, pShippingState, pShippingPhone, pBillingAddress, pBillingSecondary, pBillingCity, pBillingZipCode, pBillingState, pBillingPhone)

def loadSite(pName, pEmail, pShippingAddress, pShippingSecondary, pShippingCity, pShippingZipCode, pShippingState, pShippingPhone, pBillingAddress, pBillingSecondary, pBillingCity, pBillingZipCode, pBillingState, pBillingPhone):
    os.system("cls")
    selectedModule = input("What module would you like to load? ")

    if selectedModule == "Ticketmaster" | "ticketmaster":
        print("Ticketmaster module loading.")
        return
    elif selectedModule == "Shopify" | "shopify":
        print("Shopify module loading.")
        return
    else:
        loadSite()
        
# Call profileSelect to load the profile and retrieve the variables.
(pName, pEmail, pShippingAddress, pShippingSecondary, pShippingCity, pShippingZipCode, pShippingState, pShippingPhone, pBillingAddress, pBillingSecondary, pBillingCity, pBillingZipCode, pBillingState, pBillingPhone) = profileSelect()
