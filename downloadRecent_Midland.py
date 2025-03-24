import requests
from bs4 import BeautifulSoup
import re
import os

# URL of the Midlands Mugshots page
url = "https://www.abccolumbia.com/news/mugshots/"

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send a request to fetch the page content
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all links on the page
    links = soup.find_all("a", href=True)

    # Regex pattern to match "Midlands Mugshots [DATE]"
    pattern = re.compile(r"Midlands Mugshots")

    # Search for the first matching link
    mugshot_page_url = None
    for link in links:
        if link.text and pattern.search(link.text):
            mugshot_page_url = link["href"]
            if not mugshot_page_url.startswith("http"):
                mugshot_page_url = "https://www.abccolumbia.com" + mugshot_page_url
            print("Found link:", mugshot_page_url)
            break

    # Proceed if a valid link was found
    if mugshot_page_url:
        response = requests.get(mugshot_page_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all image tags
            image_tags = soup.find_all("img")

            # Extract jpg image URLs
            image_urls = [img["src"] for img in image_tags if "src" in img.attrs and img["src"].endswith(".jpg")]

            # Create a folder to store images
            save_directory = "newImages"
            os.makedirs(save_directory, exist_ok=True)

            # Download images
            for img_url in image_urls:
                img_url = img_url if img_url.startswith("http") else "https://www.abccolumbia.com" + img_url
                img_data = requests.get(img_url, headers=headers).content
                filename = os.path.join(save_directory, "MIDLANDS_" + os.path.basename(img_url))
                with open(filename, "wb") as img_file:
                    img_file.write(img_data)
                print(f"Downloaded: {filename}")
        else:
            print("Failed to retrieve the mugshot page. Status code:", response.status_code)
else:
    print("Failed to retrieve the main page. Status code:", response.status_code)
