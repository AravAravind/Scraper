import os
import time
import json
import subprocess
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def get_chrome_version():
    try:
        # Check the version of chrome installed on the GitHub Runner
        version = subprocess.check_output(['google-chrome', '--version']).decode('utf-8')
        # Extract just the main number (e.g., 147)
        return int(version.split()[2].split('.')[0])
    except:
        return None

def run_with_manual_tokens():
    chrome_version = get_chrome_version()
    print(f"Detected Chrome version: {chrome_version}")

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Force undetected_chromedriver to use the matching version
    driver = uc.Chrome(options=options, version_main=chrome_version)

    try:
        driver.get("https://www.kaggle.com")
        time.sleep(2)

        # ... rest of your cookie injection and download logic ...
        manual_cookies = [
            {"name": "ka_sessionid", "value": os.getenv("KAGGLE_SESSION_ID"), "domain": ".kaggle.com"},
            {"name": "XSRF-TOKEN", "value": os.getenv("KAGGLE_XSRF_TOKEN"), "domain": ".kaggle.com"}
        ]

        for cookie in manual_cookies:
            driver.add_cookie(cookie)

        driver.get("https://www.kaggle.com/datasets?topic=trendingDataset")
        time.sleep(5)
        
        # Verify
        if "Log In" not in driver.page_source:
            print("Successfully logged in!")
        else:
            print("Login failed - check your token values.")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_with_manual_tokens()