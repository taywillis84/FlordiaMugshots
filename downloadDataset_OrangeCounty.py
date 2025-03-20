import time
import base64
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
start_time = time.time()
# Set up the Chrome driver
options = webdriver.ChromeOptions()
# Uncomment the next line if you want to connect to an already running Chrome instance
# options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
print("Browser launched!")

# Create the "OrangeCounty" folder if it doesn't exist
folder_path = "trainingData/OrangeCounty"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created.")

# Define the list of letters to iterate over (A to Z)
letters = [chr(i) for i in range(ord('B'), ord('Z') + 1)]

# Iterate over each letter
for letter in letters:
    # Open the page and navigate to the URL
    url = "https://netapps.ocfl.net/BestJail/Home/Inmates#"  # Replace with the actual URL of the page
    driver.get(url)

    # Wait for the page to load
    time.sleep(3)

    try:
        # Find the text box by its id and type the current letter
        input_box = driver.find_element(By.ID, "inmate")
        input_box.clear()  # Clear the field before typing
        input_box.send_keys(letter)
        print(f"Typed letter '{letter}' into the input box.")

        # Click the search button
        search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        search_button.click()
        print(f"Clicked the search button for letter '{letter}'.")

        # Wait for the search results to load
        time.sleep(3)

        # Find all the hyperlinks (<a> tags) on the page
        links = driver.find_elements(By.TAG_NAME, "a")

        # Loop through the links and click the first one that contains a comma
        for link in links:
            if "Water, Garbage & Recycling" in link.text:
                print(f"Stopping the loop as the link '{link.text}' was found.")
                break  # Exit the loop when this link is found

            if "," in link.text:
                link.click()
                print(f'Clicked the hyperlink with a comma in it: "{link.text}"')

                # Wait for the resulting page to load
                time.sleep(3)

                # Find all <img> elements on the page
                images = driver.find_elements(By.TAG_NAME, "img")
                print(f"Found {len(images)} images on the page.")

                # Loop through each image and check if it's Base64-encoded
                for index, img in enumerate(images):
                    img_url = img.get_attribute("src")

                    # Check if the img src is a Base64-encoded image
                    if img_url and img_url.startswith("data:image/png;base64,"):
                        print(f"Base64 PNG image found: Image {index + 1}")

                        # Extract Base64 string from the img src
                        base64_data = img_url.split(",")[1]  # Remove the 'data:image/png;base64,' part

                        # Decode the Base64 string and save it as a PNG file
                        image_data = base64.b64decode(base64_data)
                        file_name = f"{folder_path}/image_{index + 1}_{link.text.replace(',', '').replace(' ', '_')}.png"  # Save in the "OrangeCounty" folder

                        with open(file_name, "wb") as file:
                            file.write(image_data)

                        print(f"Saved as {file_name}")

                        # After saving the first image, stop further processing
                        break  # Stop the loop after saving the first Base64 PNG image

                # Click the close button (button with class "close")
                close_button = driver.find_element(By.CSS_SELECTOR, "button.close")
                close_button.click()
                print("Closed the modal or dialog.")

                # Wait a bit for the modal to close
                time.sleep(2)

                # Go back to the previous page to click the next link
                driver.back()
                time.sleep(3)

    except Exception as e:
        print(f"Error: {e}")

# Close the driver
driver.quit()
print("Process complete!")
elapsed_time = (time.time() - start_time)/60
print(f"Script completed in {elapsed_time} minutes.")
