import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

# Base URL of the website, we will append the page numbers
base_url = 'https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000?Page='

# Folder to save the images
save_folder = 'JeffersonCounty'

# Create folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

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

    # Extract the URLs of the images
    img_urls = [urljoin(url, img['src']) for img in img_tags if img.get('src')]

    # Download each image from the current page
    for img_url in img_urls:
        try:
            # Get the image content
            img_data = requests.get(img_url).content
            # Open the image using PIL
            img = Image.open(BytesIO(img_data))

            # Extract the image name and replace the extension with '.png'
            img_name = os.path.join(save_folder, os.path.basename(img_url.split('?')[0]).split('.')[
                0] + '.png')  # Remove query params and change to .png

            # Save the image as PNG
            img.save(img_name, 'PNG')
            print(f"Downloaded {img_name}")
            # Increment the counter for each successfully downloaded image
            total_files_downloaded += 1
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

# Report the total number of files downloaded
print(f"Total files downloaded: {total_files_downloaded}")
