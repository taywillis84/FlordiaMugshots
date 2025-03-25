import requests
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime, timedelta

# Get yesterday's date
yesterday = datetime.now() - timedelta(days=1)

# Format the date as MM%2FDD%2FYYYY
formatted_date = yesterday.strftime("%m%%2F%d%%2F%Y")

# URL of the inmate inquiry page
url = f"https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000?Name=&SubjectNumber=&BookingNumber=&BookingFromDate={formatted_date}&BookingToDate=&Facility="

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send a request to fetch the page content
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all image tags
    image_tags = soup.find_all("img")

    # Extract and modify image URLs
    image_urls = [img["src"] for img in image_tags if "src" in img.attrs]

    # Convert relative URLs to absolute if needed and modify links
    absolute_urls = []
    for img_url in image_urls:
        full_url = img_url if img_url.startswith("http") else "https://sheriff.jccal.org" + img_url
        full_url = full_url.replace("=Search", "=Full")
        absolute_urls.append(full_url)

    # Create a folder to store images
    save_directory = "newImages"
    os.makedirs(save_directory, exist_ok=True)


    # Function to sanitize filenames
    def sanitize_filename(filename):
        return "JEFFERSON_" + re.sub(r'[^a-zA-Z0-9_.-]', '_', filename) + ".jpg"


    # Download images
    for img_url in absolute_urls:
        img_data = requests.get(img_url, headers=headers).content
        filename = sanitize_filename(img_url.split("/")[-1])
        filepath = os.path.join(save_directory, filename)
        with open(filepath, "wb") as img_file:
            img_file.write(img_data)
        print(f"Downloaded: {filepath}")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
