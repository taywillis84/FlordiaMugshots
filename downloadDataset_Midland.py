import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from datetime import datetime

# Base URL to scrape for Midlands Mugshots links
date_str = datetime.now().strftime("%Y-%m-%d")
SOURCE_URL = "https://www.abccolumbia.com/news/mugshots/page/"  # Change this to the actual source
SAVE_FOLDER = f"trainingData/MIDLANDS/{date_str}"

# Ensure the save folder exists
os.makedirs(SAVE_FOLDER, exist_ok=True)


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
    img_name = os.path.join(SAVE_FOLDER, f"MIDLANDS_{os.path.basename(img_url)}")  # Prepend "Midlands_"

    try:
        img_data = requests.get(img_url).content
        with open(img_name, "wb") as img_file:
            img_file.write(img_data)
        print(f"Downloaded: {img_name}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")


# Main execution
mugshot_links = get_mugshot_links(SOURCE_URL)
for link in mugshot_links:
    download_jpgs_from_url(link)
