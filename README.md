# Expedia_Raw_Data
Playwright and  CDP based scraper that captures raw GraphQL responses from Expedia hotel search, bypassing bot detection using real Chrome session.

# Expedia Hotels Scraper

Scrapes raw hotel search results from Expedia using Playwright and Chrome DevTools Protocol (CDP). Built to capture the actual GraphQL API responses the browser receives, not parsed or cleaned data.


# What This Does

When you search hotels on Expedia, the browser quietly fires GraphQL requests to Expedia's internal API. This script intercepts those raw JSON responses before they even render on screen. The output is the exact response from Expedia's server, untouched.

# Search parameters used:
Destination: California, United States of America
Dates: July 26, 2026 to July 30, 2026
Travelers: 1 traveler, 1 room
Results: 200 properties

# Proxies Used:

- Turbo VPN : Used to not get blocked by the site.
  

# Tech Stack Used

ToolPurposePython 3.13Core scripting languagePlaywrightBrowser automation and network interceptionChrome DevTools Protocol (CDP)Connect to a real Chrome session to bypass bot detectionGraphQLExpedia's internal API format that returns hotel dataJSONOutput format for raw responsesVPN / Residential ProxyBypass IP-level bot blocking


# Why Playwright over Selenium or BeautifulSoup

- BeautifulSoup only reads static HTML. Expedia loads hotels via JavaScript after the page opens, so BS4 sees an empty page.
- Selenium can run JavaScript but cannot intercept network responses natively. It also gets flagged by bot detection systems more easily.
- Playwright does both. It controls the browser and listens to every network response via page.on("response"). This is the only way to capture raw API data the      way the browser receives it.

# Why CDP (Chrome DevTools Protocol)
 - Playwright's built-in Chromium browser gets detected by Expedia's bot protection (Akamai / DataDome). Even with stealth scripts, the IP and browser fingerprint    get flagged.

   CDP solves this by connecting Playwright to your actual installed Chrome browser instead of launching a new one. Expedia sees a genuine Chrome session with a      real user profile, cookies, and browser fingerprint, so it does not trigger bot checks.

   pythonbrowser = playwright.chromium.connect_over_cdp("http://localhost:9222")


    Anti-Bot Challenges Faced

    Expedia uses multiple layers of bot protection:


   IP blacklisting based on known datacenter and VPN ranges
   Browser fingerprinting to detect automation tools
   Slider CAPTCHA for suspicious sessions
   DataDome behavioral analysis that tracks scroll speed, mouse movement, and request timing


# How each was handled:

ChallengeSolution UsedIP blacklistingVPN with US residential IPBrowser fingerprintingCDP connection to real ChromeCAPTCHASolved manually once, session reusedBehavioral analysisHuman-like scroll timing with time.sleep()


# How It Works


Chrome is launched with remote debugging enabled on port 9222
Playwright connects to that Chrome session via CDP
A response listener is attached before navigating to Expedia
The script opens the hotel search URL
It scrolls the page repeatedly to trigger lazy loading of more hotels
Every GraphQL response containing hotel data is captured automatically
All raw responses are saved to expedia_raw_output.json



# Setup

Install dependencies:

bashpip install playwright
playwright install chromium

Launch Chrome with remote debugging:

bash"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebug"

Run the scraper:

bashpython expedia_raw.py


# Output

Raw GraphQL responses are saved to expedia_raw_output.json. Each entry contains:

json{
  "url": "https://www.expedia.com/graphql",
  "status": 200,
  "body": {
    "data": {
      "propertySearch": {
        ...raw hotel data from Expedia's server...
      }
    }
  }
}

This is the unmodified server response, not parsed or filtered in any way.


Files

expedia_raw.py           Main scraper script
expedia_raw_output.json  Raw output from Expedia's GraphQL API
extract_hotels.py        Optional parser to extract hotel names and prices
README.md                This file
