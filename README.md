# Python Automation Script

This Python script is designed for automating interactions with web services like Ticketmaster and Shopify using Selenium and requests modules.

# Features

Ticketmaster Module: Automates account login and interaction with Ticketmaster registration pages.

Shopify Module: Searches for specific products on Shopify stores via their JSON API.

# Dependencies

Python 3.x AND requirements.txt

# Installation

Clone the repository:

```bash
git clone https://github.com/mhassannco/ticketmaster-signup-bot.git
cd ticketmaster-signup-bot
```

Install dependencies:

```python
pip install -r requirements.txt
```

Ensure Chrome browser is installed and if not you can use Chromedriver to automatically install it.

# Usage

Profiles: Create profiles (profile_profile_name.txt) with necessary details like name, email, shipping, and billing addresses.

Proxies: Prepare a proxies.txt file with proxy addresses if needed.

# Run the Script:

```bash
typer (filename).py run (your_profile_name) (wanted_module) (destination)
```

Profile Name: Name of the profile file without extension (e.g., example for profile_example.txt).

Module: Specify either Ticketmaster or Shopify.

Destination: Specific site or event identifier (e.g., website for shopify or event/performer name for ticketmaster).

Follow the prompts to execute the desired automation tasks.

# Notes

This script assumes you have valid accounts for Ticketmaster (ticketmaster_accounts.txt).
Ensure your profiles and account details are correctly formatted as per the script's requirements.

# Known Errors

Currently does not click the checkbox or checkout for the newly implemented shopify module.

# Developed with love by Malik Hassan!
