import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from datetime import datetime
import json

# Base URL to scrape for Midlands Mugshots links
date_str = datetime.now().strftime("%Y-%m-%d")
SOURCE_URL = "https://www.abccolumbia.com/news/mugshots/"  # Change this to the actual source
SAVE_FOLDER = f"trainingData/MIDLANDS/{date_str}"

# Ensure the save folder exists
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Manifest file to track downloaded images
manifest_file = os.path.join(SAVE_FOLDER, 'manifest.json')

# Load previously downloaded images from the manifest file
if os.path.exists(manifest_file):
    with open(manifest_file, 'r') as f:
        downloaded_images = {entry['img_name'] for entry in json.load(f)}
else:
    downloaded_images = set()


def get_mugshot_links(source_url):
    """Scrape the given page for hyperlinks containing 'Midlands Mugshots'."""
    response = requests.get(source_url)
    if response.status_code != 200:
        print("Failed to fetch the page.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    # Find all hyperlinks that contain "Midlands Mugshots"
    for a_tag in soup.find_all("a", href=True):
        if "Midlands Mugshots" in a_tag.text:
            full_url = urljoin(source_url, a_tag["href"])
            links.append(full_url)

    return links


def download_jpgs_from_url(page_url):
    """Find and download all JPG images from a given URL."""
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to access {page_url}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    for img_tag in img_tags:
        img_url = img_tag.get("src")
        if img_url and img_url.lower().endswith(".jpg"):
            full_img_url = urljoin(page_url, img_url)
            download_image(full_img_url)


def download_image(img_url):
    """Download an image and save it to the folder."""
    img_name = f"MIDLANDS_{os.path.basename(img_url)}"  # Prepend "Midlands_"
    img_path = os.path.join(SAVE_FOLDER, img_name)

    # Skip if the image has already been downloaded
    if img_name in downloaded_images:
        print(f"Skipping {img_name}. Already downloaded.")
        return

    try:
        img_data = requests.get(img_url).content
        with open(img_path, "wb") as img_file:
            img_file.write(img_data)
        print(f"Downloaded: {img_name}")
        downloaded_images.add(img_name)  # Add to set to track downloaded images
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")


# Main execution
mugshot_links = get_mugshot_links(SOURCE_URL)
for link in mugshot_links:
    download_jpgs_from_url(link)

# Update the manifest file with newly downloaded images
if downloaded_images:
    manifest_data = []
    for img_name in downloaded_images:
        manifest_data.append({
            'img_name': img_name,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    # Write to manifest JSON file
    with open(manifest_file, 'w') as f:
        json.dump(manifest_data, f, indent=4)

# Report the total number of new files downloaded
print(f"Total files downloaded: {len(downloaded_images)}")
