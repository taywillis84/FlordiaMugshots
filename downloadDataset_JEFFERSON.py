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
base_url = 'https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000?Name=&SubjectNumber=&BookingNumber=&BookingFromDate=03%2F22%2F2025&BookingToDate=&Facility='
photo_base_url = 'https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000/Inmate/Photo/'

# Folder to save the images
save_folder = f'trainingData/newJEFFERSON'
os.makedirs(save_folder, exist_ok=True)

# Manifest file to track downloaded images with details
manifest_file = os.path.join(save_folder, 'manifest.json')

# Load previously downloaded images from the manifest file
if os.path.exists(manifest_file):
    with open(manifest_file, 'r') as f:
        downloaded_images = {entry['img_number'] for entry in json.load(f)}
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

# Update manifest file with newly downloaded images
if new_files_downloaded > 0:
    import json
    manifest_data = []
    for img_number in downloaded_images:
        manifest_data.append({
            'img_number': img_number,
            'file_name': f"JEFFERSON_{img_number}.png",
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    # Write to manifest JSON file
    with open(manifest_file, 'w') as f:
        json.dump(manifest_data, f, indent=4)

# Stop timer and calculate total execution time
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

# Report the total number of new files downloaded and execution time
print(f"New files downloaded: {new_files_downloaded}")
print(f"Total execution time: {minutes} minutes and {seconds} seconds.")
