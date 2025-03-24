import os
from PIL import Image
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt


def analyze_images(folder_path):
    """
    Analyze images in the given folder and return insights about their properties.
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Lists to store image properties
    resolutions = []
    file_sizes = []  # in KB
    aspect_ratios = []
    color_modes = []
    avg_brightness = []

    # Supported image extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            image_path = os.path.join(folder_path, filename)
            try:
                # Open image
                with Image.open(image_path) as img:
                    # Resolution (width, height)
                    width, height = img.size
                    resolutions.append((width, height))

                    # File size in KB
                    file_size = os.path.getsize(image_path) / 1024  # Convert bytes to KB
                    file_sizes.append(file_size)

                    # Aspect ratio
                    aspect_ratio = width / height
                    aspect_ratios.append(round(aspect_ratio, 2))

                    # Color mode
                    color_modes.append(img.mode)

                    # Average brightness (for RGB images)
                    if img.mode == 'RGB':
                        img_array = np.array(img)
                        brightness = np.mean(img_array)  # Mean across all pixels and channels
                        avg_brightness.append(brightness)

            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    # Analyze collected data
    if not resolutions:
        print("No valid images found in the folder.")
        return

    # Common resolutions
    resolution_counts = Counter(resolutions)
    most_common_res = resolution_counts.most_common(1)[0] if resolution_counts else ((0, 0), 0)

    # Common aspect ratios
    aspect_ratio_counts = Counter(aspect_ratios)
    most_common_aspect = aspect_ratio_counts.most_common(1)[0] if aspect_ratio_counts else (0, 0)

    # Color mode distribution
    color_mode_counts = Counter(color_modes)

    # File size statistics
    avg_file_size = np.mean(file_sizes) if file_sizes else 0
    min_file_size = min(file_sizes) if file_sizes else 0
    max_file_size = max(file_sizes) if file_sizes else 0

    # Brightness statistics (for RGB images)
    avg_brightness_value = np.mean(avg_brightness) if avg_brightness else 0
    min_brightness = min(avg_brightness) if avg_brightness else 0
    max_brightness = max(avg_brightness) if avg_brightness else 0

    # Print insights
    print(f"\nImage Analysis for folder: {folder_path}")
    print(f"Total images analyzed: {len(resolutions)}")
    print("\nResolution Insights:")
    print(f"Most common resolution: {most_common_res[0]} (found in {most_common_res[1]} images)")
    print(f"Unique resolutions: {len(resolution_counts)}")

    print("\nAspect Ratio Insights:")
    print(f"Most common aspect ratio: {most_common_aspect[0]} (found in {most_common_aspect[1]} images)")
    print(f"Unique aspect ratios: {len(aspect_ratio_counts)}")

    print("\nColor Mode Insights:")
    for mode, count in color_mode_counts.items():
        print(f"{mode}: {count} images")

    print("\nFile Size Insights (KB):")
    print(f"Average file size: {avg_file_size:.2f} KB")
    print(f"Minimum file size: {min_file_size:.2f} KB")
    print(f"Maximum file size: {max_file_size:.2f} KB")

    if avg_brightness:
        print("\nBrightness Insights (RGB images only, 0-255 scale):")
        print(f"Average brightness: {avg_brightness_value:.2f}")
        print(f"Minimum brightness: {min_brightness:.2f}")
        print(f"Maximum brightness: {max_brightness:.2f}")

    # Optional: Visualize resolution distribution
    visualize_resolutions(resolution_counts, folder_path)


def visualize_resolutions(resolution_counts, folder_path):
    """
    Create a bar plot of resolution distribution and save it.
    """
    if not resolution_counts:
        return

    resolutions = [f"{w}x{h}" for w, h in resolution_counts.keys()]
    counts = list(resolution_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(resolutions, counts)
    plt.xlabel('Resolution (Width x Height)')
    plt.ylabel('Number of Images')
    plt.title(f'Resolution Distribution in {os.path.basename(folder_path)}')
    plt.xticks(rotation=45, ha='right')

    output_path = os.path.join(folder_path, 'resolution_distribution.png')
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved resolution distribution plot to: {output_path}")
    plt.close()


# Main execution
if __name__ == "__main__":
    # Specify the folder path to analyze
    folder_path = "newImages/Midlands"
    analyze_images(folder_path)