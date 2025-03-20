import os
import time
import base64
import requests
import fitz  # PyMuPDF for PDF parsing
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Constants
date_str = datetime.now().strftime("%Y-%m-%d")
PDF_URL = "https://netapps.ocfl.net/BestJail/PDF/bookings.pdf"
LOCAL_PDF_PATH = "new-bookings.pdf"
FOLDER_PATH = f"trainingData/Orange/{date_str}"

# Function to check timestamps
def get_online_pdf_timestamp(url):
    response = requests.head(url)
    if 'Last-Modified' in response.headers:
        last_modified = response.headers['Last-Modified']
        return datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S GMT")
    return None

def get_local_pdf_timestamp(file_path):
    if os.path.exists(file_path):
        return datetime.utcfromtimestamp(os.path.getmtime(file_path))
    return None

# Function to download PDF
def download_pdf(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print("Downloaded new version of the PDF.")
    else:
        print("Failed to download the PDF.")

# Check and download new PDF if available
def check_and_download(url, save_path):
    online_timestamp = get_online_pdf_timestamp(url)
    local_timestamp = get_local_pdf_timestamp(save_path)

    if online_timestamp and (local_timestamp is None or online_timestamp > local_timestamp):
        print("Newer PDF available. Downloading...")
        download_pdf(url, save_path)
        return True  # New PDF downloaded
    else:
        print("Local PDF is up-to-date. Exiting script.")
        return False  # No new PDF

# Function to extract names from PDF
def extract_names(file_path):
    pdf_document = fitz.open(file_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")

    text = re.sub(r'\b[A-Za-z]+, FL\b', '', text)  # Remove city names
    name_pattern = r'\b([A-Z]+, [A-Z]+(?: [A-Z]+)?)\b'  # Match names like LAST, FIRST MIDDLE
    return re.findall(name_pattern, text) or []

# Exit if no new PDF
if not check_and_download(PDF_URL, LOCAL_PDF_PATH):
    exit()

# Extract names from new PDF
names = extract_names(LOCAL_PDF_PATH)
if not names:
    print("No names found in the PDF. Exiting script.")
    exit()

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
print("Browser launched!")

# Ensure image folder exists
os.makedirs(FOLDER_PATH, exist_ok=True)

# Process each name
for name in names:
    try:
        driver.get("https://netapps.ocfl.net/BestJail/Home/Inmates#")
        time.sleep(3)

        input_box = driver.find_element(By.ID, "inmate")
        input_box.clear()
        input_box.send_keys(name)
        print(f"Searching for '{name}'.")

        search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        search_button.click()
        time.sleep(3)

        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            if "Water, Garbage & Recycling" in link.text:
                break

            if "," in link.text:  # Name format contains a comma
                link.click()
                print(f"Clicked: {link.text}")
                time.sleep(3)

                images = driver.find_elements(By.TAG_NAME, "img")
                for index, img in enumerate(images):
                    img_url = img.get_attribute("src")
                    if img_url and img_url.startswith("data:image/png;base64,"):
                        base64_data = img_url.split(",")[1]
                        image_data = base64.b64decode(base64_data)
                        file_name = f"{FOLDER_PATH}/ORANGE_{name.replace(',', '').replace(' ', '_')}.png"

                        with open(file_name, "wb") as file:
                            file.write(image_data)

                        print(f"Saved image: {file_name}")
                        break  # Stop after first image

                try:
                    close_button = driver.find_element(By.CSS_SELECTOR, "button.close")
                    close_button.click()
                    print("Closed modal.")
                    time.sleep(2)
                except:
                    print("No modal to close.")

                driver.back()
                time.sleep(3)
                break

    except Exception as e:
        print(f"Error processing '{name}': {e}")

driver.quit()
print("Process complete!")
