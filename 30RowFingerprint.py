import cv2
import numpy as np
import os
import json


def get_average_colors(image_path, top_percentage=5):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image from {image_path}")

    # Resize image to 480x600 before processing
    image = cv2.resize(image, (480, 600))

    height, width, _ = image.shape
    top_row_height = int(height * (top_percentage / 100))
    top_region = image[0:top_row_height, :]
    avg_color = np.mean(top_region, axis=(0, 1))

    return tuple(avg_color)


def save_location_fingerprint(folder_path, top_percentage=5, fingerprint_filename="location_fingerprint.json"):
    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return

    files = os.listdir(folder_path)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))]

    if not image_files:
        print(f"No image files found in {folder_path}")
        return

    colors = []
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        try:
            avg_color = get_average_colors(image_path, top_percentage)
            colors.append(avg_color)
            print(f"Processed {image_file}: Average color of top {top_percentage}%: {avg_color}")
        except Exception as e:
            print(f"Error processing {image_file}: {e}")

    color_array = np.array(colors)
    color_mean = np.mean(color_array, axis=0)
    color_std = np.std(color_array, axis=0)

    fingerprint = {
        "top": {
            "mean": color_mean.tolist(),
            "std": color_std.tolist()
        }
    }

    fingerprint_path = os.path.join(folder_path, fingerprint_filename)
    try:
        with open(fingerprint_path, "w") as f:
            json.dump(fingerprint, f, indent=4)
        print(f"\nFingerprint saved to {fingerprint_path}")
    except Exception as e:
        print(f"Error saving fingerprint file: {e}")


# Example usage:
folder_path = "OrangeCounty - Copy"  # Folder containing images from the known location
save_location_fingerprint(folder_path)
