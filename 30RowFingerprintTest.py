import cv2
import numpy as np
import os
import json


def get_average_colors(image_path, top_percentage=5):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image from {image_path}")

    height, width, _ = image.shape
    top_row_height = int(height * (top_percentage / 100))
    top_region = image[0:top_row_height, :]
    avg_color = np.mean(top_region, axis=(0, 1))

    return tuple(avg_color)


def load_location_fingerprint(fingerprint_path):
    if not os.path.exists(fingerprint_path):
        raise FileNotFoundError(f"Fingerprint file not found: {fingerprint_path}")

    with open(fingerprint_path, "r") as f:
        fingerprint = json.load(f)

    fingerprint["top"]["mean"] = np.array(fingerprint["top"]["mean"])
    fingerprint["top"]["std"] = np.array(fingerprint["top"]["std"])

    return fingerprint


def calculate_similarity_score(avg_color, fingerprint):
    mean = fingerprint["top"]["mean"]
    std_dev = fingerprint["top"]["std"]

    # Avoid division by zero by replacing zero std deviations with a small number
    std_dev = np.where(std_dev == 0, 1e-6, std_dev)

    # Compute Z-score (distance in terms of standard deviations)
    z_scores = np.abs((avg_color - mean) / std_dev)
    z_score_sum = np.sum(z_scores)

    # Convert Z-score sum into a similarity score (higher deviation = lower score)
    score = max(1, 100 - (z_score_sum * 10))  # Scaling factor can be adjusted
    return score


def process_directory(folder_path, fingerprint_path, output_file="image_scores.json", top_percentage=5):
    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return

    fingerprint = load_location_fingerprint(fingerprint_path)
    files = os.listdir(folder_path)
    image_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff"))]

    if not image_files:
        print(f"No image files found in {folder_path}")
        return

    print("\nSimilarity Scores for Images:\n")
    results = []
    total_score = 0

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        try:
            avg_color = get_average_colors(image_path, top_percentage)
            score = calculate_similarity_score(avg_color, fingerprint)
            print(f"{image_file}: Similarity Score = {score:.2f}")
            results.append({"filename": image_file, "score": score})
            total_score += score
        except Exception as e:
            print(f"Error processing {image_file}: {e}")

    average_score = total_score / len(image_files) if image_files else 0
    output_path = os.path.join(folder_path, output_file)

    try:
        with open(output_path, "w") as json_file:
            json.dump({"results": results, "average_score": average_score}, json_file, indent=4)
        print(f"\nResults saved to {output_path}")
        print(f"Average Score: {average_score:.2f}")
    except Exception as e:
        print(f"Error saving results to JSON file: {e}")


# Example usage:
if __name__ == "__main__":
    folder_path = "OrangeCounty - Copy"  # Folder containing images
    fingerprint_path = "OrangeCounty - Copy/location_fingerprint.json"  # Specify the exact fingerprint file path
    process_directory(folder_path, fingerprint_path)
