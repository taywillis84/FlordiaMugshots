import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# Function to fetch and extract links that contain "MONTGOMERY COUNTY MUGSHOTS" (case-insensitive)
def extract_montgomery_mugshot_links(url):
    # Send GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {url}")
        return []

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all anchor tags (<a>) that contain "MONTGOMERY COUNTY MUGSHOTS" (case-insensitive)
    links = soup.find_all('a', string=lambda text: text and "montgomery county mugshots" in text.lower())

    # Extract the href attribute from each link
    hrefs = [link.get('href') for link in links if link.get('href')]

    return hrefs

# Function to download images from a given page
def download_images_from_page(page_url, download_folder):
    # Send GET request to the child page URL
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to fetch the child page: {page_url}")
        return

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image tags (<img>) on the page
    img_tags = soup.find_all('img')

    # Make sure the download folder exists
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Download each image
    for idx, img_tag in enumerate(img_tags, start=1):
        img_url = img_tag.get('src')
        if img_url:
            # Ensure we have a complete URL (handle relative paths)
            img_url = urllib.parse.urljoin(page_url, img_url)

            # Get the image name (e.g., "image1.jpg")
            img_name = os.path.basename(img_url)

            # Download and save the image
            try:
                img_data = requests.get(img_url).content
                img_path = os.path.join(download_folder, img_name)

                # Save the image to the folder
                with open(img_path, 'wb') as f:
                    f.write(img_data)

                print(f"Downloaded: {img_name}")
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

# Main code to run the functions
if __name__ == "__main__":
    base_url = 'https://www.waka.com/mugshots/'  # Replace with the base URL where you found the "MONTGOMERY COUNTY MUGSHOTS" links
    download_folder = 'trainingData/MONGOMERY'  # Folder to save the images

    # Extract Montgomery County Mugshots links
    mugshot_links = extract_montgomery_mugshot_links(base_url)

    if mugshot_links:
        print("Found Montgomery County Mugshots links:")
        for idx, link in enumerate(mugshot_links, start=1):
            print(f"{idx}. {link}")
            # Download images from each discovered mugshot page
            download_images_from_page(link, download_folder)
    else:
        print("No Montgomery County Mugshots links found.")
