import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

# Base URL for listing pages
base_url = 'https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000?Page='

# Base URL for downloading inmate photos
photo_base_url = 'https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000/Inmate/Photo/'

# Folder to save the images
save_folder = 'trainingData/JeffersonCounty'

# Create folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)

# Initialize a counter for downloaded files
total_files_downloaded = 0

# Loop through each page from 1 to 29
for page_num in range(1, 30):
    # Construct the URL for the current page
    url = f"{base_url}{page_num}"

    # Fetch the content of the current page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags in the HTML
    img_tags = soup.find_all('img')

    # Extract the image numbers from URLs
    for img_tag in img_tags:
        img_src = img_tag.get('src')
        if img_src and 'Inmate/Photo/' in img_src:
            try:
                # Extract image number
                img_number = img_src.split('/')[-1].split('?')[0]

                # Construct the correct download URL
                img_url = f"{photo_base_url}{img_number}?type=Full"

                # Download image
                img_data = requests.get(img_url).content
                img = Image.open(BytesIO(img_data))

                # Save the image as PNG
                img_name = os.path.join(save_folder, f"{img_number}.png")
                img.save(img_name, 'PNG')

                print(f"Downloaded {img_name}")
                total_files_downloaded += 1

            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

# Report the total number of files downloaded
print(f"Total files downloaded: {total_files_downloaded}")
