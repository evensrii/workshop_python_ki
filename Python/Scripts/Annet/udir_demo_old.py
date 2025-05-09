import time
import re
import os
from pathlib import Path
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import io

def safe_click(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        try:
            element.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", element)
        return True
    except Exception as e:
        print(f"Click failed: {e}")
        return False

def download_udir_csv(download_dir, url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": str(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.set_window_size(1200, 800)
    time.sleep(2)
    
    ########### Aksepter cookies
    
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "submitAllCategoriesButton"))
        )
        safe_click(driver, cookie_button)
        time.sleep(2)
    except Exception:
        pass
    
    ########### Klikk Kontraktstype
    
    try:
        xpath = "//button[normalize-space(.)='Kontraktstype']"
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        safe_click(driver, element)
        time.sleep(1)
    except Exception:
        pass
    
    ########### Klikk Eksporter
    
    selectors = [
        "//button[.//span[contains(text(), 'Eksporter')]]",
        "//button[contains(@class, 'header-action')]//span[contains(text(), 'Eksporter')]/..",
        "//button[.//svg[@class='akselicon']/following-sibling::span[contains(text(), 'Eksporter')]]"
    ]
    export_button = None
    for selector in selectors:
        try:
            export_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, selector))
            )
            if export_button:
                break
        except Exception:
            continue
    if not export_button:
        driver.quit()
        raise Exception("Could not find export button")
    before_files = set(Path(download_dir).glob("*VGO.Laerekontrakter.csv"))
    safe_click(driver, export_button)
    # Wait for new file
    max_wait = 15
    start_time = time.time()
    new_file = None
    while time.time() - start_time < max_wait:
        current_files = set(Path(download_dir).glob("*VGO.Laerekontrakter.csv"))
        new_files = current_files - before_files
        if new_files:
            new_file = new_files.pop()
            break
        time.sleep(0.5)
    driver.quit()
    if not new_file:
        raise Exception("No new CSV file was downloaded")
    print(f"Downloaded file: {new_file}")
    return new_file

def clean_udir_csv(raw_csv_path, output_csv_path):
    # Manually open and decode
    with open(raw_csv_path, 'rb') as f:
        raw = f.read()
    # Decode manually (UTF-16 little endian without BOM)
    text = raw.decode('utf-16le')
    # Now load into pandas
    df = pd.read_csv(
        io.StringIO(text),
        sep='\t',
        skiprows=1,
        dtype=str
    )
    # Only keep relevant columns (skip first two columns)
    df = df.iloc[:, 2:]
    # Rename columns for clarity
    df.columns = [
        'Programområdekode',
        'Utdanningsprogram',
        'Programområde',
        '2022',
        '2023',
        '2024'
    ]
    # Clean numbers
    import re
    for year in ['2022', '2023', '2024']:
        df[year] = df[year].astype(str).apply(lambda x: re.sub(r'\s+', '', x))
        df[year] = pd.to_numeric(df[year], errors='coerce')
    df.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"Cleaned data saved to {output_csv_path}")
    return df

def main():
    url = "https://www.udir.no/tall-og-forskning/statistikk/statistikk-fag-og-yrkesopplaring/antall-larlinger/larekontrakter-utdanningsprogram/"
    data_dir = Path(__file__).parent.parent / "Data" / "Udir"
    output_csv = data_dir / "laerekontrakter.csv"
    download_dir = str(data_dir)
    raw_csv_path = download_udir_csv(download_dir, url)
    try:
        df = clean_udir_csv(raw_csv_path, output_csv)
        print("\nPreview of cleaned data:")
        print(df.head())
    finally:
        try:
            os.remove(raw_csv_path)
            print(f"Deleted original downloaded file: {raw_csv_path}")
        except Exception as e:
            print(f"Could not delete file {raw_csv_path}: {e}")

if __name__ == "__main__":
    main()