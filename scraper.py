import os
import time
import subprocess
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_chrome_version():
    try:
        # Get the version string from the system
        output = subprocess.check_output(['google-chrome', '--version']).decode('utf-8')
        # Standard output is "Google Chrome 147.0.xxxx.xx"
        version = output.split()[2].split('.')[0]
        return int(version)
    except Exception as e:
        print(f"Could not detect local Chrome version: {e}")
        return None

def run_scraper():
    # 1. Detect Version FIRST
    chrome_main_version = get_chrome_version()
    print(f"Detected System Chrome Version: {chrome_main_version}")

    base_path = os.getcwd()
    download_path = os.path.join(base_path, "downloads")
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    prefs = {
        "download.default_directory": download_path,
        "download.directory_upgrade": True,
        "download.prompt_for_download": False,
    }
    options.add_experimental_option("prefs", prefs)

    # 2. FORCE the version in the constructor
    # Use version_main to stop it from downloading v148
    driver = uc.Chrome(options=options, version_main=chrome_main_version)
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
        # Look for the download button
        download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Download')]")))
        download_btn.click()
        print("Download clicked. Monitoring folder...")

        # --- Wait for completion ---
        timeout = 120 
        start_time = time.time()
        while time.time() - start_time < timeout:
            files = os.listdir(download_path)
            valid_files = [f for f in files if not f.endswith('.crdownload')]
            if valid_files:
                print(f"Success! File ready: {valid_files[0]}")
                break
            time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("error_debug.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()