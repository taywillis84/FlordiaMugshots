import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the website
url = 'https://www.dothanpd.org/news/mugshots/'

# Folder to save the images
save_folder = 'DOTHAN'

# Create folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Fetch the content of the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all image tags in the HTML
img_tags = soup.find_all('img')

# Extract the URLs of the images (filtering by those containing .jpg in the source)
img_urls = [urljoin(url, img['src']) for img in img_tags if img.get('src') and '.jpg' in img['src'].lower()]

# Initialize a counter for downloaded files
total_files_downloaded = 0

# Download each image
for img_url in img_urls:
    try:
        # Get the image content
        img_data = requests.get(img_url).content
        # Extract the image name from the URL
        img_name = os.path.join(save_folder, os.path.basename(img_url.split('?')[0]))  # Remove query params if any
        # Write the image to the file
        with open(img_name, 'wb') as img_file:
            img_file.write(img_data)
        print(f"Downloaded {img_name}")
        # Increment the counter for each successfully downloaded image
        total_files_downloaded += 1
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

# Report the total number of files downloaded
print(f"Total files downloaded: {total_files_downloaded}")
