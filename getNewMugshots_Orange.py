import time
import base64
import os
import fitz  # PyMuPDF for PDF parsing
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

start_time = time.time()

# Step 1: Extract Names from PDF
def parse_pdf(file_path):
    """ Extract text from PDF. """
    pdf_document = fitz.open(file_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")
    return text

def extract_names(file_path):
    """ Extract names in 'LAST, FIRST MIDDLE' format and remove city names. """
    text = parse_pdf(file_path)
    text = re.sub(r'\b[A-Za-z]+, FL\b', '', text)  # Remove city names
    name_pattern = r'\b([A-Z]+, [A-Z]+(?: [A-Z]+)?)\b'  # Match names in format LAST, FIRST MIDDLE (optional)
    names = re.findall(name_pattern, text)
    return names if names else []

# Step 2: Set up Selenium WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
print("Browser launched!")

# Create a folder to store images
folder_path = "OrangeCounty"
os.makedirs(folder_path, exist_ok=True)
print(f"Folder '{folder_path}' ready.")

# Extracted names from the PDF
file_path = "new-bookings.pdf"
names = extract_names(file_path)

# Step 3: Process Each Name
for name in names:
    try:
        # Open the inmate search page
        url = "https://netapps.ocfl.net/BestJail/Home/Inmates#"  # Replace with the actual URL
        driver.get(url)
        time.sleep(3)  # Allow page to load

        # Find the text box and type the extracted name
        input_box = driver.find_element(By.ID, "inmate")
        input_box.clear()
        input_box.send_keys(name)
        print(f"Typed name '{name}' into the search box.")

        # Click the search button
        search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        search_button.click()
        print(f"Clicked the search button for '{name}'.")
        time.sleep(3)  # Wait for results

        # Find all the hyperlinks
        links = driver.find_elements(By.TAG_NAME, "a")

        for link in links:
            if "Water, Garbage & Recycling" in link.text:
                print("Stopping loop as invalid link detected.")
                break

            if "," in link.text:  # Name format contains a comma
                link.click()
                print(f'Clicked on inmate link: "{link.text}"')
                time.sleep(3)

                # Find and save the first Base64-encoded image
                images = driver.find_elements(By.TAG_NAME, "img")
                for index, img in enumerate(images):
                    img_url = img.get_attribute("src")

                    if img_url and img_url.startswith("data:image/png;base64,"):
                        base64_data = img_url.split(",")[1]
                        image_data = base64.b64decode(base64_data)
                        file_name = f"{folder_path}/{name.replace(',', '').replace(' ', '_')}.png"

                        with open(file_name, "wb") as file:
                            file.write(image_data)

                        print(f"Saved image: {file_name}")
                        break  # Stop after first image

                # Close the modal if necessary
                try:
                    close_button = driver.find_element(By.CSS_SELECTOR, "button.close")
                    close_button.click()
                    print("Closed inmate details modal.")
                    time.sleep(2)
                except:
                    print("No modal found to close.")

                driver.back()  # Return to search results
                time.sleep(3)
                break  # Move to the next name after processing first result

    except Exception as e:
        print(f"Error processing '{name}': {e}")

# Close the browser
driver.quit()
print("Process complete!")
elapsed_time = (time.time() - start_time) / 60
print(f"Script completed in {elapsed_time:.2f} minutes.")
