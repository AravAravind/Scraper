import os
import time

# ... (rest of your setup code) ...

def run_with_manual_tokens():
    # 1. Absolute path ensures GitHub finds it
    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(current_dir, "downloads")
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    
    # 2. Tell Chrome EXACTLY where to put the file
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "directory_upgrade": True
    }
    options.add_experimental_option("prefs", prefs)
    
    # ... (Login and navigation code) ...

    # 3. The Download Click
    try:
        download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[descendant::span[contains(text(), 'Download')]]")))
        download_btn.click()
        
        # 4. WAIT for the file to appear
        print("Waiting for download to complete...")
        timeout = 60  # seconds
        start_time = time.time()
        while time.time() - start_time < timeout:
            files = os.listdir(download_path)
            # Check if there is a file and it's not a .crdownload (temporary file)
            if files and not any(f.endswith('.crdownload') for f in files):
                print(f"File found: {files[0]}")
                break
            time.sleep(2)
    except Exception as e:
        print(f"Download failed: {e}")