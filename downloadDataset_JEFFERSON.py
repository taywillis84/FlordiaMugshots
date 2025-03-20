import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
from datetime import datetime

# Start timer
start_time = time.time()
date_str = datetime.now().strftime("%Y-%m-%d")
# Base URLs
base_url = 'https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000?Page='
photo_base_url = 'https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000/Inmate/Photo/'

# Folder to save the images
save_folder = f'trainingData/JEFFERSON'
os.makedirs(save_folder, exist_ok=True)

# Log file to track downloaded images
log_file = os.path.join(save_folder, 'downloaded_images.txt')

# Load previously downloaded images from log file
if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        downloaded_images = set(f.read().splitlines())
else:
    downloaded_images = set()

# Initialize a counter for new downloads
new_files_downloaded = 0

# Loop through each page from 1 to 29
for page_num in range(1, 30):
    url = f"{base_url}{page_num}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    for img_tag in img_tags:
        img_src = img_tag.get('src')
        if img_src and 'Inmate/Photo/' in img_src:
            try:
                img_number = img_src.split('/')[-1].split('?')[0]

                # Skip if the image was already downloaded
                if img_number in downloaded_images:
                    print(f"Skipping {img_number}. Already downloaded.")
                    continue

                # Construct the correct download URL
                img_url = f"{photo_base_url}{img_number}?type=Full"

                # Download image
                img_data = requests.get(img_url).content
                img = Image.open(BytesIO(img_data))

                # Save the image as PNG with "JEFFERSON_" prefix
                img_name = os.path.join(save_folder, f"JEFFERSON_{img_number}.png")
                img.save(img_name, 'PNG')

                print(f"Downloaded {img_name}")
                new_files_downloaded += 1
                downloaded_images.add(img_number)  # Add to set

            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

# Update log file with newly downloaded images
if new_files_downloaded > 0:
    with open(log_file, 'a') as f:
        for img_number in downloaded_images:
            f.write(img_number + '\n')

# Stop timer and calculate total execution time
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

# Report the total number of new files downloaded and execution time
print(f"New files downloaded: {new_files_downloaded}")
print(f"Total execution time: {minutes} minutes and {seconds} seconds.")
