import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def run_with_manual_tokens():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    driver = uc.Chrome(options=options)

    # 1. You MUST visit the site once to set the domain context
    driver.get("https://www.kaggle.com")
    time.sleep(2)

    # 2. Define the cookies you have
    # ka_sessionid is the main one that keeps you logged in
    # XSRF-TOKEN is used for security validation on clicks/downloads
    manual_cookies = [
        {"name": "ka_sessionid", "value": os.getenv("KAGGLE_SESSION_ID")},
        {"name": "XSRF-TOKEN", "value": os.getenv("KAGGLE_XSRF_TOKEN")}
    ]

    # 3. Inject them
    for cookie in manual_cookies:
        cookie['domain'] = '.kaggle.com' # Essential for the cookies to work
        driver.add_cookie(cookie)

    # 4. Navigate to Trending
    driver.get("https://www.kaggle.com/datasets?topic=trendingDataset")
    time.sleep(5)

    # Verification: If 'Log In' is not visible, we are in!
    if "Log In" not in driver.page_source:
        print("Success! Logged in with manual tokens.")
        # ... proceed with finding the first dataset and clicking download ...
    else:
        print("Login failed. Tokens might be expired or blocked by Cloudflare.")

    driver.quit()

if __name__ == "__main__":
    run_with_manual_tokens()