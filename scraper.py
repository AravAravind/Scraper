import os
import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_scraper():
    # 1. Setup Absolute Download Path
    # This ensures Python and GitHub Actions look at the same spot
    base_path = os.getcwd()
    download_path = os.path.join(base_path, "downloads")
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    print(f"Local download path: {download_path}")

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    
    # 2. Force Chrome to use this directory
    prefs = {
        "download.default_directory": download_path,
        "download.directory_upgrade": True,
        "download.prompt_for_download": False,
    }
    options.add_experimental_option("prefs", prefs)

    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    try:
        # --- Authentication ---
        driver.get("https://www.kaggle.com")
        time.sleep(2)
        
        cookies = [
            {"name": "ka_sessionid", "value": os.getenv("KAGGLE_SESSION_ID"), "domain": ".kaggle.com"},
            {"name": "XSRF-TOKEN", "value": os.getenv("KAGGLE_XSRF_TOKEN"), "domain": ".kaggle.com"}
        ]
        for c in cookies:
            driver.add_cookie(c)

        # --- Navigation ---
        driver.get("https://www.kaggle.com/datasets?topic=trendingDataset")
        
        # Click the first dataset link
        first_ds = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-test-id='dataset-list-item'] a")))
        driver.get(first_ds.get_attribute("href"))
        
        # --- The Download ---
        # We try two different selector types to be safe
        try:
            download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Download')]")))
        except:
            download_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[role='button'] i.material-icons:contains('cloud_download')")))
        
        download_btn.click()
        print("Download clicked. Monitoring folder...")

        # --- The Wait Loop (CRITICAL) ---
        timeout = 120 # 2 minutes max
        start_time = time.time()
        downloaded = False
        
        while time.time() - start_time < timeout:
            files = os.listdir(download_path)
            # Filter out hidden files or temporary .crdownload files
            valid_files = [f for f in files if not f.endswith('.crdownload') and not f.startswith('.')]
            
            if valid_files:
                print(f"Success! Found file: {valid_files[0]}")
                downloaded = True
                break
            
            time.sleep(5)
            print("Still waiting for file to appear...")

        if not downloaded:
            print("Timeout reached: No file downloaded.")

    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("error_debug.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()